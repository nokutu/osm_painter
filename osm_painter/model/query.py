from typing import List, Protocol

import overpy

from .drawable import Area, Drawable, Way
from .location import Location
from ..utils.joblib import memory


_api = overpy.Overpass(url='https://overpass.openstreetmap.fr/api/interpreter')
_api.query = memory.cache(_api.query)


class Query(Protocol):
    def query(self, location: Location) -> List[Drawable]:
        ...


class WayQuery(Query):
    _query_filter: str

    def __init__(self, query_filter: str):
        super().__init__()
        self._query_filter = query_filter

    def query(self, location: Location) -> List[Drawable]:
        result = _api.query(f'way({location.to_overpass()}){self._query_filter};'
                            f'(._;>;);'
                            f'out body;')
        return [Way(way) for way in result.ways]


class AreaQuery(Query):
    _query_filter: str

    def __init__(self, query_filter: str):
        super().__init__()
        self._query_filter = query_filter

    def query(self, location: Location) -> List[Drawable]:
        result = _api.query(f'way({location.to_overpass()}){self._query_filter};'
                            f'(._;>;);'
                            f'out body;')

        return [Area(way) for way in result.ways]
