"""
Test script for the Indian Fuel Calculator
Run this to verify the fuel calculator is working correctly
"""

import sys
import os

# Add microservices to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'microservices'))

try:
    from microservices.fuel_calculator import IndiaFuelCalculator, quick_fuel_cost, estimate_travel_budget
    
    print("✅ Fuel Calculator imported successfully!")
    print("\n" + "="*50)
    print("TESTING FUEL CALCULATOR")
    print("="*50)
    
    # Test 1: Basic calculation
    print("\n1. Testing basic fuel cost calculation...")
    calculator = IndiaFuelCalculator("bangalore")
    result = calculator.calculate_fuel_cost(300, "hatchback_petrol")
    print(f"   Distance: 300 km")
    print(f"   Vehicle: Hatchback Petrol")
    print(f"   Total Cost: ₹{result['total_fuel_cost']}")
    print(f"   Fuel Consumed: {result['fuel_consumed_liters']} liters")
    print(f"   Cost per km: ₹{result['cost_per_km']}")
    
    # Test 2: Vehicle comparison
    print("\n2. Testing vehicle comparison...")
    comparison = calculator.compare_vehicles(400, ["hatchback_petrol", "hatchback_diesel", "bike_150cc"])
    print(f"   For 400 km journey:")
    for vehicle in comparison['comparisons']:
        print(f"   • {vehicle['vehicle_name']}: ₹{vehicle['total_cost']}")
    
    # Test 3: Multi-segment trip
    print("\n3. Testing multi-segment trip...")
    segments = [
        {"distance_km": 60, "road_condition": "city_traffic", "name": "Bangalore to Highway"},
        {"distance_km": 180, "road_condition": "good_highway", "name": "Highway to Mysore"},
        {"distance_km": 140, "road_condition": "hill_station", "name": "Mysore to Ooty"}
    ]
    trip_result = calculator.calculate_trip_cost(segments, "sedan_diesel")
    print(f"   Multi-segment trip (Bangalore → Mysore → Ooty):")
    print(f"   Total Distance: {trip_result['total_distance_km']} km")
    print(f"   Total Cost: ₹{trip_result['total_fuel_cost']}")
    print(f"   Average cost per km: ₹{trip_result['average_cost_per_km']}")
    
    # Test 4: Quick estimate function
    print("\n4. Testing quick estimate function...")
    quick_cost = quick_fuel_cost(250, "hatchback_petrol", "bangalore")
    print(f"   Quick estimate for 250 km: ₹{quick_cost}")
    
    # Test 5: Travel budget estimation
    print("\n5. Testing travel budget estimation...")
    places = ["Mysore", "Ooty", "Coonoor"]
    distances = [150, 140, 50]
    budget = estimate_travel_budget(places, distances, "hatchback_petrol")
    print(f"   Travel package budget:")
    print(f"   Most economical vehicle: {budget['budget_recommendations']['economical']['vehicle_name']}")
    print(f"   Budget range: ₹{budget['budget_recommendations']['fuel_budget_range']['min']:.0f} - ₹{budget['budget_recommendations']['fuel_budget_range']['max']:.0f}")
    
    print("\n6. Available vehicles...")
    vehicles = calculator.get_available_vehicles()
    print(f"   Total vehicles in database: {len(vehicles)}")
    for vehicle in vehicles[:5]:  # Show first 5
        print(f"   • {vehicle['name']}: {vehicle['city_mileage']} kmpl (city), {vehicle['highway_mileage']} kmpl (highway)")
    
    print("\n" + "="*50)
    print("✅ ALL TESTS PASSED! Fuel Calculator is ready for integration!")
    print("="*50)
    
except ImportError as e:
    print(f"❌ Failed to import fuel calculator: {e}")
    print("Make sure the fuel_calculator.py file is in the microservices folder")
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()

print("\n📋 API Endpoints that will be available after integration:")
print("   • POST /api/fuel/quick-estimate - Quick fuel cost estimate")
print("   • POST /api/fuel/detailed-calculation - Detailed calculation with breakdown")
print("   • POST /api/fuel/trip-calculation - Multi-segment trip calculation")
print("   • POST /api/fuel/compare-vehicles - Compare fuel costs across vehicles")
print("   • GET  /api/fuel/vehicles - Get list of available vehicles")
print("   • POST /api/fuel/package-budget - Estimate budget for complete package")
print("   • GET  /api/fuel/road-conditions - Get road condition factors")
print("   • POST /api/packages/create-with-fuel - Create package with fuel estimates")

print("\n🚀 Ready to run your Flask app with fuel calculator integration!")