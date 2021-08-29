from typing import overload, Tuple, Optional

import numpy as np
import overpy
from descartes import PolygonPatch
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from .drawable import Drawable
from osm_painter.model.style import Style


class Edge(Drawable):
    _geometry: BaseGeometry

    def __init__(self, geometry: BaseGeometry):
        self._geometry = geometry
        self.tags = {}

    def draw(self, ax: plt.Axes, style: Style, perimeter: Optional[BaseGeometry]) -> None:
        width = 1.
        if 'lw' in style:
            width = style['lw']

        outer = self._geometry.buffer(width / 2)
        inner = self._geometry.buffer(-width / 2)

        geom = outer - inner
        if perimeter:
            geom = perimeter.area.intersection(geom)
        ax.add_patch(PolygonPatch(geom, **style))
