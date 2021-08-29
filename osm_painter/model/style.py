from typing import TypedDict, Dict, Tuple, Union

Color = Union[Tuple[float, float, float], str]


class Style(TypedDict, total=False):
    lw: float
    ec: Color
    fc: Color
    color: Color
    zorder: int
    hatch: str


LayerStyle = Dict[str, Style]
StyleDict = Dict[str, LayerStyle]
