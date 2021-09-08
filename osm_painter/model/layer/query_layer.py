from typing import List, Optional

from matplotlib import pyplot as plt
from shapely.geometry.base import BaseGeometry

from osm_painter.model.drawable import Drawable
from osm_painter.model.layer.layer import Layer
from osm_painter.model.location import Location
from osm_painter.model.query import Query
from osm_painter.model.style import LayerStyle


class QueryLayer(Layer):
    name: str
    _query: Query

    _result: List[Drawable]

    def __init__(self, name: str, query: Query):
        super().__init__()
        self.name = name
        self._query = query

    def query(self, location: Location) -> None:
        self._result = self._query.query(location)

    def draw(self, axes: plt.Axes, layer_style: LayerStyle, perimeter: Optional[BaseGeometry]) -> None:
        for drawable in self._result:
            if self.name in drawable.tags:
                if drawable.tags[self.name] in layer_style:
                    drawable.draw(axes, layer_style[drawable.tags[self.name]], perimeter)
                elif 'default' in layer_style:
                    drawable.draw(axes, layer_style['default'], perimeter)
