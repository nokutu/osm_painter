from typing import List

from descartes import PolygonPatch
from joblib import Parallel, delayed
import matplotlib.pyplot as plt

from .model import Layer, Location, StyleDict, Style


def draw(axes: plt.Axes, location: Location, layers: List[Layer], style: StyleDict) -> None:
    axes.axis('off')
    axes.axis('equal')
    axes.autoscale()

    Parallel(n_jobs=8, prefer='threads')(delayed(layer.query)(location) for layer in layers)

    perimeter_lw: float = 0
    if 'perimeter' in style and 'default' in style['perimeter'] and 'lw' in style['perimeter']['default']:
        perimeter_lw = style['perimeter']['default']['lw']

    draw_area = location.get_surface().buffer(-perimeter_lw)
    for layer in layers:
        layer.draw(axes, style[layer.name] if layer.name in style else {}, draw_area)

    background_style: Style = {}
    if 'background' in style and 'default' in style['background']:
        background_style = style['background']['default']

    axes.add_patch(PolygonPatch(draw_area, **background_style))
    if 'perimeter' in style and 'default' in style['perimeter']:
        location.get_perimeter().draw(axes, style['perimeter']['default'], None)
