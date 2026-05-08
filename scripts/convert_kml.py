#!/usr/bin/env python3
"""
Convert KML/KMZ files to GeoJSON for the Homeland Map.
Supports both .kml and .kmz (compressed KML) files.

Usage:
    python3 scripts/convert_kml.py input.kmz output.geojson
    python3 scripts/convert_kml.py input.kml output.geojson
"""

import json
import re
import sys
import zipfile
from pathlib import Path


def extract_kmz(kmz_path):
    """Extract KML from KMZ file"""
    with zipfile.ZipFile(kmz_path, 'r') as z:
        # Find the main KML file (usually doc.kml)
        kml_files = [f for f in z.namelist() if f.endswith('.kml')]
        if not kml_files:
            raise ValueError("No KML file found in KMZ")
        
        kml_content = z.read(kml_files[0])
        return kml_content.decode('utf-8')


def read_kml(kml_path):
    """Read KML file content"""
    with open(kml_path, 'r', encoding='utf-8') as f:
        return f.read()


def parse_kml(kml_content, feature_type=None):
    """Parse KML and extract LineStrings and Points"""
    features = []
    
    # Find all Placemark elements
    placemark_pattern = r'<Placemark>.*?</Placemark>'
    placemarks = re.findall(placemark_pattern, kml_content, re.DOTALL)
    
    for placemark in placemarks:
        # Extract name
        name_match = re.search(r'<name>(.*?)</name>', placemark)
        if not name_match:
            continue
        name = name_match.group(1).strip()
        
        # Check for LineString
        coords_match = re.search(r'<coordinates>(.*?)</coordinates>', placemark, re.DOTALL)
        if coords_match:
            coords_text = coords_match.group(1).strip()
            
            # Parse coordinates (lon,lat,alt pairs)
            coords = []
            for coord_pair in coords_text.split():
                parts = coord_pair.strip().split(',')
                if len(parts) >= 2:
                    try:
                        lon = float(parts[0])
                        lat = float(parts[1])
                        coords.append([lon, lat])
                    except ValueError:
                        continue
            
            if len(coords) >= 2:
                features.append({
                    "type": "Feature",
                    "properties": {
                        "name": name,
                        "type": feature_type or "unknown"
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coords
                    }
                })
        
        # Check for Point
        point_match = re.search(r'<Point>.*?</Point>', placemark, re.DOTALL)
        if point_match:
            point_coords = re.search(r'<coordinates>(.*?)</coordinates>', point_match.group(0))
            if point_coords:
                coords_text = point_coords.group(1).strip()
                parts = coords_text.split(',')
                if len(parts) >= 2:
                    try:
                        lon = float(parts[0])
                        lat = float(parts[1])
                        features.append({
                            "type": "Feature",
                            "properties": {
                                "name": name,
                                "type": feature_type or "point"
                            },
                            "geometry": {
                                "type": "Point",
                                "coordinates": [lon, lat]
                            }
                        })
                    except ValueError:
                        continue
    
    return {
        "type": "FeatureCollection",
        "features": features
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 convert_kml.py <input.kml|input.kmz> <output.geojson> [feature_type]")
        print("  feature_type: optional type label (default: 'unknown')")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    feature_type = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Read KML content
    if input_path.suffix.lower() == '.kmz':
        kml_content = extract_kmz(input_path)
    else:
        kml_content = read_kml(input_path)
    
    # Parse KML
    geojson = parse_kml(kml_content, feature_type)
    
    # Write GeoJSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Converted {len(geojson['features'])} features from {input_path} to {output_path}")


if __name__ == '__main__':
    main()
