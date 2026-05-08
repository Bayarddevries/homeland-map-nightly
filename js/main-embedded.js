// Homeland Map V5 - Data (embedded for file:// compatibility)
//
// Map tile configuration with automatic fallback chain.
// If the primary OSM tile server returns 403 (common with file:// access),
// the page automatically swaps to alternative tile providers.

// ---- Tile Provider Configuration ----
const TILE_PROVIDERS = [
    {
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19,
        subdomains: 'abc'
    },
    {
        url: 'https://tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM France</a>',
        maxZoom: 20,
        subdomains: 'abc'
    },
    {
        url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="https://opentopomap.org">OpenTopoMap</a>',
        maxZoom: 17,
        subdomains: 'abc'
    },
    {
        url: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
        maxZoom: 19,
        subdomains: 'abcd'
    }
];

// Map state
let map;
let currentTileLayer = null;
let currentProviderIndex = 0;
let waterwaysLayer;
let cartTrailsLayer;
let locationsLayer;

const layerState = {
    waterways: true,
    cartTrails: true,
    locations: true
};

// Embedded GeoJSON data
const waterwaysData = {type:"FeatureCollection",features:[]};
const cartTrailsData = {type:"FeatureCollection",features:[]};
const locationsData = {type:"FeatureCollection",features:[]};

// Load embedded data
try {
    const wData = JSON.parse({json.dumps(waterways).replace("'", "\\'")});
    const tData = JSON.parse({json.dumps(trails).replace("'", "\\'")});
    const lData = JSON.parse({json.dumps(locations).replace("'", "\\'")});
    Object.assign(waterwaysData, wData);
    Object.assign(cartTrailsData, tData);
    Object.assign(locationsData, lData);
} catch(e) {
    console.error("Error parsing embedded data:", e);
}

/**
 * Initialize the map
 */
function initMap() {
    map = L.map('map', {
        center: [52.0, -98.0],
        zoom: 6,
        minZoom: 4,
        maxZoom: 18
    });

    // Add primary tile layer with automatic error fallback
    addTileLayer(0);

    // Render data layers
    renderWaterways(waterwaysData);
    renderCartTrails(cartTrailsData);
    renderLocations(locationsData);
    addLayerControl();
}

/**
 * Add a tile layer with automatic fallback on error.
 */
function addTileLayer(providerIndex) {
    if (providerIndex >= TILE_PROVIDERS.length) {
        console.warn('All tile providers failed. Map will have no background.');
        return;
    }

    currentProviderIndex = providerIndex;
    const provider = TILE_PROVIDERS[providerIndex];

    if (currentTileLayer) {
        map.removeLayer(currentTileLayer);
    }

    console.log('Loading tiles from:', provider.url.split('/')[2]);

    currentTileLayer = L.tileLayer(provider.url, {
        attribution: provider.attribution,
        maxZoom: provider.maxZoom,
        subdomains: provider.subdomains || 'abc',
        detectRetina: true,
        errorTileUrl: ''
    });

    currentTileLayer.on('tileerror', function(event) {
        if (!window._tileFallbackAttempted) {
            window._tileFallbackAttempted = true;
            const nextIndex = currentProviderIndex + 1;
            console.warn('Tile error -> falling back to provider', nextIndex);
            if (nextIndex < TILE_PROVIDERS.length) {
                addTileLayer(nextIndex);
            }
        }
    });

    window._tileFallbackAttempted = false;
    currentTileLayer.addTo(map);
}

function renderWaterways(data) {
    waterwaysLayer = L.geoJSON(data, {
        style: {
            color: '#3498db',
            weight: 3,
            opacity: 0.7
        },
        onEachFeature: function(feature, layer) {
            if (feature.properties && feature.properties.name) {
                layer.bindPopup('<div class="popup-title">' + feature.properties.name + '</div><div class="popup-description">Waterway</div>');
            }
        }
    });
    if (layerState.waterways) waterwaysLayer.addTo(map);
}

function renderCartTrails(data) {
    cartTrailsLayer = L.geoJSON(data, {
        style: {
            color: '#e74c3c',
            weight: 4,
            opacity: 0.8,
            dashArray: '10, 10'
        },
        onEachFeature: function(feature, layer) {
            if (feature.properties && feature.properties.name) {
                layer.bindPopup('<div class="popup-title">' + feature.properties.name + '</div><div class="popup-description">Historic Cart Trail</div>');
            }
        }
    });
    if (layerState.cartTrails) cartTrailsLayer.addTo(map);
}

function renderLocations(data) {
    const locationIcon = L.divIcon({
        className: 'location-marker',
        html: '<div style="background-color: #27ae60; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>',
        iconSize: [12, 12],
        iconAnchor: [6, 6]
    });

    locationsLayer = L.geoJSON(data, {
        pointToLayer: function(feature, latlng) {
            return L.marker(latlng, { icon: locationIcon });
        },
        onEachFeature: function(feature, layer) {
            const props = feature.properties || {};
            let popupContent = '<div class="popup-title">' + (props.name || 'Unknown Location') + '</div>';
            if (props.description) {
                const desc = props.description.length > 200 ? props.description.substring(0, 200) + '...' : props.description;
                popupContent += '<div class="popup-description">' + desc + '</div>';
            }
            let metaInfo = [];
            if (props.founded && props.founded !== '#N/A' && props.founded !== '') {
                metaInfo.push('Founded: ' + props.founded);
            }
            if (props.community_type) {
                metaInfo.push(props.community_type);
            }
            if (metaInfo.length > 0) {
                popupContent += '<div class="popup-meta">' + metaInfo.join(' | ') + '</div>';
            }
            layer.bindPopup(popupContent);
        }
    });
    if (layerState.locations) locationsLayer.addTo(map);
}

function addLayerControl() {
    L.control.layers(null, {
        "Waterways": waterwaysLayer,
        "Cart Trails": cartTrailsLayer,
        "Locations": locationsLayer
    }, {
        position: 'topright',
        collapsed: false
    }).addTo(map);
}

document.addEventListener('DOMContentLoaded', initMap);