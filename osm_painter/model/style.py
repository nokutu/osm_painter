from typing import Dict, TypedDict, Tuple, Union

from matplotlib.colors import Colormap

Color = Union[Tuple[float, float, float], str]


class Style(TypedDict, total=False):
    lw: float
    ec: Color
    fc: Color
    color: Union[Color, Colormap]
    zorder: int
    hatch: str


LayerStyle = Dict[str, Style]
StyleDict = Dict[str, LayerStyle]
