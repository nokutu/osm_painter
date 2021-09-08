from osm_painter.model.query import AreaQuery, WayQuery
from .query_layer import QueryLayer
from .elevation_layer import ElevationLayer


class Layers:
    building_layer = QueryLayer('building', AreaQuery('["building"]'))
    highway_layer = QueryLayer('highway', WayQuery('["highway"]'))
    elevation_layer = ElevationLayer('elevation')
    landuse_layer = QueryLayer('landuse', AreaQuery('["landuse"]'))
    leisure_layer = QueryLayer('leisure', AreaQuery('["leisure"]'))
    water_layer = QueryLayer('water', AreaQuery('["water"]'))
    waterway_layer = QueryLayer('waterway', WayQuery('["waterway"]'))
