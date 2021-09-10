from typing import Optional, Protocol

from matplotlib import pyplot as plt
from shapely.geometry.base import BaseGeometry

from osm_painter.model.location import Location
from osm_painter.model.style import LayerStyle


class Layer(Protocol):
    name: str

    def query(self, location: Location) -> None:
        ...

    def draw(self, axes: plt.Axes, layer_style: LayerStyle, perimeter: Optional[BaseGeometry]) -> None:
        ...
