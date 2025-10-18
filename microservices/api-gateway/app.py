import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, send_from_directory
from shared.config import config
import requests
import json

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Set template and static folders to use original templates
    template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config[config_name])
    
    return app

app = create_app()

# Service URLs
AUTH_SERVICE_URL = app.config.get('AUTH_SERVICE_URL', 'http://localhost:5001')
PACKAGE_SERVICE_URL = app.config.get('PACKAGE_SERVICE_URL', 'http://localhost:5002')
MAPS_SERVICE_URL = app.config.get('MAPS_SERVICE_URL', 'http://localhost:5003')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "api-gateway"})

# ============= Frontend Routes =============

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

@app.route('/<page>.html')
def render_template_page(page):
    """Render template pages"""
    try:
        return render_template(f"{page}.html")
    except Exception:
        return redirect('/auth')

@app.route('/auth')
def auth():
    """Authentication page"""
    return render_template('auth.html')

@app.route('/home')
def home():
    """Home page after login"""
    return render_template('home.html')

@app.route('/services')
def services():
    """Services page"""
    return render_template('services.html')

@app.route('/transport')
def transport():
    """Transport page"""
    return render_template('transport.html')

@app.route('/packages')
def packages():
    """Packages listing page"""
    return render_template('packages.html')

@app.route('/packages/new')
def packages_new():
    """New package creation page"""
    return render_template('packages.html')

@app.route('/packages/<int:package_id>')
def packages_view(package_id):
    """View individual package"""
    try:
        # Get package details from package service
        response = requests.get(f"{PACKAGE_SERVICE_URL}/packages/{package_id}")
        if response.status_code == 404:
            flash("Package not found", "error")
            return redirect(url_for('packages'))
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                package = data.get('package')
                images = package.get('image_urls', [])
                places = package.get('places', [])
                return render_template('packages_view.html', package=package, images=images, places=places)
        
        flash("Error loading package", "error")
        return redirect(url_for('packages'))
        
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('packages'))

@app.route('/maps')
def maps():
    """Maps page"""
    try:
        # Get map configuration from maps service
        response = requests.get(f"{MAPS_SERVICE_URL}/config")
        cfg = response.json() if response.status_code == 200 else {
            "map_center": [13.0, 76.0],
            "map_zoom": 6,
            "geojson_url": f"{MAPS_SERVICE_URL}/geojson",
            "geocode_url": f"{MAPS_SERVICE_URL}/geocode",
            "route_url": f"{MAPS_SERVICE_URL}/route",
            "cities_url": f"{MAPS_SERVICE_URL}/api/cities",
            "save_annotations_url": f"{MAPS_SERVICE_URL}/api/annotations"
        }
        
        return render_template('map.html', **cfg)
    except Exception as e:
        # Fallback config
        cfg = {
            "map_center": [13.0, 76.0],
            "map_zoom": 6,
            "geojson_url": f"{MAPS_SERVICE_URL}/geojson",
            "geocode_url": f"{MAPS_SERVICE_URL}/geocode",
            "route_url": f"{MAPS_SERVICE_URL}/route",
            "cities_url": f"{MAPS_SERVICE_URL}/api/cities",
            "save_annotations_url": f"{MAPS_SERVICE_URL}/api/annotations"
        }
        return render_template('map.html', **cfg)

@app.route('/admin')
def admin():
    """Admin page"""
    try:
        # Get login data from auth service
        response = requests.get(f"{AUTH_SERVICE_URL}/admin/logins")
        if response.status_code == 200:
            data = response.json()
            logins = data.get('logins', [])
        else:
            logins = []
        
        return render_template('admin.html', logins=logins)
    except Exception as e:
        return render_template('admin.html', logins=[])

# ============= API Proxy Routes =============

# Auth Service Routes
@app.route('/signup', methods=['POST'])
def signup():
    """Proxy signup to auth service"""
    try:
        # Convert form data to JSON for microservice
        data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone', ''),
            'password': request.form.get('password')
        }
        
        response = requests.post(f"{AUTH_SERVICE_URL}/signup", json=data)
        result = response.json()
        
        if response.status_code == 201:
            flash(result.get('message', 'Account created successfully!'), "success")
        else:
            flash(result.get('error', 'Error during signup!'), "error")
            
        return redirect(url_for('auth'))
    except Exception as e:
        flash(f"Error during signup: {str(e)}", "error")
        return redirect(url_for('auth'))

@app.route('/signin', methods=['POST'])
def signin():
    """Proxy signin to auth service"""
    try:
        # Convert form data to JSON for microservice
        data = {
            'email': request.form.get('email'),
            'password': request.form.get('password')
        }
        
        response = requests.post(f"{AUTH_SERVICE_URL}/signin", json=data)
        result = response.json()
        
        if response.status_code == 200:
            return redirect(url_for('home'))
        else:
            flash(result.get('error', 'Invalid email or password!'), "error")
            return redirect(url_for('auth'))
    except Exception as e:
        flash(f"Error during signin: {str(e)}", "error")
        return redirect(url_for('auth'))

# Package Service Routes
@app.route('/api/packages', methods=['GET'])
def api_packages():
    """Proxy to package service"""
    try:
        response = requests.get(f"{PACKAGE_SERVICE_URL}/packages")
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/packages', methods=['POST'])
def api_packages_create():
    """Proxy to package service"""
    try:
        response = requests.post(f"{PACKAGE_SERVICE_URL}/packages", json=request.get_json())
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/packages/<int:package_id>', methods=['GET'])
def api_package_get(package_id):
    """Proxy to package service"""
    try:
        response = requests.get(f"{PACKAGE_SERVICE_URL}/packages/{package_id}")
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/places')
def api_places():
    """Proxy to package service for places data"""
    try:
        response = requests.get(f"{PACKAGE_SERVICE_URL}/api/places")
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Maps Service Routes
@app.route('/geojson')
def geojson():
    """Proxy to maps service"""
    try:
        response = requests.get(f"{MAPS_SERVICE_URL}/geojson")
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/geocode')
def geocode():
    """Proxy to maps service"""
    try:
        params = request.args.to_dict()
        response = requests.get(f"{MAPS_SERVICE_URL}/geocode", params=params)
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/route', methods=['POST'])
def route():
    """Proxy to maps service"""
    try:
        response = requests.post(f"{MAPS_SERVICE_URL}/route", json=request.get_json())
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cities')
def api_cities():
    """Proxy to maps service"""
    try:
        response = requests.get(f"{MAPS_SERVICE_URL}/api/cities")
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/annotations', methods=['GET', 'POST'])
def api_annotations():
    """Proxy to maps service"""
    try:
        if request.method == 'GET':
            response = requests.get(f"{MAPS_SERVICE_URL}/api/annotations")
        else:
            response = requests.post(f"{MAPS_SERVICE_URL}/api/annotations", json=request.get_json())
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/admin/refresh-geojson', methods=['POST'])
def admin_refresh_geojson():
    """Proxy to maps service"""
    try:
        response = requests.post(f"{MAPS_SERVICE_URL}/admin/refresh-geojson")
        return response.json(), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Static files
@app.route('/static/images/<path:filename>')
def static_images(filename):
    """Serve static images"""
    return send_from_directory(os.path.join(app.static_folder, 'images'), filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)