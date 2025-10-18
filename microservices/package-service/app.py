import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify, send_from_directory
from shared.database import db, Package, PackagePlace, init_db
from shared.config import config
import json

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    init_db(app)
    
    return app

app = create_app()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "package-service"})

@app.route('/api/places', methods=['GET'])
def api_places():
    """Serve places dataset"""
    try:
        # Try to load from the original data directory
        data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'data', 'karnataka_places.json')
        if not os.path.exists(data_path):
            # Fallback sample data
            sample = [
                {
                    "id": "bengaluru",
                    "name": "Bengaluru (Bangalore)",
                    "lat": 12.9716,
                    "lon": 77.5946,
                    "categories": ["city", "historical", "temple", "park"],
                    "seasons": ["winter", "summer"],
                    "short_desc": "Capital city — parks, tech, temples, museums."
                }
            ]
            return jsonify(sample)
        
        with open(data_path, 'r', encoding='utf-8') as f:
            places = json.load(f)
        return jsonify(places)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/packages', methods=['GET'])
def get_packages():
    """Get all packages"""
    try:
        packages = Package.query.all()
        package_list = []
        
        for pkg in packages:
            package_dict = pkg.to_dict()
            # Add places information
            places = []
            for pp in sorted(pkg.places, key=lambda x: x.sort_order):
                places.append(pp.place_id)
            package_dict['places'] = places
            package_list.append(package_dict)
        
        return jsonify({
            "ok": True,
            "packages": package_list
        }), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/packages/<int:package_id>', methods=['GET'])
def get_package(package_id):
    """Get a specific package"""
    try:
        pkg = Package.query.get(package_id)
        if not pkg:
            return jsonify({"ok": False, "error": "Package not found"}), 404
        
        package_dict = pkg.to_dict()
        
        # Add places information with details
        data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'data', 'karnataka_places.json')
        places_map = {}
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                places = json.load(f)
                for p in places:
                    places_map[str(p.get('id'))] = p
        
        # Build ordered list with place details
        ordered_places = []
        for pp in sorted(pkg.places, key=lambda x: x.sort_order):
            pid = pp.place_id
            place_info = places_map.get(pid, {"id": pid, "name": pid})
            ordered_places.append(place_info)
        
        package_dict['places'] = ordered_places
        
        return jsonify({
            "ok": True,
            "package": package_dict
        }), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/packages', methods=['POST'])
def create_package():
    """Create a new package"""
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
            seasons=",".join(seasons) if seasons else "",
            categories=",".join(categories) if categories else "",
            image_urls=json.dumps(image_urls) if image_urls else "[]",
        )
        db.session.add(pkg)
        db.session.flush()  # get pkg.id

        # Create PackagePlace rows in the given order
        for idx, pid in enumerate(places_list):
            pp = PackagePlace(package_id=pkg.id, place_id=str(pid), sort_order=idx)
            db.session.add(pp)

        db.session.commit()
        
        return jsonify({
            "ok": True, 
            "package_id": pkg.id,
            "package": pkg.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/packages/<int:package_id>', methods=['PUT'])
def update_package(package_id):
    """Update a package"""
    try:
        pkg = Package.query.get(package_id)
        if not pkg:
            return jsonify({"ok": False, "error": "Package not found"}), 404
        
        data = request.get_json() or {}
        
        # Update package fields
        if 'name' in data:
            pkg.name = data['name'].strip()
        if 'description' in data:
            pkg.description = data['description'].strip()
        if 'price' in data:
            pkg.price = float(data['price'] or 0.0)
        if 'seasons' in data:
            pkg.seasons = ",".join(data['seasons']) if data['seasons'] else ""
        if 'categories' in data:
            pkg.categories = ",".join(data['categories']) if data['categories'] else ""
        if 'image_urls' in data:
            pkg.image_urls = json.dumps(data['image_urls']) if data['image_urls'] else "[]"
        
        # Update places if provided
        if 'places' in data:
            # Remove existing places
            PackagePlace.query.filter_by(package_id=package_id).delete()
            
            # Add new places
            for idx, pid in enumerate(data['places']):
                pp = PackagePlace(package_id=pkg.id, place_id=str(pid), sort_order=idx)
                db.session.add(pp)
        
        db.session.commit()
        
        return jsonify({
            "ok": True,
            "package": pkg.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/packages/<int:package_id>', methods=['DELETE'])
def delete_package(package_id):
    """Delete a package"""
    try:
        pkg = Package.query.get(package_id)
        if not pkg:
            return jsonify({"ok": False, "error": "Package not found"}), 404
        
        db.session.delete(pkg)
        db.session.commit()
        
        return jsonify({
            "ok": True,
            "message": "Package deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/static/images/<path:filename>')
def static_images(filename):
    """Serve static images"""
    static_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'images')
    return send_from_directory(static_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)