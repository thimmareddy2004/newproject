# Bikes dataset for bike rentals page
try:
    from data.bikes import BIKES
except Exception:
    BIKES = []
from flask import Flask, redirect, render_template, request, jsonify, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ---------- START: your original app code (unchanged) ----------
app = Flask(__name__)

# Use environment variables for production
import os
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# Database configuration with environment variable support
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///userlogins.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class LoginTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    login_time = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='logins')

# Create tables on app startup
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<page>.html')
def render_template_page(page):
    """Render a template that lives in the templates folder when requested as '/name.html'.
    This is intentionally narrow (requires the .html suffix) so it doesn't accidentally
    capture named routes like /auth or /packages which should be registered explicitly.
    """
    try:
        return render_template(f"{page}.html")
    except Exception:
        # If rendering fails (missing template etc), fall back to auth page
        return redirect('/auth')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/logout')
def logout():
    try:
        session.clear()
    except Exception:
        pass
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth'))


# Explicit services route (render services page)
@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/fuel-calculator')
def fuel_calculator():
    return render_template('fuel_calculator.html')

@app.route('/rentals')
def rentals():
    return render_template('rentals.html')

@app.route('/taxi-rental')
def taxi_rental():
    return render_template('taxi_rental.html')

@app.route('/packages')
def packages():
    return render_template('packages.html')

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.form
        email = data.get('email')
        if not email:
            flash("Email is required!", "error")
            return redirect(url_for('auth'))
        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "error")
            return redirect(url_for('auth'))
        user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=email,
            phone=data.get('phone', ''),
        )
        user.set_password(data.get('password'))
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully! Please sign in.", "success")
        return redirect(url_for('auth'))
    except Exception as e:
        print("Signup error:", e)
        flash("Error during signup!", "error")
        return redirect(url_for('auth'))

@app.route('/signin', methods=['POST'])
def signin():
    data = request.form
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        # Record login event
        login_entry = LoginTracking(user_id=user.id)
        db.session.add(login_entry)
        db.session.commit()
        session['user_id'] = user.id
        session['user_email'] = user.email
        return redirect(url_for('home'))
    flash("Invalid email or password!", "error")
    return redirect(url_for('auth'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    # Fetch all logins with user info ordered by login_time desc
    logins = LoginTracking.query.join(User).order_by(LoginTracking.login_time.desc()).all()
    return render_template('admin.html', logins=logins)
# ---------- END: your original app code (unchanged) ----------


# ------------------ MAP CODE APPENDED BELOW ------------------
# (This section is added but does NOT change any of the original logic above.)

# Additional imports needed by the map code
import json
from pathlib import Path
from datetime import timedelta
import requests

# Fuel calculator integration
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'microservices'))
try:
    from microservices.fuel_api import integrate_fuel_calculator
    FUEL_CALCULATOR_AVAILABLE = True
except ImportError as e:
    print(f"Fuel calculator import failed: {e}")
    FUEL_CALCULATOR_AVAILABLE = False

# GeoJSON cache configuration (creates data/ folder in project root)
APP_ROOT = Path(__file__).parent
DATA_DIR = APP_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
GEOJSON_CACHE = DATA_DIR / "karnataka_districts.json"
# upstream GeoJSON - replace with your own if needed
GEOJSON_SRC = "https://raw.githubusercontent.com/civictech-India/INDIA-GEO-JSON-Datasets/main/Karnataka_District_Boundary.json"
GEOJSON_CACHE_TTL = timedelta(days=7)

def geojson_cache_is_stale() -> bool:
    if not GEOJSON_CACHE.exists():
        return True
    mtime = datetime.fromtimestamp(GEOJSON_CACHE.stat().st_mtime)
    return datetime.utcnow() - mtime > GEOJSON_CACHE_TTL

def fetch_and_cache_geojson() -> dict:
    """
    Fetch GeoJSON from remote source and cache locally.
    Returns parsed JSON.
    """
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

