from typing import Protocol, Optional

import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry.base import BaseGeometry

from osm_painter.model.style import Style

import pyproj

_transformer = pyproj.Transformer.from_crs(4326, 3857)


class Drawable(Protocol):
    tags: dict[str, str]

    def draw(self, ax: plt.Axes, style: Style, perimeter: Optional[BaseGeometry]) -> None:
        ...

    @staticmethod
    def transform_coords(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
        return np.vstack(_transformer.transform(lat, lon)).transpose()
