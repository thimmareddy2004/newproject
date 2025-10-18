"""
Flask API routes for Fuel Calculator Integration
Add these routes to your main app.py
"""

from flask import request, jsonify
import sys
import os

# Add the microservices directory to Python path
sys.path.append(os.path.dirname(__file__))
from fuel_calculator import IndiaFuelCalculator, quick_fuel_cost, estimate_travel_budget

class FuelAPIRoutes:
    """Class containing all fuel calculation API routes"""
    
    @staticmethod
    def register_routes(app):
        """Register all fuel calculation routes with Flask app"""
        
        @app.route('/api/fuel/quick-estimate', methods=['POST'])
        def fuel_quick_estimate():
            """Quick fuel cost estimate for distance and vehicle type"""
            try:
                data = request.get_json()
                distance = float(data.get('distance_km', 0))
                vehicle_type = data.get('vehicle_type', 'hatchback_petrol')
                location = data.get('location', 'bangalore')
                
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
        
        @app.route('/api/fuel/detailed-calculation', methods=['POST'])
        def fuel_detailed_calculation():
            """Detailed fuel cost calculation with breakdown"""
            try:
                data = request.get_json()
                distance = float(data.get('distance_km', 0))
                vehicle_key = data.get('vehicle_key', 'hatchback_petrol')
                location = data.get('location', 'bangalore')
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
        
        @app.route('/api/fuel/trip-calculation', methods=['POST'])
        def fuel_trip_calculation():
            """Calculate fuel cost for multi-segment trip"""
            try:
                data = request.get_json()
                segments = data.get('segments', [])
                vehicle_key = data.get('vehicle_key', 'hatchback_petrol')
                location = data.get('location', 'bangalore')
                
                if not segments:
                    return jsonify({"error": "Trip segments required"}), 400
                
                calculator = IndiaFuelCalculator(location)
                result = calculator.calculate_trip_cost(segments, vehicle_key)
                
                return jsonify(result)
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/fuel/compare-vehicles', methods=['POST'])
        def fuel_compare_vehicles():
            """Compare fuel costs across different vehicles"""
            try:
                data = request.get_json()
                distance = float(data.get('distance_km', 0))
                vehicle_keys = data.get('vehicle_keys', ['hatchback_petrol', 'hatchback_diesel', 'bike_150cc'])
                location = data.get('location', 'bangalore')
                
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
                calculator = IndiaFuelCalculator()
                vehicles = calculator.get_available_vehicles()
                
                return jsonify({
                    "vehicles": vehicles,
                    "total_count": len(vehicles)
                })
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/fuel/package-budget', methods=['POST'])
        def fuel_package_budget():
            """Estimate travel budget for a complete package"""
            try:
                data = request.get_json()
                places = data.get('places', [])
                distances = data.get('distances', [])
                vehicle_type = data.get('vehicle_type', 'hatchback_petrol')
                
                if len(places) != len(distances):
                    return jsonify({"error": "Places and distances arrays must have same length"}), 400
                
                if not places or not distances:
                    return jsonify({"error": "Places and distances required"}), 400
                
                result = estimate_travel_budget(places, distances, vehicle_type)
                
                return jsonify(result)
                
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @app.route('/api/fuel/road-conditions', methods=['GET'])
        def fuel_road_conditions():
            """Get available road condition factors"""
            calculator = IndiaFuelCalculator()
            
            return jsonify({
                "road_conditions": list(calculator.ROAD_CONDITION_FACTORS.keys()),
                "condition_factors": calculator.ROAD_CONDITION_FACTORS,
                "description": {
                    "excellent_highway": "Express highways (factor: 1.10)",
                    "good_highway": "National/State highways (factor: 1.00)", 
                    "average_road": "District roads (factor: 0.85)",
                    "city_traffic": "Heavy city traffic (factor: 0.70)",
                    "hill_station": "Ghat/hill sections (factor: 0.75)",
                    "rural_road": "Village/rural roads (factor: 0.80)"
                }
            })

# Integration function for your existing app.py
def integrate_fuel_calculator(app):
    """
    Function to integrate fuel calculator with your existing Flask app
    Call this in your main app.py file
    """
    FuelAPIRoutes.register_routes(app)
    
    # Add fuel calculation to package creation
    @app.route('/api/packages/create-with-fuel', methods=['POST'])
    def create_package_with_fuel():
        """Enhanced package creation with fuel cost estimation"""
        try:
            data = request.get_json() or {}
            
            # Extract package data
            name = data.get('name', '').strip()
            description = data.get('description', '').strip()
            price = float(data.get('price') or 0.0)
            places_list = data.get('places', [])
            distances = data.get('distances', [])  # New field for distances
            vehicle_recommendations = data.get('vehicle_recommendations', True)
            
            if not name or not places_list:
                return jsonify({"error": "Package name and places required"}), 400
            
            # Calculate fuel estimates if distances provided
            fuel_estimates = None
            if distances and len(distances) == len(places_list):
                try:
                    fuel_estimates = estimate_travel_budget(
                        [f"Place {i+1}" for i in range(len(places_list))], 
                        distances
                    )
                except Exception as e:
                    print(f"Fuel calculation error: {e}")
            
            # Create package (your existing logic here)
            from app import Package, PackagePlace, db
            import json
            
            pkg = Package(
                name=name,
                description=description,
                price=price,
                seasons=",".join(data.get('seasons', [])),
                categories=",".join(data.get('categories', [])),
                image_urls=json.dumps(data.get('image_urls', [])),
            )
            
            # Add fuel estimates to description if available
            if fuel_estimates:
                fuel_info = f"\n\nEstimated Fuel Costs:\n"
                fuel_info += f"• Budget range: ₹{fuel_estimates['budget_recommendations']['fuel_budget_range']['min']:.0f} - ₹{fuel_estimates['budget_recommendations']['fuel_budget_range']['max']:.0f}\n"
                fuel_info += f"• Most economical: {fuel_estimates['budget_recommendations']['economical']['vehicle_name']}"
                pkg.description += fuel_info
            
            db.session.add(pkg)
            db.session.flush()
            
            # Create PackagePlace rows
            for idx, pid in enumerate(places_list):
                pp = PackagePlace(package_id=pkg.id, place_id=str(pid), sort_order=idx)
                db.session.add(pp)
            
            db.session.commit()
            
            response = {
                "ok": True, 
                "package_id": pkg.id,
                "fuel_estimates": fuel_estimates
            }
            
            return jsonify(response)
            
        except Exception as e:
            print("Error creating package with fuel calculation:", e)
            db.session.rollback()
            return jsonify({"ok": False, "error": str(e)}), 500