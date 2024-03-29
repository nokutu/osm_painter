from typing import Dict, Optional, Tuple

from descartes import PolygonPatch
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from osm_painter.model.style import Style
from osm_painter.utils import transform_coords

from .drawable import Drawable


class Circle(Drawable):
    _radius: float
    _center: np.ndarray

    def __init__(self, center: Tuple[float, float], radius: float):
        super().__init__()
        lat = np.array([center[0]], dtype=np.float32)
        lon = np.array([center[1]], dtype=np.float32)
        self._center = transform_coords(lat, lon)[0]
        self._radius = radius
        self.tags: Dict[str, str] = {}

    def draw(self, axes: plt.Axes, style: Style, perimeter: Optional[BaseGeometry]) -> None:
        width = 1.
        if 'lw' in style:
            width = style['lw']

        outer = Point(self._center).buffer(self._radius + width / 2)
        inner = Point(self._center).buffer(self._radius - width / 2)

        geom = outer - inner
        if perimeter:
            geom = perimeter.area.intersection(geom)
        axes.add_patch(PolygonPatch(geom, **style))
