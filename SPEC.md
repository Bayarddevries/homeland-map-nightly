# Homeland Map — Specification

## Overview

Interactive Leaflet.js map of the Métis homeland, showing waterways, cart trails, and 229 historical settlements. Built as a standalone HTML file with no backend required.

## Tech Stack

- **Map**: Leaflet.js 1.9.4 (local copy in `lib/`)
- **Basemap**: CartoDB Positron → OpenStreetMap fallback chain
- **Data**: GeoJSON, compiled into `js/data.js` or loaded from `data/*.geojson`
- **Server**: Python `serve.py` with CORS headers for cross-origin tile loading

## Layers

1. **Waterways** — 41 river/waterway segments, blue lines
2. **Cart Trails** — 43 Red River cart trail segments, red dashed lines
3. **Locations** — 229 settlement points, green markers with popups

## Popup Fields (Locations)

- Name
- Description
- Founded (year)
- Community Type (HBC Fort, Trading Post, Métis Community, Settlement)

## Tile Fallback Chain

CartoDB Light → CartoDB Dark → OpenStreetMap

On tile error, automatically falls through the chain. Each provider tracks its own failure count so one bad tile doesn't block the chain.

## File Descriptions

| File | Purpose |
|---|---|
| `index.html` | App shell — loads Leaflet, CSS, JS |
| `js/main.js` | Map init, tile chain, layer setup, event handlers |
| `js/main-embedded.js` | Variant with data embedded inline |
| `js/data.js` | Compiled GeoJSON (704KB, all three layers) |
| `data/*.geojson` | Individual layer files (readable source) |
| `data/*_compact.json` | Minified variants for production |
| `css/style.css` | Overlay, legend, popup styling |
| `lib/leaflet.css` + `lib/leaflet.js` | Leaflet distribution (local) |
| `serve.py` | HTTP server with CORS, MIME types, WSL IP detection |

## Planned Enhancements (V6)

- [ ] KMZ/KML upload directly in browser
- [ ] Drawing/shape tools (polygon, line, point)
- [ ] Google Earth export
- [ ] Location type color-coding in markers
- [ ] Historical date slider / timeline view
- [ ] Search and filter by community type
- [ ] Link locations to West and Back CHARACTERS.md entries

## V5 Completion Notes

- All 313 features render correctly
- Layer toggles work
- Popups display correctly
- Mobile responsive
- No API keys required