import itertools
from typing import Optional, List, Tuple

import numpy as np
from descartes import PolygonPatch
from matplotlib import pyplot as plt, cm
from matplotlib.colors import Normalize, Colormap
from matplotlib.contour import QuadContourSet
from numpy.typing import NDArray
from shapely.geometry import LineString
from shapely.geometry.base import BaseGeometry

from osm_painter.model.location import Location
from osm_painter.model.style import LayerStyle
from osm_painter.utils.coords_utils import transform_coords
from osm_painter.utils.opentopodata import query_topo
from .layer import Layer


class ElevationLayer(Layer):
    name: str
    _samples: int
    _levels: int
    _legend: bool
    _lines: List[Tuple[float, LineString]] = []

    _min_max_elevation: Tuple[float, float] = (0, 0)
    _contour: QuadContourSet = None

    _x: NDArray[np.float32]
    _y: NDArray[np.float32]
    _z: NDArray[np.float32]

    def __init__(self, name: str, samples: int = 30, levels: int = 30, legend: bool = False):
        super().__init__()
        self.name = name
        self._samples = samples
        self._levels = levels
        self._legend = legend

    def query(self, location: Location) -> None:
        left, bottom, right, top = location.get_bounds()

        self._x, self._y = np.meshgrid(np.linspace(bottom, top, self._samples),
                                       np.linspace(left, right, self._samples))  # type: ignore

        samples = []
        for i, j in itertools.product(range(self._samples), range(self._samples)):
            samples.append((self._x[i, j], self._y[i, j]))

        result = transform_coords(self._x.flatten(), self._y.flatten()).reshape((*self._x.shape, 2))
        self._x = result[:, :, 0]
        self._y = result[:, :, 1]
        self._z = np.zeros(self._x.shape)

        offset = 0
        positions = list(itertools.product(range(self._samples), range(self._samples)))
        for i in range(0, self._samples ** 2, 100):
            elevations = query_topo(samples[i:i + 100])

            for idx, elev in enumerate(elevations):
                self._z[positions[offset + idx]] = elev
            offset += 100

        self._min_max_elevation = (np.min(self._z), np.max(self._z))  # type: ignore

        # Create new figure, to get contours.
        fig = plt.figure()
        self._contour: QuadContourSet = plt.contour(self._x, self._y, self._z, levels=self._levels)
        for idx, collection in enumerate(self._contour.collections):
            for path in collection.get_paths():
                if path.vertices.shape[0] > 1:
                    self._lines.append((self._contour.levels[idx], LineString(path.vertices)))
        plt.close(fig)

    def draw(self, axes: plt.Axes, layer_style: LayerStyle, perimeter: Optional[BaseGeometry]) -> None:
        width = 1.
        style = layer_style['default']

        if 'lw' in style:
            width = style['lw']
        for elevation, line in self._lines:
            line = line.buffer(width / 2)

            if perimeter:
                line = line.intersection(perimeter)

            color = None
            if 'color' in style:
                if isinstance(style['color'], Colormap):
                    color = style['color'](
                        (elevation - self._min_max_elevation[0]) /
                        (self._min_max_elevation[1] - self._min_max_elevation[0])
                    )
                else:
                    color = style['color']

            if not line.is_empty:
                axes.add_patch(PolygonPatch(line, **dict(style, lw=0, color=color)))

        if self._legend and isinstance(style['color'], Colormap):
            plt.colorbar(cm.ScalarMappable(norm=Normalize(self._min_max_elevation[0], self._min_max_elevation[1]),
                                           cmap=style['color']), ax=axes, shrink=0.5)
