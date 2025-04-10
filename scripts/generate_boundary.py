import json

# Coordenadas en sistema local (X, Y)
boundary_coords = [
    [0, 0],
    [20, 0],
    [20, 20],
    [0, 20],
    [0, 0]  # cerrar el polígono
]

geojson = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [boundary_coords]
        }
    }]
}

with open("boundary.geojson", "w") as f:
    json.dump(geojson, f, indent=2)

print("✅ boundary.geojson creado en coordenadas locales.")
