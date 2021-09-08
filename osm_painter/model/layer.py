import itertools
from typing import List, Optional, Protocol, Tuple

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from descartes import PolygonPatch
from matplotlib import cm
from matplotlib.colors import Colormap, Normalize
from matplotlib.contour import QuadContourSet
from shapely.geometry import LineString
from shapely.geometry.base import BaseGeometry

from .drawable import Drawable
from .location import Location
from .query import Query, WayQuery, AreaQuery
from .style import LayerStyle
from ..utils.coords_utils import transform_coords
from ..utils.opentopodata import query_topo


class Layer(Protocol):
    name: str

    def query(self, location: Location) -> None:
        ...

    def draw(self, axes: plt.Axes, layer_style: LayerStyle, perimeter: Optional[BaseGeometry]) -> None:
        ...


class QueryLayer(Layer):
    name: str
    _query: Query

    _result: List[Drawable]

    def __init__(self, name: str, query: Query):
        super().__init__()
        self.name = name
        self._query = query

    def query(self, location: Location) -> None:
        self._result = self._query.query(location)

    def draw(self, axes: plt.Axes, layer_style: LayerStyle, perimeter: Optional[BaseGeometry]) -> None:
        for drawable in self._result:
            if self.name in drawable.tags:
                if drawable.tags[self.name] in layer_style:
                    drawable.draw(axes, layer_style[drawable.tags[self.name]], perimeter)
                elif 'default' in layer_style:
                    drawable.draw(axes, layer_style['default'], perimeter)


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


class Layers:
    building_layer = QueryLayer('building', AreaQuery('["building"]'))
    highway_layer = QueryLayer('highway', WayQuery('["highway"]'))
    elevation_layer = ElevationLayer('elevation')
    landuse_layer = QueryLayer('landuse', AreaQuery('["landuse"]'))
    leisure_layer = QueryLayer('leisure', AreaQuery('["leisure"]'))
    water_layer = QueryLayer('water', AreaQuery('["water"]'))
    waterway_layer = QueryLayer('waterway', WayQuery('["waterway"]'))
