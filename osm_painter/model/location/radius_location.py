from typing import Tuple

import numpy as np
from shapely.geometry import Point
from shapely.geometry.base import BaseGeometry

from osm_painter.model.drawable import Drawable, Edge
from osm_painter.utils.coords_utils import transform_coords, transform_coords_inv


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
