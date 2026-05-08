# Métis Homeland Map V5

An interactive web map displaying Métis homeland historical data including waterways, cart trails, and settlements/locations.

## Features

- **Waterways**: Historical river and waterway routes (blue lines)
- **Cart Trails**: Red River cart trail routes (red dashed lines)
- **Locations**: 229+ historical settlements, forts, and communities (green markers)
- **Layer Controls**: Toggle visibility of each data type
- **Interactive Popups**: Click on features to see details

## Quick Start

1. Open `index.html` in a web browser
2. Or serve via local server: `python3 -m http.server 8000`
3. Navigate to `http://localhost:8000`

## Data Sources

### Current Data (V5)
- `data/waterways.geojson` - 41 waterway segments (converted from Waterways.kmz)
- `data/cart-trails.geojson` - 43 cart trail segments (converted from Cart Trails.kmz)
- `data/locations.geojson` - 229 locations (converted from Locations.csv)

### Updating Data

#### From Google Earth (KMZ/KML)
1. Draw shapes in Google Earth
2. Save/Export as KMZ or KML
3. Place in project root
4. Run conversion script:
```bash
python3 scripts/convert_kml.py waterways.kmz data/waterways.geojson
```

#### From CSV
1. Ensure CSV has columns: `Location Name`, `Latitude`, `Longitude`, `Description`, `Founded`, `Community Type`
2. Place in project root
3. Run conversion script:
```bash
python3 scripts/convert_csv.py locations.csv data/locations.geojson
```

## File Structure

```
homeland-map-v5/
├── index.html              # Main page
├── css/
│   └── style.css           # Styling
├── js/
│   └── main.js             # Map logic
├── data/
│   ├── waterways.geojson   # Waterway lines
│   ├── cart-trails.geojson # Cart trail lines
│   └── locations.geojson   # Location points
├── scripts/
│   ├── convert_kml.py      # KML to GeoJSON converter
│   └── convert_csv.py      # CSV to GeoJSON converter
└── README.md               # This file
```

## Technology Stack

- **Leaflet.js** - Interactive map library
- **OpenStreetMap** - Base map tiles
- **GeoJSON** - Data format
- Vanilla HTML/CSS/JavaScript (no build step required)

## Future Enhancements (V6+)

- [ ] KMZ/KML file upload and parsing in browser
- [ ] Shape drawing tools (polygon, line)
- [ ] Admin interface for data management
- [ ] Export functionality
- [ ] Search/filter locations
- [ ] Timeline view for historical changes
- [ ] Story integration with location narratives

## Development

### Running Locally
```bash
cd homeland-map-v5
python3 -m http.server 8000
# Open http://localhost:8000
```

### Adding New Data
1. Convert source data to GeoJSON
2. Place in `data/` directory
3. Update `js/main.js` to load new layer
4. Add to layer control

## License

This project is for the Métis Homeland community.
