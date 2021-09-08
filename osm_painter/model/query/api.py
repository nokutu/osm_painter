import overpy

from osm_painter.utils.joblib import memory

overpy_api = overpy.Overpass(url='https://overpass.openstreetmap.fr/api/interpreter')
overpy_api.query = memory.cache(overpy_api.query)
