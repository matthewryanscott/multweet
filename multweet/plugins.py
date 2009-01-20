from pkg_resources import iter_entry_points


PLUGINS = dict(
    (entry_point.name, entry_point.load())
    for entry_point
    in iter_entry_points('multweet')
)

for name, plugin in PLUGINS.items():
    plugin.name = name
