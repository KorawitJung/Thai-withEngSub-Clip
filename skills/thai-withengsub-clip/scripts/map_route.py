"""Fetch real roads, water and a bike route from OpenStreetMap for draw.route_map.

usage: map_route.py map_data.json --stop start,13.7567,100.5018 --stop end,13.7400,100.4985 [--margin 0.004]
Place each stop on a road, otherwise the route makes an out-and-back spur to reach it.
If the map server is down, roads already in the output file are kept and only the route is refreshed.
Credit the map as: © OpenStreetMap contributors. The route is computed, so have someone check it before recommending it.
"""
import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

OVERPASS = ("https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter")
ROUTER = "https://routing.openstreetmap.de/routed-bike/route/v1/bike/{}?overview=full&geometries=geojson"
FAILURES = (urllib.error.URLError, TimeoutError, ValueError)


def get(url, data=None):
    request = urllib.request.Request(url, data=data, headers={"User-Agent": "thai-withengsub-clip/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def parse_stop(text):
    key, lat, lon = text.rsplit(",", 2)
    return [key, float(lat), float(lon)]


def bounds(stops, margin):
    lats, lons = [s[1] for s in stops], [s[2] for s in stops]
    return [min(lats) - margin, min(lons) - margin, max(lats) + margin, max(lons) + margin]


def fetch_ways(box):
    area = ",".join(map(str, box))
    query = f"""[out:json][timeout:90];
(way["highway"~"^(primary|secondary|tertiary)$"]({area});
 way["waterway"="river"]({area});
 way["natural"="water"]({area}););
out geom;"""
    last = None
    for url in OVERPASS:
        try:
            return ways_from(get(url, urllib.parse.urlencode({"data": query}).encode()))
        except FAILURES as err:
            last = err
    raise ConnectionError(last)


def ways_from(osm):
    ways = []
    for element in osm["elements"]:
        tags = {key: value for key, value in element.get("tags", {}).items() if key in ("highway", "waterway", "natural")}
        if "geometry" in element:
            ways.append({"tags": tags, "pts": [[p["lat"], p["lon"]] for p in element["geometry"]]})
    return ways


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--stop", action="append", required=True, type=parse_stop, help="name,lat,lon in travel order")
    ap.add_argument("--margin", type=float, default=0.004)
    args = ap.parse_args()
    if len(args.stop) < 2:
        sys.exit("Give at least two stops")
    out = Path(args.out)
    old = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    try:
        ways = fetch_ways(bounds(args.stop, args.margin))
    except ConnectionError as err:
        if not old.get("ways"):
            sys.exit(f"Map server unavailable and no saved roads: {err}")
        print(f"Map server unavailable ({err}), keeping saved roads")
        ways = old["ways"]
    coords = ";".join(f"{lon},{lat}" for _, lat, lon in args.stop)
    try:
        route = get(ROUTER.format(coords))["routes"][0]
    except FAILURES as err:
        sys.exit(f"Route server unavailable: {err}")
    km = route["distance"] / 1000
    out.write_text(json.dumps({"stops": args.stop, "ways": ways, "route": route["geometry"]["coordinates"], "km": km}, ensure_ascii=False), encoding="utf-8")
    print(f"{len(ways)} ways, route {km:.2f} km, legs {[round(leg['distance']) for leg in route['legs']]} m")


if __name__ == "__main__":
    main()
