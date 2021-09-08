from typing import cast, overload, Tuple, Union

import numpy as np
import pyproj

_transformer = pyproj.Transformer.from_crs(4326, 3857)
_transformer_inverse = pyproj.Transformer.from_crs(3857, 4326)


@overload
def transform_coords(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    ...


@overload
def transform_coords(lat: float, lon: float) -> Tuple[float, float]:
    ...


def transform_coords(lat: Union[np.ndarray, float], lon: Union[np.ndarray, float]) -> \
        Union[np.ndarray, Tuple[float, float]]:
    if isinstance(lat, np.ndarray):
        return np.vstack(_transformer.transform(lat, lon)).transpose()
    return cast(Tuple[float, float], _transformer.transform(lat, lon))


@overload
def transform_coords_inv(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    ...


@overload
def transform_coords_inv(lat: float, lon: float) -> Tuple[float, float]:
    ...


def transform_coords_inv(lat: Union[np.ndarray, float], lon: Union[np.ndarray, float]) -> \
        Union[np.ndarray, Tuple[float, float]]:
    if isinstance(lat, np.ndarray):
        return np.vstack(_transformer_inverse.transform(lat, lon)).transpose()
    return cast(Tuple[float, float], _transformer_inverse.transform(lat, lon))
