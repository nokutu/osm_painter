from typing import List

from descartes import PolygonPatch
from joblib import Parallel, delayed
import matplotlib.pyplot as plt

from .model.layer import Layer
from .model.location import Location
from .model.style import StyleDict, Style


def draw(axes: plt.Axes, location: Location, layers: List[Layer], style: StyleDict, perimeter_style: Style,
         background_style: Style) -> None:
    axes.axis('off')
    axes.axis('equal')
    axes.autoscale()

    Parallel(n_jobs=8, prefer='threads')(delayed(layer.query)(location) for layer in layers)

    draw_area = location.get_surface().buffer(-perimeter_style['lw'])
    for layer in layers:
        layer.draw(axes, style[layer.name] if layer.name in style else {}, draw_area)

    axes.add_patch(PolygonPatch(draw_area, **background_style))
    location.get_perimeter().draw(axes, perimeter_style, None)
