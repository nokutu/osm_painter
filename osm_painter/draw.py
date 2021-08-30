from descartes import PolygonPatch
from joblib import Parallel, delayed
import matplotlib.pyplot as plt

from .model.layer import Layer
from .model.location import Location
from .model.style import StyleDict, Style


def draw(ax: plt.Axes, location: Location, layers: list[Layer], style: StyleDict, perimeter_style: Style,
         background_style: Style) -> None:
    ax.axis('off')
    ax.axis('equal')
    ax.autoscale()

    Parallel(n_jobs=8, prefer='threads')(delayed(layer.query)(location) for layer in layers)

    draw_area = location.get_surface().buffer(-perimeter_style['lw'])
    for layer in layers:
        layer.draw(ax, style[layer.name] if layer.name in style else {}, draw_area)

    ax.add_patch(PolygonPatch(draw_area, **background_style))
    location.get_perimeter().draw(ax, perimeter_style, None)
