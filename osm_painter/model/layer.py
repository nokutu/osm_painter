from typing import List, Optional, Union

from matplotlib import pyplot as plt
from shapely.geometry.base import BaseGeometry

from . import Style
from .drawable import Drawable
from .location import Location
from .query import Query, WayQuery, AreaQuery
from .style import LayerStyle


class Layer:
    name: str
    _query: Query

    _result: List[Drawable]

    def __init__(self, name: str, query: Query):
        self.name = name
        self._query = query

    def query(self, location: Location) -> None:
        self._result = self._query.query(location)

    def draw(self, ax: plt.Axes, style: LayerStyle, perimeter: Optional[BaseGeometry]) -> None:
        for drawable in self._result:
            if self.name in drawable.tags:
                if drawable.tags[self.name] in style:
                    drawable.draw(ax, style[drawable.tags[self.name]], perimeter)
                elif 'default' in style:
                    drawable.draw(ax, style['default'], perimeter)


building_layer = Layer('building', AreaQuery('["building"]'))
highway_layer = Layer('highway', WayQuery('["highway"]'))
landuse_layer = Layer('landuse', AreaQuery('["landuse"]'))
leisure_layer = Layer('leisure', AreaQuery('["leisure"]'))
water_layer = Layer('water', AreaQuery('["water"]'))
waterway_layer = Layer('waterway', WayQuery('["waterway"]'))