@app.route("/geojson")
def geojson():
    """
    Serve cached copy of Karnataka districts GeoJSON.
    If cache is missing or stale, fetch upstream.
    """
    try:
        if geojson_cache_is_stale():
            gj = fetch_and_cache_geojson()
        else:
            with GEOJSON_CACHE.open("r", encoding="utf-8") as fh:
                gj = json.load(fh)
        return jsonify(gj)
    except Exception as e:
        return jsonify({"error": "failed to load geojson", "details": str(e)}), 500

@app.route("/api/cities")
def cities():
    """Demo city markers used by the client map page."""
    demo = [
        {"id": "bengaluru", "name": "Bengaluru", "lat": 12.9716, "lng": 77.5946},
        {"id": "mysuru", "name": "Mysuru", "lat": 12.2958, "lng": 76.6394},
        {"id": "mangaluru", "name": "Mangaluru", "lat": 12.9141, "lng": 74.8560},
        {"id": "hubli", "name": "Hubli-Dharwad", "lat": 15.3647, "lng": 75.1234},
    ]
    return jsonify(demo)

# Annotations endpoints (save/delist drawn GeoJSON)
ANNOTATIONS_DIR = DATA_DIR / "annotations"
ANNOTATIONS_DIR.mkdir(exist_ok=True)

