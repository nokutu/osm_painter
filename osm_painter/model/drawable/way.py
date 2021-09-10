from typing import Optional

from descartes import PolygonPatch
import matplotlib.pyplot as plt
import numpy as np
import overpy
from shapely.geometry import LineString
from shapely.geometry.base import BaseGeometry

from osm_painter.model.style import Style
from osm_painter.utils import transform_coords

from .drawable import Drawable


class Way(Drawable):
    _way: overpy.Way
    _line: BaseGeometry

    def __init__(self, way: overpy.Way):
        super().__init__()
        self._way = way

        lat = np.array([node.lat for node in way.nodes], dtype=np.float32)
        lon = np.array([node.lon for node in way.nodes], dtype=np.float32)
        self._line = LineString(transform_coords(lat, lon))
        self.tags = way.tags

    def draw(self, axes: plt.Axes, style: Style, perimeter: Optional[BaseGeometry]) -> None:
        line = self._line
        width = 1.

        if 'lw' in style:
            width = style['lw']

        line = line.buffer(width / 2)

        if perimeter:
            line = line.intersection(perimeter)

        if not line.is_empty:
            axes.add_patch(PolygonPatch(line, **dict(style, lw=0)))
