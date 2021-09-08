from typing import List

from osm_painter.model.drawable import Area, Drawable
from osm_painter.model.location import Location
from osm_painter.model.query.api import overpy_api
from osm_painter.model.query.query import Query


class AreaQuery(Query):
    _query_filter: str

    def __init__(self, query_filter: str):
        super().__init__()
        self._query_filter = query_filter

    def query(self, location: Location) -> List[Drawable]:
        result = overpy_api.query(f'way({location.to_overpass()}){self._query_filter};'
                                  f'(._;>;);'
                                  f'out body;')

        return [Area(way) for way in result.ways]
