from typing import overload, Tuple, Optional

import numpy as np
import overpy
from descartes import PolygonPatch
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from .drawable import Drawable
from osm_painter.model.style import Style


class Circle(Drawable):
    _radius: float
    _center: np.ndarray

    def __init__(self, center: Tuple[float, float], radius: float):
        lat = np.array([center[0]], dtype=np.float32)
        lon = np.array([center[1]], dtype=np.float32)
        self._center = self.transform_coords(lat, lon)[0]
        self._radius = radius
        self.tags = {}

    def draw(self, ax: plt.Axes, style: Style, perimeter: Optional[BaseGeometry]) -> None:
        width = 1.
        if 'lw' in style:
            width = style['lw']

        outer = Point(self._center).buffer(self._radius + width / 2)
        inner = Point(self._center).buffer(self._radius - width / 2)

        geom = outer - inner
        if perimeter:
            geom = perimeter.area.intersection(geom)
        ax.add_patch(PolygonPatch(geom, **style))
