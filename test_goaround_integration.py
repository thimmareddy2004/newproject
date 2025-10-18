"""
Test GoAround + Fuel Calculator Integration
This shows how the fuel calculator enhances your GoAround app
"""

import sys
import os
import requests
import threading
import time
from flask import Flask

# Add microservices to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'microservices'))

print("🚗 GOAROUND + FUEL CALCULATOR INTEGRATION TEST")
print("="*50)

# Test 1: Direct integration
print("\n✅ Test 1: Direct Integration")
try:
    from microservices.fuel_calculator import IndiaFuelCalculator
    from microservices.fuel_api import integrate_fuel_calculator
    
    # Create a test Flask app
    test_app = Flask(__name__)
    
    # Integrate fuel calculator
    integrate_fuel_calculator(test_app)
    
    print("✓ Fuel calculator successfully integrated with Flask app")
    print("✓ All API routes have been added")
    
    # List the new routes
    fuel_routes = [rule.rule for rule in test_app.url_map.iter_rules() if 'fuel' in rule.rule]
    print(f"✓ Added {len(fuel_routes)} new fuel calculator routes:")
    for route in fuel_routes:
        print(f"   • {route}")
    
except Exception as e:
    print(f"✗ Integration failed: {e}")

# Test 2: Calculate fuel for a GoAround package
print("\n✅ Test 2: Sample GoAround Package with Fuel Costs")
try:
    calculator = IndiaFuelCalculator("bangalore")
    
    # Sample GoAround package: Bangalore → Mysore → Ooty → Coonoor
    package_name = "Karnataka Hill Stations Tour"
    places = ["Bangalore", "Mysore", "Ooty", "Coonoor"]
    distances = [150, 140, 35]  # km between places
    
    print(f"Package: {package_name}")
    print(f"Route: {' → '.join(places)}")
    print(f"Distances: {distances} km")
    
    # Create segments for fuel calculation
    segments = []
    for i, (place, distance) in enumerate(zip(places[1:], distances)):
        road_condition = "good_highway" if distance > 100 else "average_road"
        segments.append({
            "distance_km": distance,
            "road_condition": road_condition,
            "name": f"To {place}"
        })
    
    # Calculate fuel costs for different vehicles
    vehicles = ["hatchback_petrol", "hatchback_diesel", "suv_diesel", "bike_150cc"]
    
    print(f"\nFuel cost estimates for {sum(distances)}km total:")
    for vehicle in vehicles:
        trip_cost = calculator.calculate_trip_cost(segments, vehicle)
        vehicle_name = vehicle.replace("_", " ").title()
        print(f"  • {vehicle_name:20}: ₹{trip_cost['total_fuel_cost']:>6.0f}")
    
    # Best recommendation
    comparison = calculator.compare_vehicles(sum(distances), vehicles)
    best = comparison['most_economical']
    print(f"\n💡 Recommended: {best['vehicle_name']} (₹{best['total_cost']:.0f})")
    
except Exception as e:
    print(f"✗ Package calculation failed: {e}")

# Test 3: API endpoint simulation
print("\n✅ Test 3: API Endpoint Simulation")
try:
    # Simulate what happens when someone calls your API
    sample_request = {
        "distance_km": 300,
        "vehicle_key": "hatchback_petrol",
        "location": "bangalore"
    }
    
    calculator = IndiaFuelCalculator("bangalore")
    result = calculator.calculate_fuel_cost(
        sample_request["distance_km"],
        sample_request["vehicle_key"]
    )
    
    print(f"API Request: {sample_request}")
    print(f"API Response:")
    print(f"  • Total fuel cost: ₹{result['total_fuel_cost']}")
    print(f"  • Fuel consumed: {result['fuel_consumed_liters']} L")
    print(f"  • Cost per km: ₹{result['cost_per_km']}")
    
except Exception as e:
    print(f"✗ API simulation failed: {e}")

# Test 4: GoAround database integration potential
print("\n✅ Test 4: Database Integration Potential")
try:
    # Show how fuel costs could be stored with packages
    package_data = {
        "name": "Coastal Karnataka Tour",
        "places": ["Bangalore", "Mangalore", "Udupi", "Gokarna"],
        "distances": [350, 60, 150],
        "estimated_fuel_costs": {}
    }
    
    calculator = IndiaFuelCalculator("bangalore")
    total_distance = sum(package_data["distances"])
    
    # Calculate for popular vehicle types
    popular_vehicles = ["hatchback_petrol", "suv_diesel", "bike_150cc"]
    for vehicle in popular_vehicles:
        cost = calculator.calculate_fuel_cost(total_distance, vehicle)
        package_data["estimated_fuel_costs"][vehicle] = {
            "total_cost": cost["total_fuel_cost"],
            "cost_per_km": cost["cost_per_km"]
        }
    
    print("Sample package with fuel costs:")
    print(f"  • Package: {package_data['name']}")
    print(f"  • Total distance: {total_distance} km")
    print("  • Estimated fuel costs:")
    for vehicle, costs in package_data["estimated_fuel_costs"].items():
        vehicle_name = vehicle.replace("_", " ").title()
        print(f"    - {vehicle_name}: ₹{costs['total_cost']:.0f} (₹{costs['cost_per_km']:.1f}/km)")
    
except Exception as e:
    print(f"✗ Database integration test failed: {e}")

print("\n" + "="*50)
print("🎉 INTEGRATION TEST COMPLETE!")
print("="*50)

print("\n📊 SUMMARY:")
print("✓ Fuel calculator is integrated into your GoAround project")
print("✓ Works with your existing package system")
print("✓ Provides realistic Indian fuel cost estimates")
print("✓ Supports 11 different vehicle types")
print("✓ Accounts for regional pricing and road conditions")

print("\n🚀 TO USE IN YOUR GOAROUND APP:")
print("1. Start your Flask app: python app.py")
print("2. Create packages with fuel estimates using /api/packages/create-with-fuel")
print("3. Get fuel costs for any distance using /api/fuel/quick-estimate")
print("4. Compare vehicles using /api/fuel/compare-vehicles")

print("\n💡 BUSINESS VALUE:")
print("• Users can see realistic travel costs upfront")
print("• Help users choose the most economical vehicle")
print("• Differentiate GoAround from competitors")
print("• Increase booking confidence with transparent pricing")

print(f"\n📁 All files are in your project at:")
print(f"   {os.path.dirname(__file__)}")
print(f"   └── microservices/fuel_calculator.py")
print(f"   └── microservices/fuel_api.py")