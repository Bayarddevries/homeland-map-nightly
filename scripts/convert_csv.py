#!/usr/bin/env python3
"""
Convert CSV files to GeoJSON for the Homeland Map.
Expects CSV with columns: Location Name, Latitude, Longitude, Description, Story, Founded, Community Type

Usage:
    python3 scripts/convert_csv.py input.csv output.geojson
"""

import json
import csv
import sys
from pathlib import Path


def parse_csv(csv_path):
    """Parse CSV and convert to GeoJSON"""
    features = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Parse latitude - handle "° N" or "° S" format
                lat_str = row.get('Latitude', '').strip().replace('°', '').replace('N', '').replace('S', '').strip()
                lon_str = row.get('Longitude', '').strip().replace('°', '').replace('E', '').replace('W', '').strip()
                
                # Handle negative coordinates
                lat = float(lat_str)
                lon = float(lon_str)
                if 'S' in row.get('Latitude', ''):
                    lat = -lat
                if 'W' in row.get('Longitude', ''):
                    lon = -lon
                
                # Clean up fields
                name = row.get('Location Name', '').strip()
                description = row.get('Description', '').strip()
                story = row.get('Story', '').strip()
                founded = row.get('Founded', '').strip()
                community_type = row.get('Community Type', '').strip()
                
                features.append({
                    "type": "Feature",
                    "properties": {
                        "name": name,
                        "description": description,
                        "story": story,
                        "founded": founded,
                        "community_type": community_type,
                        "type": "location"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    }
                })
            except Exception as e:
                print(f"Warning: Error parsing row: {e}")
                continue
    
    return {
        "type": "FeatureCollection",
        "features": features
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 convert_csv.py <input.csv> <output.geojson>")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    
    # Parse CSV
    geojson = parse_csv(input_path)
    
    # Write GeoJSON
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Converted {len(geojson['features'])} features from {input_path} to {output_path}")


if __name__ == '__main__':
    main()
