from typing import Protocol, Tuple

from shapely.geometry.base import BaseGeometry

from osm_painter.model.drawable import Drawable


class Location(Protocol):
    def to_overpass(self) -> str:
        ...

    def get_perimeter(self) -> Drawable:
        ...

    def get_surface(self) -> BaseGeometry:
        ...

    def get_bounds(self) -> Tuple[float, float, float, float]:
        ...
