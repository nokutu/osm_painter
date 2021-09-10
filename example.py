import matplotlib.pyplot as plt

from osm_painter import draw, Layers, RadiusLocation

fig, ax = plt.subplots(figsize=(15, 12), constrained_layout=True)

draw(ax, RadiusLocation((38.54200, -1.95335), 1000),
     [
         Layers.highway_layer,
         Layers.building_layer,
         Layers.landuse_layer,
         Layers.waterway_layer,
         Layers.leisure_layer,
         Layers.elevation_layer,
         Layers.water_layer
     ], style={
        'highway': {
            'primary': {'lw': 4.5, 'color': '#011627'},
            'secondary': {'lw': 4, 'color': '#011627'},
            'tertiary': {'lw': 3.5, 'color': '#011627'},
            'residential': {'lw': 3, 'color': '#011627'},
            'unclassified': {'lw': 3, 'color': '#011627'},
            'path': {'lw': 1, 'color': '#011627'},
            'track': {'lw': 1, 'color': '#011627'},
            'footway': {'lw': 1, 'color': '#011627'},
        },
        'building': {
            'default': {'fc': '#6B0504', 'ec': '#2F3737', 'lw': 0, 'zorder': 2},
        },
        'landuse': {
            'cemetery': {'color': '#948e8e', 'lw': 1, 'zorder': -2},
            'forest': {'color': '#80FF72', 'lw': 0, 'zorder': -2},
            'grass': {'color': '#80FF72', 'lw': 0, 'zorder': -2}
        },
        'waterway': {
            'river': {'color': '#20A4F3', 'lw': 4, 'zorder': -1},
            'default': {'color': '#20A4F3', 'lw': 1, 'zorder': -1},
        },
        'water': {
            'default': {'color': '#20A4F3', 'lw': 0, 'zorder': -1},
        },
        'leisure': {
            'park': {'color': '#80FF72', 'lw': 0, 'zorder': -2}
        },
        'elevation': {
            'default': {'color': plt.get_cmap('viridis'), 'lw': 2, 'zorder': -3}
        },
        'perimeter': {
            'default': {
                'lw': 2,
                'fc': '#011627',
                'zorder': 10
            }
        },
        'background': {
            'default': {
                'zorder': -10,
                'fc': '#F6F7F8',
                'ec': '#E8EBED',
                'hatch': 'ooo...'
            }
        }}
     )

plt.savefig('out.svg')
plt.show()
