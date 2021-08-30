from typing import Optional

from descartes import PolygonPatch
import matplotlib.pyplot as plt
import numpy as np
import overpy
from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry

from .drawable import Drawable
from ..style import Style


class Area(Drawable):
    _polygon: BaseGeometry

    def __init__(self, way: overpy.Way):
        super().__init__()
        lat = np.array([node.lat for node in way.nodes], dtype=np.float32)
        lon = np.array([node.lon for node in way.nodes], dtype=np.float32)
        self._polygon = Polygon(self.transform_coords(lat, lon))
        self.tags = way.tags

    def draw(self, axes: plt.Axes, style: Style, perimeter: Optional[BaseGeometry]) -> None:
        polygon = self._polygon
        if perimeter:
            polygon = polygon.intersection(perimeter)

        if not polygon.is_empty:
            axes.add_patch(PolygonPatch(polygon, **style))
