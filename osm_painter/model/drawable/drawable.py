from typing import Dict, Optional, Protocol

import matplotlib.pyplot as plt

from shapely.geometry.base import BaseGeometry

from osm_painter.model.style import Style


class Drawable(Protocol):
    tags: Dict[str, str]

    def draw(self, axes: plt.Axes, style: Style, perimeter: Optional[BaseGeometry]) -> None:
        ...
