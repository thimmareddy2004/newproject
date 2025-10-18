# Fuel Calculator API Integration Guide

## Overview
The Indian Fuel Calculator has been integrated into your GoAround travel platform. It provides comprehensive fuel cost calculations optimized for Indian road conditions, vehicle types, and regional fuel pricing.

## Features
- **Indian-specific**: Realistic mileage figures for Indian vehicles
- **Regional pricing**: State-wise fuel price variations
- **Road conditions**: Factors for different road types (highways, city traffic, hill stations)
- **Multiple vehicle types**: Cars, bikes, buses, auto-rickshaws
- **Trip planning**: Multi-segment journey calculations

## Available API Endpoints

### 1. Quick Fuel Estimate
**POST** `/api/fuel/quick-estimate`
```json
{
  "distance_km": 300,
  "vehicle_type": "hatchback_petrol",
  "location": "bangalore"
}
```

**Response:**
```json
{
  "distance_km": 300,
  "vehicle_type": "hatchback_petrol", 
  "location": "bangalore",
  "estimated_fuel_cost": 1566.0,
  "status": "success"
}
```

### 2. Detailed Calculation
**POST** `/api/fuel/detailed-calculation`
```json
{
  "distance_km": 300,
  "vehicle_key": "hatchback_petrol",
  "location": "bangalore",
  "city_percentage": 30,
  "road_condition": "good_highway"
}
```

**Response:**
```json
{
  "distance_km": 300,
  "vehicle_type": "car",
  "fuel_type": "petrol",
  "city_distance_km": 90.0,
  "highway_distance_km": 210.0,
  "city_mileage_kmpl": 15.0,
  "highway_mileage_kmpl": 20.0,
  "fuel_consumed_liters": 16.5,
  "fuel_price_per_liter": 104.53,
  "total_fuel_cost": 1724.75,
  "cost_per_km": 5.75,
  "location": "bangalore",
  "road_condition": "good_highway"
}
```

### 3. Trip Calculation (Multi-segment)
**POST** `/api/fuel/trip-calculation`
```json
{
  "segments": [
    {
      "distance_km": 60,
      "road_condition": "city_traffic",
      "name": "Bangalore to Highway"
    },
    {
      "distance_km": 180,
      "road_condition": "good_highway", 
      "name": "Highway to Mysore"
    },
    {
      "distance_km": 140,
      "road_condition": "hill_station",
      "name": "Mysore to Ooty"
    }
  ],
  "vehicle_key": "sedan_diesel",
  "location": "bangalore"
}
```

### 4. Vehicle Comparison
**POST** `/api/fuel/compare-vehicles`
```json
{
  "distance_km": 400,
  "vehicle_keys": ["hatchback_petrol", "hatchback_diesel", "bike_150cc"],
  "location": "bangalore"
}
```

**Response:**
```json
{
  "distance_km": 400,
  "comparisons": [
    {
      "vehicle_key": "bike_150cc",
      "vehicle_name": "Bike 150Cc",
      "total_cost": 372.46,
      "cost_per_km": 0.93,
      "fuel_type": "petrol",
      "mileage_city": 45.0,
      "mileage_highway": 55.0
    },
    {
      "vehicle_key": "hatchback_diesel", 
      "vehicle_name": "Hatchback Diesel",
      "total_cost": 800.09,
      "cost_per_km": 2.0,
      "fuel_type": "diesel"
    }
  ],
  "most_economical": {
    "vehicle_key": "bike_150cc",
    "total_cost": 372.46
  }
}
```

### 5. Get Available Vehicles
**GET** `/api/fuel/vehicles`

**Response:**
```json
{
  "vehicles": [
    {
      "key": "hatchback_petrol",
      "name": "Hatchback Petrol",
      "type": "car",
      "fuel_type": "petrol",
      "city_mileage": 15.0,
      "highway_mileage": 20.0,
      "tank_capacity": 40
    }
  ],
  "total_count": 11
}
```

### 6. Package Budget Estimation  
**POST** `/api/fuel/package-budget`
```json
{
  "places": ["Mysore", "Ooty", "Coonoor"],
  "distances": [150, 140, 50],
  "vehicle_type": "hatchback_petrol"
}
```

### 7. Road Conditions
**GET** `/api/fuel/road-conditions`

