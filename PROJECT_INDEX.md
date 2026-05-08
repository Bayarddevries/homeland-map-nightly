# Homeland Map — Project Index

**Version:** 5.1 — Merged desktop + v5 improvements, May 1, 2026
**Status:** Active
**Related project:** West and Back RPG (`~/projects/west-and-back/`)

---

## Folder Structure

```
homeland-map/
├── PROJECT_INDEX.md           ← This file
├── SPEC.md                   ← Map specification / layer config
├── index.html                ← Main app (Leaflet.js)
├── css/
│   └── style.css             ← Map overlay, legend, popup styling
├── js/
│   ├── main.js               ← Map init, tile providers, layer setup
│   ├── main-embedded.js      ← Embedded data variant
│   └── data.js               ← Compiled GeoJSON (41 waterways, 43 trails, 229 locations)
├── data/
│   ├── waterways.geojson     ← 41 waterway segments (source: west-and-back reference)
│   ├── waterways_compact.json
│   ├── cart-trails.geojson   ← 43 trail segments (source: west-and-back reference)
│   ├── cart-trails_compact.json
│   ├── locations.geojson     ← 229 settlement points (source: west-and-back reference)
│   └── locations_compact.json
├── lib/                      ← Leaflet.js (local copy for file:// compatibility)
├── scripts/
│   ├── convert_kml.py        ← KML/KMZ → GeoJSON converter
│   └── convert_csv.py        ← CSV → GeoJSON converter
├── mechanics/
│   └── layers/               ← Map layer configs (colors, styles, popup templates)
├── reference/
│   ├── source-data/          ← Notes on source files
│   └── art/                  ← Palette, design mockups
├── serve.py                  ← Local server (CORS, MIME types, WSL IP detection)
├── start.bat                 ← Windows launcher
└── start_server.sh           ← Unix launcher
```

---

## What's in the Map

| Layer | Count | Source | Style |
|---|---|---|---|
| Waterways | 41 segments | Waterways.kmz → west-and-back reference | Blue lines |
| Cart Trails | 43 segments | Cart Trails.kmz → west-and-back reference | Red dashed lines |
| Locations | 229 points | Locations.csv → west-and-back reference | Green markers |

**Total features: 313**

### Tile Providers (in priority order)
1. CartoDB Positron (primary) — light basemap, very permissive, almost never 403s
2. CartoDB Dark Matter (alternate)
3. OpenStreetMap (fallback)

---

## How to Run

```bash
# From project root
python3 serve.py 8000
# Then open http://localhost:8000 (WSL) or http://<WSL-IP>:8000 (Windows)
```

Or use `start.bat` (Windows) or `start_server.sh` (Unix).

---

## Data Update Workflow

When west-and-back reference data is updated:

```bash
# 1. Convert new KML/KMZ
python3 scripts/convert_kml.py ../west-and-back/Game\ Data/reference/data/cart_trails.kml data/cart-trails.geojson

# 2. Convert new CSV
python3 scripts/convert_csv.py ../west-and-back/Game\ Data/reference/data/settlements_locations.csv data/locations.geojson

# 3. Recompile data.js (if using embedded mode)
# Edit js/data.js with the new GeoJSON content

# 4. Refresh browser
```

---

## Relationship to West and Back RPG

The homeland-map visualizes the same geographic data that the West and Back RPG uses:

- **Source files**: `~/projects/west-and-back/Game Data/reference/data/`
- **cart_trails.kml** → processed to `data/cart-trails.geojson`
- **settlements_locations.csv** → processed to `data/locations.geojson`
- **Waterways.kmz** → processed to `data/waterways.geojson`

When the west-and-back data is updated, re-run the conversion scripts above and commit both the source and the processed geo data.

---

## Active Issues

- V6 feature planning: KMZ upload in browser, drawing tools, Google Earth export
- Layer style review: marker colors/icons for community types not yet differentiated
- data.js embedded format: 704KB inline — consider lazy loading for production
- No mobile-optimized popup layout yet

---

## Next Steps

1. Layer style differentiation by community type (HBC Fort vs. Métis settlement vs. Trading Post)
2. Add timeline slider for historical date filtering
3. Link clickable locations to West and Back CHARACTERS.md entries
4. V6: browser-based KMZ upload tool