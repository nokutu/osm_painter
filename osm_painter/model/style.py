from typing import TypedDict, Tuple, Union

Color = Union[Tuple[float, float, float], str]


class Style(TypedDict, total=False):
    lw: float
    ec: Color
    fc: Color
    color: Color
    zorder: int
    hatch: str


LayerStyle = dict[str, Style]
StyleDict = dict[str, LayerStyle]
