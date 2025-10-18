"""
Fuel Calculation Module for Indian Travel Conditions
Optimized for GoAround travel platform
"""

import math
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class VehicleSpecs:
    """Vehicle specifications for fuel calculations"""
    vehicle_type: str  # car, bike, bus, truck
    fuel_type: str     # petrol, diesel, cng, electric
    mileage_city: float    # kmpl in city
    mileage_highway: float # kmpl on highway
    tank_capacity: float   # liters
    engine_cc: Optional[int] = None

@dataclass
class FuelPrices:
    """Current fuel prices in India (₹/liter)"""
    petrol: float = 103.50  # Average price in major cities
    diesel: float = 89.50   # Average price in major cities
    cng: float = 75.20      # Average price per kg
    electric: float = 6.50  # ₹/kWh average

class IndiaFuelCalculator:
    """
    Advanced fuel calculator optimized for Indian road conditions
    """
    
    # Comprehensive Indian vehicle database with realistic mileage figures
    VEHICLE_DATABASE = {
        # Generic categories
        "hatchback_petrol": VehicleSpecs("car", "petrol", 15.0, 20.0, 40, 1200),
        "hatchback_diesel": VehicleSpecs("car", "diesel", 18.0, 24.0, 40, 1500),
        "sedan_petrol": VehicleSpecs("car", "petrol", 13.0, 18.0, 45, 1600),
        "sedan_diesel": VehicleSpecs("car", "diesel", 16.0, 22.0, 45, 1600),
        "suv_petrol": VehicleSpecs("car", "petrol", 10.0, 14.0, 60, 2000),
        "suv_diesel": VehicleSpecs("car", "diesel", 13.0, 17.0, 60, 2000),
        "bike_150cc": VehicleSpecs("bike", "petrol", 45.0, 55.0, 15, 150),
        "bike_250cc": VehicleSpecs("bike", "petrol", 35.0, 45.0, 20, 250),
        "scooter": VehicleSpecs("bike", "petrol", 50.0, 60.0, 7, 125),
        "auto_cng": VehicleSpecs("auto", "cng", 25.0, 30.0, 8),
        "bus_diesel": VehicleSpecs("bus", "diesel", 4.0, 6.0, 150, 5900),
        
        # Specific Hatchback Models
        "maruti_swift_petrol": VehicleSpecs("car", "petrol", 16.5, 21.5, 37, 1200),
        "maruti_swift_diesel": VehicleSpecs("car", "diesel", 20.0, 26.0, 37, 1300),
        "hyundai_i20_petrol": VehicleSpecs("car", "petrol", 15.5, 20.5, 37, 1200),
        "hyundai_i20_diesel": VehicleSpecs("car", "diesel", 19.5, 25.0, 37, 1400),
        "tata_altroz_petrol": VehicleSpecs("car", "petrol", 16.0, 21.0, 37, 1200),
        "tata_altroz_diesel": VehicleSpecs("car", "diesel", 20.5, 25.5, 37, 1500),
        "maruti_baleno_petrol": VehicleSpecs("car", "petrol", 17.0, 22.0, 37, 1200),
        "maruti_baleno_diesel": VehicleSpecs("car", "diesel", 21.0, 27.0, 37, 1300),
        "honda_jazz_petrol": VehicleSpecs("car", "petrol", 15.0, 19.0, 40, 1200),
        "volkswagen_polo_petrol": VehicleSpecs("car", "petrol", 14.5, 18.5, 45, 1000),
        "ford_figo_petrol": VehicleSpecs("car", "petrol", 15.5, 20.0, 40, 1200),
        "ford_figo_diesel": VehicleSpecs("car", "diesel", 18.5, 24.0, 40, 1500),
        "nissan_micra_petrol": VehicleSpecs("car", "petrol", 16.0, 20.5, 41, 1200),
        
        # Specific Sedan Models
        "maruti_dzire_petrol": VehicleSpecs("car", "petrol", 16.0, 21.0, 37, 1200),
        "maruti_dzire_diesel": VehicleSpecs("car", "diesel", 20.0, 26.0, 37, 1300),
        "hyundai_verna_petrol": VehicleSpecs("car", "petrol", 13.5, 18.0, 45, 1600),
        "hyundai_verna_diesel": VehicleSpecs("car", "diesel", 17.0, 22.5, 45, 1600),
        "honda_city_petrol": VehicleSpecs("car", "petrol", 14.0, 18.5, 40, 1500),
        "honda_city_diesel": VehicleSpecs("car", "diesel", 17.5, 23.0, 40, 1500),
        "tata_tigor_petrol": VehicleSpecs("car", "petrol", 16.5, 21.5, 35, 1200),
        "tata_tigor_diesel": VehicleSpecs("car", "diesel", 20.0, 25.5, 35, 1500),
        "volkswagen_vento_petrol": VehicleSpecs("car", "petrol", 13.0, 17.5, 50, 1600),
        "volkswagen_vento_diesel": VehicleSpecs("car", "diesel", 16.5, 21.5, 50, 1600),
        "skoda_rapid_petrol": VehicleSpecs("car", "petrol", 13.5, 18.0, 50, 1600),
        "skoda_rapid_diesel": VehicleSpecs("car", "diesel", 17.0, 22.0, 50, 1600),
        "toyota_yaris_petrol": VehicleSpecs("car", "petrol", 13.0, 17.5, 42, 1500),
        "honda_amaze_petrol": VehicleSpecs("car", "petrol", 15.5, 20.0, 35, 1200),
        "honda_amaze_diesel": VehicleSpecs("car", "diesel", 18.5, 24.0, 35, 1500),
        
        # SUVs and MUVs
        "maruti_ertiga_petrol": VehicleSpecs("car", "petrol", 12.0, 16.5, 45, 1500),
        "maruti_ertiga_diesel": VehicleSpecs("car", "diesel", 16.0, 21.0, 45, 1300),
        "hyundai_creta_petrol": VehicleSpecs("car", "petrol", 11.0, 15.5, 50, 1600),
        "hyundai_creta_diesel": VehicleSpecs("car", "diesel", 15.0, 19.5, 50, 1600),
        "tata_safari_diesel": VehicleSpecs("car", "diesel", 12.0, 16.0, 50, 2000),
        "tata_harrier_diesel": VehicleSpecs("car", "diesel", 12.5, 16.5, 50, 2000),
        "mahindra_xuv500_diesel": VehicleSpecs("car", "diesel", 11.0, 15.0, 60, 2200),
        "mahindra_scorpio_diesel": VehicleSpecs("car", "diesel", 10.5, 14.5, 60, 2200),
        "ford_ecosport_petrol": VehicleSpecs("car", "petrol", 12.5, 16.5, 52, 1500),
        "ford_ecosport_diesel": VehicleSpecs("car", "diesel", 16.0, 21.0, 52, 1500),
        "renault_duster_petrol": VehicleSpecs("car", "petrol", 11.5, 15.5, 50, 1600),
        "renault_duster_diesel": VehicleSpecs("car", "diesel", 15.0, 19.5, 50, 1500),
        "toyota_innova_diesel": VehicleSpecs("car", "diesel", 10.0, 14.0, 55, 2500),
        "toyota_fortuner_diesel": VehicleSpecs("car", "diesel", 9.0, 12.5, 80, 2800),
        "kia_seltos_petrol": VehicleSpecs("car", "petrol", 11.5, 16.0, 50, 1500),
        "kia_seltos_diesel": VehicleSpecs("car", "diesel", 15.5, 20.0, 50, 1500),
        "nissan_terrano_petrol": VehicleSpecs("car", "petrol", 11.0, 15.0, 60, 1600),
        "nissan_terrano_diesel": VehicleSpecs("car", "diesel", 15.0, 19.0, 60, 1500),
        
        # Motorcycles
        "hero_splendor_100cc": VehicleSpecs("bike", "petrol", 65.0, 75.0, 11, 100),
        "bajaj_pulsar_150cc": VehicleSpecs("bike", "petrol", 45.0, 55.0, 15, 150),
        "bajaj_pulsar_220cc": VehicleSpecs("bike", "petrol", 35.0, 45.0, 15, 220),
        "hero_passion_110cc": VehicleSpecs("bike", "petrol", 60.0, 70.0, 10, 110),
        "tvs_apache_160cc": VehicleSpecs("bike", "petrol", 40.0, 50.0, 16, 160),
        "yamaha_fz_150cc": VehicleSpecs("bike", "petrol", 42.0, 52.0, 13, 150),
        "honda_cb_shine_125cc": VehicleSpecs("bike", "petrol", 55.0, 65.0, 10.5, 125),
        "royal_enfield_350cc": VehicleSpecs("bike", "petrol", 30.0, 40.0, 20, 350),
        "royal_enfield_500cc": VehicleSpecs("bike", "petrol", 25.0, 35.0, 20, 500),
        "ktm_duke_200cc": VehicleSpecs("bike", "petrol", 30.0, 40.0, 13.5, 200),
        "ktm_duke_390cc": VehicleSpecs("bike", "petrol", 25.0, 35.0, 13.5, 390),
        "bajaj_dominar_400cc": VehicleSpecs("bike", "petrol", 26.0, 36.0, 13, 400),
        "honda_unicorn_150cc": VehicleSpecs("bike", "petrol", 50.0, 60.0, 13, 150),
        "suzuki_gixxer_155cc": VehicleSpecs("bike", "petrol", 40.0, 50.0, 12, 155),
        "tvs_ntorq_125cc": VehicleSpecs("bike", "petrol", 45.0, 55.0, 5.8, 125),
        
        # Scooters
        "honda_activa_110cc": VehicleSpecs("scooter", "petrol", 50.0, 60.0, 5.3, 110),
        "honda_activa_125cc": VehicleSpecs("scooter", "petrol", 48.0, 58.0, 5.3, 125),
        "tvs_jupiter_110cc": VehicleSpecs("scooter", "petrol", 52.0, 62.0, 5, 110),
        "suzuki_access_125cc": VehicleSpecs("scooter", "petrol", 50.0, 60.0, 5.6, 125),
        "yamaha_fascino_113cc": VehicleSpecs("scooter", "petrol", 52.0, 62.0, 5.2, 113),
        "hero_maestro_110cc": VehicleSpecs("scooter", "petrol", 51.0, 61.0, 5.4, 110),
        "bajaj_chetak_electric": VehicleSpecs("scooter", "electric", 90.0, 95.0, 2.9, 0),
        "ather_450x_electric": VehicleSpecs("scooter", "electric", 85.0, 90.0, 2.9, 0),
        
        # Commercial Vehicles
        "auto_petrol": VehicleSpecs("auto", "petrol", 20.0, 25.0, 8, 200),
        "tata_ace_diesel": VehicleSpecs("truck", "diesel", 12.0, 16.0, 30, 700),
        "mahindra_bolero_pickup_diesel": VehicleSpecs("truck", "diesel", 11.0, 15.0, 60, 2500),
        "force_tempo_traveller_diesel": VehicleSpecs("bus", "diesel", 8.0, 12.0, 60, 2600),
        "truck_diesel": VehicleSpecs("truck", "diesel", 4.0, 6.0, 200, 5900),
        "mini_truck_diesel": VehicleSpecs("truck", "diesel", 8.0, 12.0, 60, 1500),
        
        # Electric Vehicles
        "tata_nexon_ev": VehicleSpecs("car", "electric", 120.0, 130.0, 30.2, 0),
        "mahindra_e2o_electric": VehicleSpecs("car", "electric", 110.0, 120.0, 9.4, 0),
        "hyundai_kona_electric": VehicleSpecs("car", "electric", 140.0, 150.0, 39.2, 0),
        "mg_zs_ev": VehicleSpecs("car", "electric", 130.0, 140.0, 44.5, 0),
        "ola_s1_electric": VehicleSpecs("scooter", "electric", 85.0, 90.0, 2.98, 0),
        "tvs_iqube_electric": VehicleSpecs("scooter", "electric", 80.0, 85.0, 2.25, 0),
        "generic_electric_car": VehicleSpecs("car", "electric", 120.0, 130.0, 30.0, 0),
        "generic_electric_bike": VehicleSpecs("bike", "electric", 80.0, 85.0, 2.5, 0),
    }
    
    # Indian state-wise fuel price variations (multiplier)
    STATE_PRICE_MULTIPLIER = {
        "maharashtra": 1.02,
        "karnataka": 1.01,
        "tamil_nadu": 0.98,
        "kerala": 1.03,
        "gujarat": 0.97,
        "rajasthan": 1.04,
        "delhi": 1.00,
        "mumbai": 1.05,
        "bangalore": 1.01,
        "hyderabad": 0.99,
    }
    
    # Road condition factors for Indian highways/cities
    ROAD_CONDITION_FACTORS = {
        "excellent_highway": 1.10,  # Express highways
        "good_highway": 1.00,       # NH, SH
        "average_road": 0.85,       # District roads
        "city_traffic": 0.70,       # Heavy traffic
        "hill_station": 0.75,       # Ghat sections
        "rural_road": 0.80,         # Village roads
    }
    
    def __init__(self, location: str = "bangalore"):
        self.location = location.lower()
        self.fuel_prices = FuelPrices()
        self._apply_location_pricing()
    
    def _apply_location_pricing(self):
        """Apply location-based fuel pricing"""
        multiplier = self.STATE_PRICE_MULTIPLIER.get(self.location, 1.00)
        self.fuel_prices.petrol *= multiplier
        self.fuel_prices.diesel *= multiplier
        self.fuel_prices.cng *= multiplier
    
    def get_vehicle_mileage(self, vehicle_key: str, road_condition: str = "good_highway") -> Tuple[float, float]:
        """Get vehicle mileage adjusted for road conditions"""
        if vehicle_key not in self.VEHICLE_DATABASE:
            raise ValueError(f"Vehicle {vehicle_key} not found in database")
        
        vehicle = self.VEHICLE_DATABASE[vehicle_key]
        factor = self.ROAD_CONDITION_FACTORS.get(road_condition, 1.00)
        
        return vehicle.mileage_city * factor, vehicle.mileage_highway * factor
    
    def calculate_fuel_cost(self, 
                          distance_km: float, 
                          vehicle_key: str,
                          city_percentage: float = 30.0,
                          road_condition: str = "good_highway") -> Dict:
        """
        Calculate comprehensive fuel cost for Indian travel
        
        Args:
            distance_km: Total distance in kilometers
            vehicle_key: Vehicle type from database
            city_percentage: Percentage of city driving (0-100)
            road_condition: Road condition type
            
        Returns:
            Dictionary with detailed cost breakdown
        """
        if vehicle_key not in self.VEHICLE_DATABASE:
            return {"error": f"Vehicle {vehicle_key} not supported"}
        
        vehicle = self.VEHICLE_DATABASE[vehicle_key]
        city_mileage, highway_mileage = self.get_vehicle_mileage(vehicle_key, road_condition)
        
        # Calculate distance breakdown
        city_distance = distance_km * (city_percentage / 100)
        highway_distance = distance_km - city_distance
        
        # Calculate fuel consumption
        city_fuel = city_distance / city_mileage if city_mileage > 0 else 0
        highway_fuel = highway_distance / highway_mileage if highway_mileage > 0 else 0
        total_fuel = city_fuel + highway_fuel
        
        # Get fuel price
        fuel_price_per_liter = getattr(self.fuel_prices, vehicle.fuel_type)
        
        # Calculate costs
        total_cost = total_fuel * fuel_price_per_liter
        cost_per_km = total_cost / distance_km if distance_km > 0 else 0
        
        return {
            "distance_km": distance_km,
            "vehicle_type": vehicle.vehicle_type,
            "fuel_type": vehicle.fuel_type,
            "city_distance_km": round(city_distance, 2),
            "highway_distance_km": round(highway_distance, 2),
            "city_mileage_kmpl": round(city_mileage, 2),
            "highway_mileage_kmpl": round(highway_mileage, 2),
            "fuel_consumed_liters": round(total_fuel, 2),
            "fuel_price_per_liter": fuel_price_per_liter,
            "total_fuel_cost": round(total_cost, 2),
            "cost_per_km": round(cost_per_km, 2),
            "location": self.location,
            "road_condition": road_condition,
            "calculation_date": datetime.now().isoformat()
        }
    
    def calculate_trip_cost(self, 
                           route_segments: List[Dict],
                           vehicle_key: str) -> Dict:
        """
        Calculate cost for multi-segment trip (useful for GoAround packages)
        
        Args:
            route_segments: List of segments with distance and road_condition
            vehicle_key: Vehicle type
            
        Example:
            segments = [
                {"distance_km": 50, "road_condition": "city_traffic", "name": "Bangalore to outskirts"},
                {"distance_km": 200, "road_condition": "good_highway", "name": "Highway to Mysore"},
                {"distance_km": 30, "road_condition": "hill_station", "name": "Mysore to Ooty"}
            ]
        """
        total_cost = 0
        total_distance = 0
        total_fuel = 0
        segment_details = []
        
        for segment in route_segments:
            distance = segment["distance_km"]
            condition = segment.get("road_condition", "good_highway")
            name = segment.get("name", f"Segment {len(segment_details) + 1}")
            
            # Calculate for this segment
            result = self.calculate_fuel_cost(
                distance, 
                vehicle_key, 
                city_percentage=0,  # Treat each segment as per its condition
                road_condition=condition
            )
            
            segment_details.append({
                "name": name,
                "distance_km": distance,
                "road_condition": condition,
                "fuel_cost": result["total_fuel_cost"],
                "fuel_consumed": result["fuel_consumed_liters"]
            })
            
            total_cost += result["total_fuel_cost"]
            total_distance += distance
            total_fuel += result["fuel_consumed_liters"]
        
        return {
            "total_distance_km": total_distance,
            "total_fuel_cost": round(total_cost, 2),
            "total_fuel_consumed_liters": round(total_fuel, 2),
            "average_cost_per_km": round(total_cost / total_distance if total_distance > 0 else 0, 2),
            "vehicle_key": vehicle_key,
            "segments": segment_details,
            "calculation_date": datetime.now().isoformat()
        }
    
    def compare_vehicles(self, distance_km: float, vehicle_keys: List[str]) -> Dict:
        """Compare fuel costs across different vehicles"""
        comparisons = []
        
        for vehicle_key in vehicle_keys:
            if vehicle_key in self.VEHICLE_DATABASE:
                result = self.calculate_fuel_cost(distance_km, vehicle_key)
                comparisons.append({
                    "vehicle_key": vehicle_key,
                    "vehicle_name": vehicle_key.replace("_", " ").title(),
                    "total_cost": result["total_fuel_cost"],
                    "cost_per_km": result["cost_per_km"],
                    "fuel_type": result["fuel_type"],
                    "mileage_city": result["city_mileage_kmpl"],
                    "mileage_highway": result["highway_mileage_kmpl"]
                })
        
        # Sort by total cost
        comparisons.sort(key=lambda x: x["total_cost"])
        
        return {
            "distance_km": distance_km,
            "comparisons": comparisons,
            "most_economical": comparisons[0] if comparisons else None,
            "calculation_date": datetime.now().isoformat()
        }

    def get_available_vehicles(self) -> List[Dict]:
        """Get list of all available vehicles with their specs"""
        vehicles = []
        for key, specs in self.VEHICLE_DATABASE.items():
            vehicles.append({
                "key": key,
                "name": key.replace("_", " ").title(),
                "type": specs.vehicle_type,
                "fuel_type": specs.fuel_type,
                "city_mileage": specs.mileage_city,
                "highway_mileage": specs.mileage_highway,
                "tank_capacity": specs.tank_capacity
            })
        return vehicles

