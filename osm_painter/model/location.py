import math
from typing import Protocol, Tuple

import numpy as np
from shapely.geometry import Point, Polygon
from shapely.geometry.base import BaseGeometry

from .drawable import Drawable, Edge
from ..utils.coords_utils import transform_coords, transform_coords_inv


class Location(Protocol):
    def to_overpass(self) -> str:
        ...

    def get_perimeter(self) -> Drawable:
        ...

    def get_surface(self) -> BaseGeometry:
        ...

    def get_bounds(self) -> Tuple[float, float, float, float]:
        ...


class RadiusLocation:
    _coords: Tuple[float, float]
    _radius: float

    def __init__(self, coords: Tuple[float, float], radius: float):
        self._coords = coords
        self._radius = radius

    def to_overpass(self) -> str:
        return f'around:{self._radius},{self._coords[0]},{self._coords[1]}'

    def get_perimeter(self) -> Drawable:
        return Edge(self.get_surface())

    def get_surface(self) -> BaseGeometry:
        lat = np.array([self._coords[0]], dtype=np.float32)
        lon = np.array([self._coords[1]], dtype=np.float32)
        center = transform_coords(lat, lon)[0]
        return Point(center).buffer(self._radius)

    def get_bounds(self) -> Tuple[float, float, float, float]:
        center = transform_coords(self._coords[0], self._coords[1])
        lats = np.array([center[0] - self._radius, center[0] + self._radius], dtype=np.float32)
        lons = np.array([center[1] - self._radius, center[1] + self._radius], dtype=np.float32)
        bounds = transform_coords_inv(lats, lons)
        return bounds[0, 1], bounds[0, 0], bounds[1, 1], bounds[1, 0]


class BoxLocation:
    _coords: Tuple[float, float]
    _width: float
    _height: float
    _radius: float

    def __init__(self, coords: Tuple[float, float], width: float, height: float, corner_radius: float = 0):
        self._coords = coords
        self._width = width
        self._height = height
        self._radius = math.sqrt(width ** 2 + height ** 2) / 2
        self._corner_radius = corner_radius

    def to_overpass(self) -> str:
        return f'around:{self._radius},{self._coords[0]},{self._coords[1]}'

    def get_perimeter(self) -> Drawable:
        return Edge(self.get_surface())

    def get_surface(self) -> BaseGeometry:
        lat = np.array([self._coords[0]], dtype=np.float32)
        lon = np.array([self._coords[1]], dtype=np.float32)
        center = transform_coords(lat, lon)[0]

        width = self._width - self._corner_radius * 2
        height = self._height - self._corner_radius * 2
        square = Polygon([
            center + (-width / 2, -height / 2),
            center + (width / 2, -height / 2),
            center + (width / 2, height / 2),
            center + (-width / 2, height / 2),
        ])

        if self._corner_radius:
            return square.buffer(self._corner_radius)
        return square
