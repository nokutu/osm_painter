from typing import Dict, TypedDict, Tuple, Union

from matplotlib.colors import Colormap

_color = Union[Tuple[float, float, float], str]


class Style(TypedDict, total=False):
    lw: float
    ec: _color
    fc: _color
    color: Union[_color, Colormap]
    zorder: int
    hatch: str


LayerStyle = Dict[str, Style]
StyleDict = Dict[str, LayerStyle]
