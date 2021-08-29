from typing import Optional, overload

import numpy as np
import overpy
import pyproj
from descartes import PolygonPatch
from matplotlib import pyplot as plt
from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry

from .drawable import Drawable
from osm_painter.model.style import Style


class Area(Drawable):
    _polygon: BaseGeometry

    def __init__(self, way: overpy.Way):
        lat = np.array([node.lat for node in way.nodes], dtype=np.float32)
        lon = np.array([node.lon for node in way.nodes], dtype=np.float32)
        self._polygon = Polygon(self.transform_coords(lat, lon))
        self.tags = way.tags

    def draw(self, ax: plt.Axes, style: Style, perimeter: Optional[BaseGeometry]) -> None:
        polygon = self._polygon
        if perimeter:
            polygon = polygon.intersection(perimeter)

        if not polygon.is_empty:
            ax.add_patch(PolygonPatch(polygon, **style))
