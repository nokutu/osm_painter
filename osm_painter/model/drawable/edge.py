from typing import Optional

from descartes import PolygonPatch
import matplotlib.pyplot as plt
from shapely.geometry.base import BaseGeometry

from .drawable import Drawable
from ..style import Style


class Edge(Drawable):
    _geometry: BaseGeometry

    def __init__(self, geometry: BaseGeometry):
        super().__init__()
        self._geometry = geometry
        self.tags: dict[str, str] = {}

    def draw(self, axes: plt.Axes, style: Style, perimeter: Optional[BaseGeometry]) -> None:
        width = 1.
        if 'lw' in style:
            width = style['lw']

        outer = self._geometry.buffer(width / 2)
        inner = self._geometry.buffer(-width / 2)

        geom = outer - inner
        if perimeter:
            geom = perimeter.area.intersection(geom)
        axes.add_patch(PolygonPatch(geom, **style))
