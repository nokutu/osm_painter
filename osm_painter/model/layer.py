from typing import Optional

import matplotlib.pyplot as plt
from shapely.geometry.base import BaseGeometry

from .drawable import Drawable
from .location import Location
from .query import Query, WayQuery, AreaQuery
from .style import LayerStyle


class Layer:
    name: str
    _query: Query

    _result: list[Drawable]

    def __init__(self, name: str, query: Query):
        self.name = name
        self._query = query

    def query(self, location: Location) -> None:
        self._result = self._query.query(location)

    def draw(self, axes: plt.Axes, style: LayerStyle, perimeter: Optional[BaseGeometry]) -> None:
        for drawable in self._result:
            if self.name in drawable.tags:
                if drawable.tags[self.name] in style:
                    drawable.draw(axes, style[drawable.tags[self.name]], perimeter)
                elif 'default' in style:
                    drawable.draw(axes, style['default'], perimeter)


class Layers:
    building_layer = Layer('building', AreaQuery('["building"]'))
    highway_layer = Layer('highway', WayQuery('["highway"]'))
    landuse_layer = Layer('landuse', AreaQuery('["landuse"]'))
    leisure_layer = Layer('leisure', AreaQuery('["leisure"]'))
    water_layer = Layer('water', AreaQuery('["water"]'))
    waterway_layer = Layer('waterway', WayQuery('["waterway"]'))
