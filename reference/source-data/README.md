# Source Data — Homeland Map

The geo data in `../data/` is derived from the west-and-back RPG reference data.

## Source Files (west-and-back)

| File | Produced | Used for layer |
|---|---|---|
| `~/projects/west-and-back/Game Data/reference/data/cart_trails.kml` | Historical | Cart Trails |
| `~/projects/west-and-back/Game Data/reference/data/settlements_locations.csv` | Historical | Locations |
| `~/projects/west-and-back/Game Data/reference/data/waterways.kml` | Historical | Waterways |

## Conversion Scripts

- `scripts/convert_kml.py` — KML/KMZ → GeoJSON (for trails and waterways)
- `scripts/convert_csv.py` — CSV → GeoJSON (for locations)

## Update Process

1. Make changes to source files in west-and-back
2. Re-run conversion scripts
3. Commit updated geo data to this project
4. Commit source data changes to west-and-back

**Do not edit geo data files directly** — they are generated from source.