# Utility functions for easy integration
def quick_fuel_cost(distance_km: float, vehicle_type: str = "hatchback_petrol", location: str = "bangalore") -> float:
    """Quick fuel cost calculation - returns just the cost"""
    calculator = IndiaFuelCalculator(location)
    result = calculator.calculate_fuel_cost(distance_km, vehicle_type)
    return result.get("total_fuel_cost", 0)

def estimate_travel_budget(places: List[str], distances: List[float], vehicle_type: str = "hatchback_petrol") -> Dict:
    """Estimate travel budget for a package - useful for GoAround integration"""
    total_distance = sum(distances)
    calculator = IndiaFuelCalculator()
    
    # Create segments
    segments = []
    for i, (place, distance) in enumerate(zip(places, distances)):
        segments.append({
            "distance_km": distance,
            "road_condition": "good_highway",  # Default assumption
            "name": f"To {place}"
        })
    
    trip_cost = calculator.calculate_trip_cost(segments, vehicle_type)
    vehicle_comparison = calculator.compare_vehicles(total_distance, 
        ["hatchback_petrol", "hatchback_diesel", "bike_150cc", "suv_diesel"])
    
    return {
        "trip_details": trip_cost,
        "vehicle_options": vehicle_comparison,
        "budget_recommendations": {
            "economical": vehicle_comparison["most_economical"],
            "fuel_budget_range": {
                "min": vehicle_comparison["most_economical"]["total_cost"],
                "max": vehicle_comparison["comparisons"][-1]["total_cost"]
            }
        }
    }

if __name__ == "__main__":
    # Example usage
    calculator = IndiaFuelCalculator("bangalore")
    
    # Example 1: Simple calculation
    result = calculator.calculate_fuel_cost(300, "hatchback_petrol")
    print("Simple calculation:", result)
    
    # Example 2: Trip with multiple segments
    segments = [
        {"distance_km": 60, "road_condition": "city_traffic", "name": "Bangalore to Highway"},
        {"distance_km": 180, "road_condition": "good_highway", "name": "Highway to Mysore"},
        {"distance_km": 140, "road_condition": "hill_station", "name": "Mysore to Ooty"}
    ]
    trip_result = calculator.calculate_trip_cost(segments, "sedan_diesel")
    print("\nTrip calculation:", trip_result)
    
    # Example 3: Vehicle comparison
    comparison = calculator.compare_vehicles(400, ["hatchback_petrol", "hatchback_diesel", "bike_150cc"])
    print("\nVehicle comparison:", comparison)