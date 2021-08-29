from typing import Optional

import numpy as np
import overpy
from descartes import PolygonPatch
from shapely.geometry import LineString
import matplotlib.pyplot as plt
from shapely.geometry.base import BaseGeometry

from .drawable import Drawable
from osm_painter.model.style import Style


class Way(Drawable):
    _way: overpy.Way
    _line: BaseGeometry

    def __init__(self, way: overpy.Way):
        self._way = way

        lat = np.array([node.lat for node in way.nodes], dtype=np.float32)
        lon = np.array([node.lon for node in way.nodes], dtype=np.float32)
        self._line = LineString(self.transform_coords(lat, lon))
        self.tags = way.tags

    def draw(self, ax: plt.Axes, style: Style, perimeter: Optional[BaseGeometry]) -> None:
        line = self._line
        width = 1.

        if 'lw' in style:
            width = style['lw']

        line = line.buffer(width/2)

        if perimeter:
            line = line.intersection(perimeter)

        if not line.is_empty:
            ax.add_patch(PolygonPatch(line, **dict(style, lw=0)))
