# Homeland Map V5 - Deployment Guide

## Quick Deploy (Local Testing)

```bash
cd homeland-map-v5
python3 serve.py 8000
# Open http://localhost:8000 in browser
```

## Production Deployment

### Option 1: Static Hosting (Recommended)
The map is a static site - deploy to any static hosting:

- **GitHub Pages**: Push to `gh-pages` branch
- **Netlify**: Drag & drop folder or connect Git repo
- **Vercel**: Import Git repository
- **Cloudflare Pages**: Connect Git repo

### Option 2: Self-Hosted
1. Copy entire `homeland-map-v5/` directory to web server
2. Configure web server to serve `index.html`
3. Ensure all files are accessible

## Data Update Workflow

### From Google Earth (Future V6)
1. Draw shapes in Google Earth
2. Export as KMZ/KML
3. Run: `python3 scripts/convert_kml.py new_data.kmz data/waterways.geojson`
4. Refresh browser

### From CSV
1. Update CSV with new locations
2. Run: `python3 scripts/convert_csv.py locations.csv data/locations.geojson`
3. Refresh browser

## File Checklist
- [x] `index.html` - Main page
- [x] `css/style.css` - Styling
- [x] `js/main.js` - Map logic
- [x] `data/waterways.geojson` - 41 waterway segments
- [x] `data/cart-trails.geojson` - 43 trail segments
- [x] `data/locations.geojson` - 229 locations
- [x] `scripts/convert_kml.py` - KML converter
- [x] `scripts/convert_csv.py` - CSV converter
- [x] `serve.py` - Local dev server
- [x] `README.md` - Documentation

## Browser Compatibility
- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers (responsive design)

## Performance Notes
- All data loads client-side (no backend required)
- GeoJSON files are ~200KB total
- Leaflet.js loads from CDN
- OpenStreetMap tiles load from OSM CDN