**Response:**
```json
{
  "road_conditions": [
    "excellent_highway",
    "good_highway", 
    "average_road",
    "city_traffic",
    "hill_station",
    "rural_road"
  ],
  "condition_factors": {
    "excellent_highway": 1.10,
    "good_highway": 1.00,
    "average_road": 0.85,
    "city_traffic": 0.70,
    "hill_station": 0.75,
    "rural_road": 0.80
  }
}
```

### 8. Enhanced Package Creation
**POST** `/api/packages/create-with-fuel`
```json
{
  "name": "Karnataka Hill Stations",
  "description": "Beautiful hill stations tour",
  "price": 15000,
  "places": ["bengaluru", "mysuru", "ooty"],
  "distances": [150, 140],
  "seasons": ["winter", "monsoon"],
  "categories": ["hill-station", "nature"],
  "vehicle_recommendations": true
}
```

## Vehicle Database

The system includes realistic mileage figures for Indian vehicles:

### Cars
- **Hatchback Petrol**: 15 kmpl (city), 20 kmpl (highway)
- **Hatchback Diesel**: 18 kmpl (city), 24 kmpl (highway)
- **Sedan Petrol**: 13 kmpl (city), 18 kmpl (highway)
- **Sedan Diesel**: 16 kmpl (city), 22 kmpl (highway)
- **SUV Petrol**: 10 kmpl (city), 14 kmpl (highway)
- **SUV Diesel**: 13 kmpl (city), 17 kmpl (highway)

### Two Wheelers
- **150cc Bike**: 45 kmpl (city), 55 kmpl (highway)
- **250cc Bike**: 35 kmpl (city), 45 kmpl (highway)
- **Scooter**: 50 kmpl (city), 60 kmpl (highway)

### Others
- **Auto CNG**: 25 kmpl (city), 30 kmpl (highway)
- **Bus Diesel**: 4 kmpl (city), 6 kmpl (highway)

## Regional Pricing

State-wise fuel price multipliers:
- **Maharashtra**: 1.02x
- **Karnataka**: 1.01x
- **Tamil Nadu**: 0.98x
- **Kerala**: 1.03x
- **Gujarat**: 0.97x
- **Rajasthan**: 1.04x
- **Delhi**: 1.00x (base)
- **Mumbai**: 1.05x
- **Bangalore**: 1.01x
- **Hyderabad**: 0.99x

## Road Condition Factors

- **Excellent Highway** (1.10x): Express highways with great conditions
- **Good Highway** (1.00x): National/State highways (baseline)
- **Average Road** (0.85x): District roads with moderate conditions  
- **City Traffic** (0.70x): Heavy urban traffic, frequent stops
- **Hill Station** (0.75x): Ghat sections, steep inclines/declines
- **Rural Road** (0.80x): Village roads, less maintained

## Integration Examples

### JavaScript Frontend Integration
```javascript
// Quick estimate
async function getQuickEstimate(distance, vehicleType) {
    const response = await fetch('/api/fuel/quick-estimate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            distance_km: distance,
            vehicle_type: vehicleType,
            location: 'bangalore'
        })
    });
    return await response.json();
}

// Vehicle comparison
async function compareVehicles(distance) {
    const response = await fetch('/api/fuel/compare-vehicles', {
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            distance_km: distance,
            vehicle_keys: ['hatchback_petrol', 'hatchback_diesel', 'bike_150cc']
        })
    });
    return await response.json();
}
```

### Package Integration
When creating travel packages, you can now include fuel cost estimates:

```javascript
async function createPackageWithFuel(packageData) {
    const response = await fetch('/api/packages/create-with-fuel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            ...packageData,
            distances: [120, 200, 80], // distances between places
            vehicle_recommendations: true
        })
    });
    return await response.json();
}
```

## Testing

Run the test script to verify integration:
```bash
cd C:\Users\Hp\OneDrive\Desktop\GoAround\GoAround
python test_fuel_calculator.py
```

## Error Handling

All endpoints return consistent error responses:
```json
{
  "error": "Error message description"
}
```

Common error codes:
- **400**: Invalid input data (e.g., distance <= 0)
- **500**: Internal server error

## Benefits for GoAround

1. **Enhanced User Experience**: Provide fuel cost estimates for travel packages
2. **Better Trip Planning**: Help users choose economical vehicles
3. **Regional Accuracy**: Account for local fuel prices and road conditions
4. **Competitive Advantage**: Offer detailed cost breakdowns other platforms lack

The fuel calculator is now fully integrated and ready to enhance your GoAround travel platform!