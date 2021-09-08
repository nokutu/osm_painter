from typing import List, Protocol

from osm_painter.model.drawable import Drawable
from osm_painter.model.location import Location


class Query(Protocol):
    def query(self, location: Location) -> List[Drawable]:
        ...
