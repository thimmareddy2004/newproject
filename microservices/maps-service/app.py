import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify
from shared.config import config
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import urlencode

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    return app

app = create_app()

# GeoJSON cache configuration
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
GEOJSON_CACHE = DATA_DIR / "karnataka_districts.json"
GEOJSON_SRC = "https://raw.githubusercontent.com/civictech-India/INDIA-GEO-JSON-Datasets/main/Karnataka_District_Boundary.json"
GEOJSON_CACHE_TTL = timedelta(days=7)

# Annotations directory
ANNOTATIONS_DIR = DATA_DIR / "annotations"
ANNOTATIONS_DIR.mkdir(exist_ok=True)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "maps-service"})

def geojson_cache_is_stale() -> bool:
    """Check if GeoJSON cache is stale"""
    if not GEOJSON_CACHE.exists():
        return True
    mtime = datetime.fromtimestamp(GEOJSON_CACHE.stat().st_mtime)
    return datetime.utcnow() - mtime > GEOJSON_CACHE_TTL

def fetch_and_cache_geojson() -> dict:
    """Fetch GeoJSON from remote source and cache locally"""
    try:
        resp = requests.get(GEOJSON_SRC, timeout=20)
        resp.raise_for_status()
        gj = resp.json()
        with GEOJSON_CACHE.open("w", encoding="utf-8") as fh:
            json.dump(gj, fh)
        return gj
    except Exception as e:
        # fallback to existing cache if network fails
        if GEOJSON_CACHE.exists():
            with GEOJSON_CACHE.open("r", encoding="utf-8") as fh:
                return json.load(fh)
        raise

@app.route("/geojson", methods=['GET'])
def geojson():
    """Serve cached copy of Karnataka districts GeoJSON"""
    try:
        if geojson_cache_is_stale():
            gj = fetch_and_cache_geojson()
        else:
            with GEOJSON_CACHE.open("r", encoding="utf-8") as fh:
                gj = json.load(fh)
        return jsonify(gj)
    except Exception as e:
        return jsonify({"error": "failed to load geojson", "details": str(e)}), 500

@app.route("/api/cities", methods=['GET'])
def cities():
    """Demo city markers"""
    demo = [
        {"id": "bengaluru", "name": "Bengaluru", "lat": 12.9716, "lng": 77.5946},
        {"id": "mysuru", "name": "Mysuru", "lat": 12.2958, "lng": 76.6394},
        {"id": "mangaluru", "name": "Mangaluru", "lat": 12.9141, "lng": 74.8560},
        {"id": "hubli", "name": "Hubli-Dharwad", "lat": 15.3647, "lng": 75.1234},
    ]
    return jsonify(demo)

@app.route("/geocode", methods=['GET'])
def geocode():
    """Geocoding service using Nominatim"""
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify([])

    # Nominatim search
    params = {
        "q": q,
        "format": "json",
        "addressdetails": 1,
        "limit": 8,
    }
    url = "https://nominatim.openstreetmap.org/search?" + urlencode(params)
    try:
        r = requests.get(url, headers={"User-Agent": "goaround-maps-service/1.0"}, timeout=10)
        r.raise_for_status()
        results = r.json()
        
        # normalize fields
        out = []
        for item in results:
            out.append({
                "display_name": item.get("display_name"),
                "lat": float(item.get("lat")),
                "lon": float(item.get("lon")),
                "type": item.get("type"),
                "address": item.get("address", {})
            })
        return jsonify(out)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/route", methods=['POST'])
def route():
    """Route planning using OpenRouteService"""
    ORS_API_KEY = app.config.get('ORS_API_KEY')
    if not ORS_API_KEY:
        return jsonify({"error": "ORS_API_KEY not configured on server"}), 500

    try:
        body = request.get_json(force=True)
        profile = body.get("profile", "driving-car")
        coords = body.get("coordinates")  # [[lon,lat], [lon,lat]]
        alternatives = int(body.get("alternatives", 1))

        if not coords or len(coords) < 2:
            return jsonify({"error": "coordinates (two points) required"}), 400

        ors_url = f"https://api.openrouteservice.org/v2/directions/{profile}/geojson"

        # Build request payload; ask for alternative routes
        payload = {
            "coordinates": coords,
            "instructions": False,
            "geometry": True,
            "units": "m",
            "language": "en",
            "options": {
                "alternative_routes": {
                    "target_count": alternatives,
                    "share_factor": 0.6,
                    "weight_factor": 2
                }
            }
        }

        headers = {
            "Authorization": ORS_API_KEY,
            "Content-Type": "application/json"
        }

        r = requests.post(ors_url, headers=headers, json=payload, timeout=20)
        r.raise_for_status()
        resp_json = r.json()

        # Return ORS response directly to client
        return jsonify(resp_json)
    except requests.HTTPError as he:
        return jsonify({"error": "Upstream ORS error", "details": he.response.text}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/annotations", methods=["POST", "GET"])
def annotations():
    """
    POST: accept GeoJSON from client (drawn shapes/markers) and save as file.
    GET: list saved annotation files (metadata).
    """
    if request.method == "GET":
        files = []
        for p in sorted(ANNOTATIONS_DIR.glob("*.json")):
            files.append({
                "file": p.name,
                "mtime": p.stat().st_mtime,
                "size": p.stat().st_size
            })
        return jsonify(files)

    # POST
    try:
        body = request.get_json(force=True)
        if not body or "geojson" not in body:
            return ("JSON body with 'geojson' key required", 400)

        name = body.get("name") or f"annotation-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        safe_name = "".join(c for c in name if c.isalnum() or c in ("-", "_"))[:60]
        out_file = ANNOTATIONS_DIR / f"{safe_name}.json"

        payload = {
            "name": name,
            "saved_at": datetime.utcnow().isoformat() + "Z",
            "client_info": {
                "ip": request.remote_addr,
                "user_agent": request.headers.get("User-Agent")
            },
            "geojson": body["geojson"]
        }
        with out_file.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)

        return jsonify({"ok": True, "file": out_file.name}), 201
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/admin/refresh-geojson", methods=["POST"])
def refresh_geojson():
    """Admin helper to force refresh geojson cache"""
    try:
        gj = fetch_and_cache_geojson()
        return jsonify({"ok": True, "features": len(gj.get("features", []))})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/config", methods=['GET'])
def map_config():
    """Return map configuration for frontend"""
    cfg = {
        # Map view defaults
        "map_center": [13.0, 76.0],
        "map_zoom": 6,
        
        # Backend endpoints
        "geojson_url": "/geojson",
        "geocode_url": "/geocode",
        "route_url": "/route",
        "cities_url": "/api/cities",
        "save_annotations_url": "/api/annotations"
    }
    return jsonify(cfg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)