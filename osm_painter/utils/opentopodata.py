import json
import time
from typing import List, Tuple, cast, Callable

import polyline
import requests

from .joblib import memory


class _QueryTopo:
    _last_query: float = 0

    def __call__(self) -> Callable[[List[Tuple[float, float]]], List[float]]:
        @memory.cache
        def impl(data: List[Tuple[float, float]]) -> List[float]:
            encoded_line = polyline.encode(data, 5)

            if time.time() - self._last_query < 1:
                time.sleep(1 - (time.time() - self._last_query))
            result = requests.get(f'https://api.opentopodata.org/v1/srtm90m?locations={encoded_line}')
            self._last_query = time.time()
            if result.status_code != 200:
                raise Exception(f'Error accessing opentopodata: {result.content!r}')
            points = json.loads(result.content)['results']
            return list(map(lambda p: cast(float, p['elevation']), points))

        return cast(Callable[[List[Tuple[float, float]]], List[float]], impl)


query_topo = _QueryTopo()()