@app.route("/api/annotations", methods=["POST", "GET"])
def annotations():
    """
    POST: accept GeoJSON from client (drawn shapes/markers) and save as file.
          expects JSON body { "name": "...", "geojson": {...} }
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

@app.route("/maps")
def maps():
    """
    Render the interactive map page. This function always provides the
    full config dict expected by the template so Jinja doesn't produce
    Undefined values (which would break tojson()).
    """
    cfg = {
        # Map view defaults
        "map_center": [13.0, 76.0],
        "map_zoom": 6,

        # Backend endpoints used by the client. Ensure these routes exist in app.py
        # If you didn't add /geojson, /geocode, /route, /api/cities or /api/annotations,
        # either implement them or change these strings to the proper endpoints.
        "geojson_url": "/geojson",
        "geocode_url": "/geocode",
        "route_url": "/route",
        "cities_url": "/api/cities",
        "save_annotations_url": "/api/annotations"
    }

    # Optional: helpful debug if you want to verify what's being passed
    # print("Rendering map with cfg:", cfg)

    return render_template("map.html", **cfg)

@app.route('/transport')
def transport():
    # this renders templates/transport.html — make sure that file exists
    return render_template('transport.html')

@app.route('/bike-rental')
def bike_rental():
    """Render the Bike Rentals page with dataset from data/bikes.py."""
    return render_template('bike_rental_v2.html', bikes=BIKES)

@app.route('/api/bikes')
def api_bikes():
    """Return bikes as JSON formatted for the booking page cards."""
    def slugify(text: str) -> str:
        import re
        return re.sub(r'-{2,}', '-', re.sub(r'[^a-z0-9]+', '-', (text or '').lower())).strip('-')

    items = []
    for b in BIKES:
        items.append({
            "id": slugify(b.get("name", "")),
            "name": b.get("name"),
            "type": b.get("type"),
            "capacity": int(str(b.get("capacity", "2")).split()[0] or 2),
            "image": f"/static/bikes/{b.get('image')}",
            "features": b.get("features", []),
            # Use price_per_km for both local/outstation to keep UI consistent
            "localRate": b.get("price_per_km", "₹0"),
            "outstationRate": b.get("price_per_km", "₹0"),
            "rating": b.get("rating", 4.6),
            "description": b.get("blurb", "")
        })
    return jsonify(items)

@app.route("/admin/refresh-geojson", methods=["POST"])
def refresh_geojson():
    """
    Admin helper to force refresh geojson cache (protect in prod!).
    """
    try:
        gj = fetch_and_cache_geojson()
        return jsonify({"ok": True, "features": len(gj.get("features", []))})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# ------------------ END APP.PY ------------------

if __name__ == '__main__':
    app.run(debug=True)
# --- append to app.py (keep all original routes unchanged) ---
import os
from flask import current_app
import requests
from urllib.parse import urlencode

ORS_API_KEY = os.environ.get("ORS_API_KEY")  # set this in environment before running

# Simple server-side geocode proxy (uses Nominatim). We proxy so browser doesn't hit rate limits / CORS.
# Query param: q (the address string). Returns list of place objects from Nominatim.
@app.route("/geocode")
def geocode():
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
        r = requests.get(url, headers={"User-Agent": "my-flask-app/1.0"}, timeout=10)
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


# Route planning proxy to OpenRouteService Directions API
# POST JSON body: {"profile":"driving-car"|"cycling-regular"|"foot-walking", "coordinates":[ [lon,lat], [lon,lat] ], "alternatives": 3}
@app.route("/route", methods=["POST"])
def route():
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

        # Return ORS response directly to client (GeoJSON features contain summary/distance/duration)
        return jsonify(resp_json)
    except requests.HTTPError as he:
        return jsonify({"error": "Upstream ORS error", "details": he.response.text}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# --- end appended code ---

# Import send_from_directory for favicon handling
from flask import send_from_directory

# ---------- Package models for travel packages ----------
class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)
    seasons = db.Column(db.String(255))  # comma-separated seasons (monsoon,summer,winter)
    categories = db.Column(db.String(255))  # comma-separated categories
    image_urls = db.Column(db.Text)  # JSON list of image urls (stringified)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    places = db.relationship('PackagePlace', back_populates='package', cascade='all, delete-orphan')

class PackagePlace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    place_id = db.Column(db.String(200), nullable=False)  # matches the `id` field in your places JSON
    sort_order = db.Column(db.Integer, default=0)

    package = db.relationship('Package', back_populates='places')

# Add favicon route to prevent 404 errors
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 
                              'favicon.ico', mimetype='image/vnd.microsoft.icon')

# ---------- Package & API routes ----------

# Serve places dataset (the map & the packages page will call this)
# Make sure you saved your places JSON at static/data/karnataka_places.json
@app.route('/api/places')
def api_places():
    data_path = os.path.join(app.static_folder, 'data', 'karnataka_places.json')
    if not os.path.exists(data_path):
        # fallback to an embedded smaller sample to avoid 404 if file missing
        sample = [
            {"id":"bengaluru","name":"Bengaluru (Bangalore)","lat":12.9716,"lon":77.5946,"categories":["city","historical","temple","park"],"seasons":["winter","summer"],"short_desc":"Capital city — parks, tech, temples, museums."}
        ]
        return jsonify(sample)
    with open(data_path, 'r', encoding='utf-8') as f:
        places = json.load(f)
    return jsonify(places)

# Package listing page (defined earlier in core routes)

# Page: create new package (shows map + place selection UI)
@app.route('/packages/new')
def packages_new():
    # frontend will fetch /api/places
    return render_template('packages.html')

# API: create package (POST)
@app.route('/packages/create', methods=['POST'])
def packages_create():
    try:
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        price = float(data.get('price') or 0.0)
        seasons = data.get('seasons', [])  # list
        categories = data.get('categories', [])  # list
        image_urls = data.get('image_urls', [])  # list
        places_list = data.get('places', [])  # list of place ids in order

        if not name:
            return jsonify({"ok": False, "error": "Package name required"}), 400

        pkg = Package(
            name=name,
            description=description,
            price=price,
            seasons=",".join(seasons),
            categories=",".join(categories),
            image_urls=json.dumps(image_urls),
        )
        db.session.add(pkg)
        db.session.flush()  # get pkg.id

        # create PackagePlace rows in the given order
        for idx, pid in enumerate(places_list):
            pp = PackagePlace(package_id=pkg.id, place_id=str(pid), sort_order=idx)
            db.session.add(pp)

        db.session.commit()
        return jsonify({"ok": True, "package_id": pkg.id})
    except Exception as e:
        print("Error creating package:", e)
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500

# View a single package
@app.route('/packages/<int:package_id>')
def packages_view(package_id):
    pkg = Package.query.get_or_404(package_id)
    # decode images
    try:
        images = json.loads(pkg.image_urls or "[]")
    except Exception:
        images = []
    # For place details, we will load the static places JSON and match by id
    data_path = os.path.join(app.static_folder, 'data', 'karnataka_places.json')
    places_map = {}
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            places = json.load(f)
            for p in places:
                places_map[str(p.get('id'))] = p
    # build ordered list
    ordered = []
    for pp in sorted(pkg.places, key=lambda x: x.sort_order):
        pid = pp.place_id
        ordered.append(places_map.get(pid, {"id": pid, "name": pid}))
    return render_template('packages_view.html', package=pkg, images=images, places=ordered)

# Static route to allow direct image files if needed (optional)
@app.route('/static/images/<path:filename>')
def static_images(filename):
    from flask import send_from_directory
    return send_from_directory(os.path.join(app.static_folder, 'images'), filename)

# Fuel Calculator API Routes (Direct Integration)
@app.route('/api/fuel/detailed-calculation', methods=['POST'])
def fuel_detailed_calculation():
    """Detailed fuel cost calculation with breakdown"""
    try:
        from microservices.fuel_calculator import IndiaFuelCalculator
        
        data = request.get_json()
        distance = float(data.get('distance_km', 0))
        vehicle_key = data.get('vehicle_key', 'hatchback_petrol')
        location = data.get('location', 'karnataka')
        city_percentage = float(data.get('city_percentage', 30))
        road_condition = data.get('road_condition', 'good_highway')
        
        if distance <= 0:
            return jsonify({"error": "Distance must be greater than 0"}), 400
        
        calculator = IndiaFuelCalculator(location)
        result = calculator.calculate_fuel_cost(
            distance, vehicle_key, city_percentage, road_condition
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fuel/compare-vehicles', methods=['POST'])
def fuel_compare_vehicles():
    """Compare fuel costs across different vehicles"""
    try:
        from microservices.fuel_calculator import IndiaFuelCalculator
        
        data = request.get_json()
        distance = float(data.get('distance_km', 0))
        vehicle_keys = data.get('vehicle_keys', ['hatchback_petrol', 'hatchback_diesel', 'bike_150cc'])
        location = data.get('location', 'karnataka')
        
        if distance <= 0:
            return jsonify({"error": "Distance must be greater than 0"}), 400
        
        calculator = IndiaFuelCalculator(location)
        result = calculator.compare_vehicles(distance, vehicle_keys)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fuel/vehicles', methods=['GET'])
def fuel_get_vehicles():
    """Get list of available vehicles"""
    try:
        from microservices.fuel_calculator import IndiaFuelCalculator
        
        calculator = IndiaFuelCalculator()
        vehicles = calculator.get_available_vehicles()
        
        return jsonify({
            "vehicles": vehicles,
            "total_count": len(vehicles)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/fuel/quick-estimate', methods=['POST'])
def fuel_quick_estimate():
    """Quick fuel cost estimate for distance and vehicle type"""
    try:
        from microservices.fuel_calculator import quick_fuel_cost
        
        data = request.get_json()
        distance = float(data.get('distance_km', 0))
        vehicle_type = data.get('vehicle_type', 'hatchback_petrol')
        location = data.get('location', 'karnataka')
        
        if distance <= 0:
            return jsonify({"error": "Distance must be greater than 0"}), 400
        
        cost = quick_fuel_cost(distance, vehicle_type, location)
        
        return jsonify({
            "distance_km": distance,
            "vehicle_type": vehicle_type,
            "location": location,
            "estimated_fuel_cost": cost,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

print("Fuel calculator API routes added successfully!")

# keep app run as before
if __name__ == '__main__':
    # Use environment variables for production deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
