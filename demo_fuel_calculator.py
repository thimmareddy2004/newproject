"""
Simple Demo of Indian Fuel Calculator
Run this to see the fuel calculator in action!
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'microservices'))

from fuel_calculator import IndiaFuelCalculator, quick_fuel_cost

print("🚗 INDIAN FUEL CALCULATOR DEMO 🚗")
print("="*40)

# Create calculator for Bangalore
calculator = IndiaFuelCalculator("bangalore")

# Example 1: Simple calculation
print("\n📍 Example 1: Bangalore to Mysore (150 km)")
result = calculator.calculate_fuel_cost(150, "hatchback_petrol")
print(f"Vehicle: Hatchback Petrol")
print(f"Total Cost: ₹{result['total_fuel_cost']}")
print(f"Fuel Needed: {result['fuel_consumed_liters']} liters")
print(f"Cost per km: ₹{result['cost_per_km']}")

# Example 2: Compare vehicles
print("\n📍 Example 2: Vehicle Comparison for 200km trip")
vehicles = ["hatchback_petrol", "hatchback_diesel", "bike_150cc"]
comparison = calculator.compare_vehicles(200, vehicles)

for vehicle in comparison['comparisons']:
    print(f"• {vehicle['vehicle_name']}: ₹{vehicle['total_cost']:.0f}")

print(f"\n💰 Most economical: {comparison['most_economical']['vehicle_name']} (₹{comparison['most_economical']['total_cost']:.0f})")

# Example 3: Multi-city trip
print("\n📍 Example 3: Multi-city trip calculation")
segments = [
    {"distance_km": 60, "road_condition": "city_traffic", "name": "City to Highway"},
    {"distance_km": 120, "road_condition": "good_highway", "name": "Highway stretch"},
    {"distance_km": 40, "road_condition": "hill_station", "name": "Hill climb"}
]

trip = calculator.calculate_trip_cost(segments, "sedan_diesel")
print(f"Total distance: {trip['total_distance_km']} km")
print(f"Total fuel cost: ₹{trip['total_fuel_cost']}")

for segment in trip['segments']:
    print(f"  - {segment['name']}: ₹{segment['fuel_cost']:.0f}")

# Example 4: Available vehicles
print("\n📍 Available Vehicle Types:")
vehicles = calculator.get_available_vehicles()
for i, vehicle in enumerate(vehicles[:6], 1):  # Show first 6
    print(f"{i}. {vehicle['name']}: {vehicle['city_mileage']} kmpl (city)")

print(f"\n✅ Fuel Calculator is integrated and working!")
print(f"📁 Files are located in:")
print(f"   • microservices/fuel_calculator.py")
print(f"   • microservices/fuel_api.py") 
print(f"   • FUEL_CALCULATOR_API_GUIDE.md")

print(f"\n🌐 Your Flask app now has these new API endpoints:")
print(f"   • /api/fuel/quick-estimate")
print(f"   • /api/fuel/detailed-calculation")
print(f"   • /api/fuel/compare-vehicles")
print(f"   • /api/fuel/vehicles")
print(f"   • /api/fuel/package-budget")