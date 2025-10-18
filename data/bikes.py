# data/bikes.py
# -*- coding: utf-8 -*-

BIKES = [
    # =======================
    # Superbikes / Hyperbikes
    # =======================
    {
        "name": "Ducati Panigale V4",
        "type": "Superbike",
        "cc": "1103cc",
        "mileage": "12–15 kmpl",
        "capacity": "2",
        "image": "panigale-v4.jpg",
        "features": ["Brembo Stylema", "Cornering ABS", "Quickshifter"],
        "price_per_km": "₹50",
        "rating": 4.9,
        "blurb": "Track-bred performance with MotoGP DNA."
    },
    {
        "name": "BMW S 1000 RR",
        "type": "Superbike",
        "cc": "999cc",
        "mileage": "14–16 kmpl",
        "capacity": "2",
        "image": "bmw-s1000rr.jpg",
        "features": ["ShiftCam", "Dynamic Traction Control", "Quickshifter Pro"],
        "price_per_km": "₹48",
        "rating": 4.9,
        "blurb": "Iconic liter-class superbike with cutting-edge electronics."
    },
    {
        "name": "Kawasaki Ninja ZX-10R",
        "type": "Superbike",
        "cc": "998cc",
        "mileage": "13–15 kmpl",
        "capacity": "2",
        "image": "zx10r.jpg",
        "features": ["KQS", "S-KTRC", "Showa BFF"],
        "price_per_km": "₹42",
        "rating": 4.8,
        "blurb": "Race-proven superbike with championship pedigree."
    },
    {
        "name": "Suzuki Hayabusa",
        "type": "Hyperbike",
        "cc": "1340cc",
        "mileage": "12–14 kmpl",
        "capacity": "2",
        "image": "hayabusa.jpg",
        "features": ["Bi-directional QS", "Cornering ABS", "Cruise Control"],
        "price_per_km": "₹45",
        "rating": 4.9,
        "blurb": "Legendary hyperbike—effortless power and comfort."
    },
    {
        "name": "Ducati Streetfighter V4",
        "type": "Hyper-Naked",
        "cc": "1103cc",
        "mileage": "12–15 kmpl",
        "capacity": "2",
        "image": "streetfighter-v4.jpg",
        "features": ["Wheelie Control", "Slide Control", "Up/Down QS"],
        "price_per_km": "₹48",
        "rating": 4.8,
        "blurb": "Panigale heart with upright aggression."
    },
    {
        "name": "Aprilia RSV4 Factory",
        "type": "Superbike",
        "cc": "1099cc",
        "mileage": "12–15 kmpl",
        "capacity": "2",
        "image": "aprilia-rsv4.jpg",
        "features": ["APRC Suite", "Öhlins Smart EC 2.0", "Brembo M50"],
        "price_per_km": "₹50",
        "rating": 4.8,
        "blurb": "V4 soundtrack with factory-spec hardware."
    },

    # ======================================
    # Adventure / Touring / Power Cruiser
    # ======================================
    {
        "name": "BMW R 1250 GS Adventure",
        "type": "Adventure",
        "cc": "1254cc",
        "mileage": "20–22 kmpl",
        "capacity": "2",
        "image": "r1250gsa.jpg",
        "features": ["ShiftCam Boxer", "ESA", "Riding Modes Pro"],
        "price_per_km": "₹40",
        "rating": 4.9,
        "blurb": "The gold standard for long-distance adventure touring."
    },
    {
        "name": "Ducati Multistrada V4 S",
        "type": "Adventure",
        "cc": "1158cc",
        "mileage": "18–20 kmpl",
        "capacity": "2",
        "image": "multistrada-v4s.jpg",
        "features": ["Radar Cruise", "Skyhook Suspension", "Cornering Lights"],
        "price_per_km": "₹44",
        "rating": 4.8,
        "blurb": "Radar-assisted touring with superbike intent."
    },
    {
        "name": "Triumph Tiger 1200 Rally Pro",
        "type": "Adventure",
        "cc": "1160cc",
        "mileage": "18–20 kmpl",
        "capacity": "2",
        "image": "tiger-1200-rally-pro.jpg",
        "features": ["Showa Semi-Active", "IMU ABS", "Quickshifter"],
        "price_per_km": "₹38",
        "rating": 4.7,
        "blurb": "Serious off-road ability with highway comfort."
    },
    {
        "name": "Triumph Rocket 3 R",
        "type": "Power Cruiser",
        "cc": "2458cc",
        "mileage": "14–16 kmpl",
        "capacity": "2",
        "image": "rocket-3r.jpg",
        "features": ["IMU Rider Aids", "Cruise Control", "Quickshifter"],
        "price_per_km": "₹52",
        "rating": 4.8,
        "blurb": "Massive torque and road presence."
    },
    {
        "name": "Harley-Davidson Fat Boy 114",
        "type": "Cruiser",
        "cc": "1868cc",
        "mileage": "17–19 kmpl",
        "capacity": "2",
        "image": "fatboy-114.jpg",
        "features": ["Milwaukee-Eight 114", "LED Lighting", "Keyless Ignition"],
        "price_per_km": "₹36",
        "rating": 4.7,
        "blurb": "Classic American cruiser with modern muscle."
    },
    {
        "name": "KTM 790 Duke",
        "type": "Naked",
        "cc": "799cc",
        "mileage": "22–25 kmpl",
        "capacity": "2",
        "image": "ktm-790-duke.jpg",
        "features": ["Track Mode", "Quickshifter+", "Cornering MTC"],
        "price_per_km": "₹30",
        "rating": 4.7,
        "blurb": "Scalpel-like handling and playful character."
    },

    # =======================
    # Royal Enfield (India)
    # =======================
    {
        "name": "Royal Enfield Classic 350",
        "type": "Cruiser",
        "cc": "349cc",
        "mileage": "35–38 kmpl",
        "capacity": "2",
        "image": "re-classic350.jpg",
        "features": ["ABS", "Dual Disc", "USB Charging"],
        "price_per_km": "₹7.5",
        "rating": 4.8,
        "blurb": "Timeless design with a refined J-series engine."
    },
    {
        "name": "Royal Enfield Bullet 350",
        "type": "Classic",
        "cc": "349cc",
        "mileage": "35–38 kmpl",
        "capacity": "2",
        "image": "re-bullet350.jpg",
        "features": ["ABS", "Comfort Seat", "Alloy/Spoke Options"],
        "price_per_km": "₹7.0",
        "rating": 4.7,
        "blurb": "Iconic thump and old-school charm, updated for today."
    },
    {
        "name": "Royal Enfield Meteor 350",
        "type": "Cruiser",
        "cc": "349cc",
        "mileage": "35–40 kmpl",
        "capacity": "2",
        "image": "re-meteor350.jpg",
        "features": ["Tripper Nav (var.)", "ABS", "Low Seat"],
        "price_per_km": "₹7.2",
        "rating": 4.7,
        "blurb": "Easygoing city cruiser with touring comfort."
    },
    {
        "name": "Royal Enfield Hunter 350",
        "type": "Roadster",
        "cc": "349cc",
        "mileage": "36–40 kmpl",
        "capacity": "2",
        "image": "re-hunter350.jpg",
        "features": ["ABS", "Alloy Wheels", "USB Charging"],
        "price_per_km": "₹7.0",
        "rating": 4.7,
        "blurb": "Compact, agile, and stylish—built for urban fun."
    },
    {
        "name": "Royal Enfield Himalayan 450",
        "type": "Adventure",
        "cc": "452cc",
        "mileage": "30–32 kmpl",
        "capacity": "2",
        "image": "re-himalayan450.jpg",
        "features": ["Liquid-Cooled", "Ride-by-Wire", "Long Travel"],
        "price_per_km": "₹9.0",
        "rating": 4.8,
        "blurb": "Go-anywhere ADV with modern tech and rugged build."
    },
    {
        "name": "Royal Enfield Interceptor 650",
        "type": "Twin Roadster",
        "cc": "648cc",
        "mileage": "25–28 kmpl",
        "capacity": "2",
        "image": "re-interceptor650.jpg",
        "features": ["Parallel-Twin", "ABS", "Assist & Slipper Clutch"],
        "price_per_km": "₹10",
        "rating": 4.8,
        "blurb": "Smooth twin, classic lines, and relaxed ergonomics."
    },
    {
        "name": "Royal Enfield Continental GT 650",
        "type": "Café Racer",
        "cc": "648cc",
        "mileage": "24–27 kmpl",
        "capacity": "2",
        "image": "re-continental-gt650.jpg",
        "features": ["Clip-ons", "Twin-Pod", "ABS"],
        "price_per_km": "₹10.5",
        "rating": 4.8,
        "blurb": "Retro racer stance with tractable twin performance."
    },

    # =======================
    # Popular Indian Commuters
    # =======================
    {
        "name": "Hero Splendor Plus",
        "type": "Commuter",
        "cc": "97cc",
        "mileage": "60–65 kmpl",
        "capacity": "2",
        "image": "hero-splendor.jpg",
        "features": ["i3S (var.)", "Alloy Wheels", "ES"],
        "price_per_km": "₹4.5",
        "rating": 4.6,
        "blurb": "India’s mileage king—ultra low running cost."
    },
    {
        "name": "Honda Shine 125",
        "type": "Commuter",
        "cc": "124cc",
        "mileage": "55–60 kmpl",
        "capacity": "2",
        "image": "honda-shine125.jpg",
        "features": ["eSP", "Silent Start", "CBS"],
        "price_per_km": "₹5.0",
        "rating": 4.6,
        "blurb": "Refined, reliable 125cc for daily use."
    },
    {
        "name": "TVS Apache RTR 160 4V",
        "type": "Sport Commuter",
        "cc": "160cc",
        "mileage": "45–50 kmpl",
        "capacity": "2",
        "image": "tvs-apache-160-4v.jpg",
        "features": ["Ride Modes", "Slipper Clutch (var.)", "GTT"],
        "price_per_km": "₹5.8",
        "rating": 4.6,
        "blurb": "Peppy 160cc with sharp dynamics and features."
    },
    {
        "name": "Bajaj Pulsar 150",
        "type": "Sport Commuter",
        "cc": "149cc",
        "mileage": "45–50 kmpl",
        "capacity": "2",
        "image": "pulsar-150.jpg",
        "features": ["DTS-i", "Tubeless", "Disc/Drum (var.)"],
        "price_per_km": "₹5.5",
        "rating": 4.6,
        "blurb": "Tried-and-true Pulsar—balanced power and economy."
    },
    {
        "name": "Honda Unicorn",
        "type": "Commuter",
        "cc": "163cc",
        "mileage": "50–55 kmpl",
        "capacity": "2",
        "image": "honda-unicorn.jpg",
        "features": ["Monoshock", "PGM-FI", "Comfort Seat"],
        "price_per_km": "₹5.5",
        "rating": 4.6,
        "blurb": "Buttery-smooth engine with all-day comfort."
    },
    {
        "name": "Yamaha FZ-S FI V3",
        "type": "Street",
        "cc": "149cc",
        "mileage": "45–50 kmpl",
        "capacity": "2",
        "image": "yamaha-fzs-v3.jpg",
        "features": ["Fuel Injection", "LED", "Bluetooth (var.)"],
        "price_per_km": "₹5.8",
        "rating": 4.6,
        "blurb": "Muscular styling with refined city manners."
    },
    {
        "name": "Yamaha MT-15 V2",
        "type": "Naked",
        "cc": "155cc",
        "mileage": "40–45 kmpl",
        "capacity": "2",
        "image": "yamaha-mt15.jpg",
        "features": ["VVA", "Assist & Slipper", "USD Forks"],
        "price_per_km": "₹6.2",
        "rating": 4.7,
        "blurb": "Lightweight, torquey, and fun—great for city."
    },

    # =======================
    # Popular Scooters
    # =======================
    {
        "name": "Honda Activa 6G",
        "type": "Scooter",
        "cc": "109cc",
        "mileage": "50–55 kmpl",
        "capacity": "2",
        "image": "activa6g.jpg",
        "features": ["Silent Start", "Telescopic Forks", "eSP"],
        "price_per_km": "₹4.5",
        "rating": 4.6,
        "blurb": "India’s favorite scooter—easy, reliable, efficient."
    },
    {
        "name": "TVS Jupiter",
        "type": "Scooter",
        "cc": "110cc",
        "mileage": "48–52 kmpl",
        "capacity": "2",
        "image": "tvs-jupiter.jpg",
        "features": ["External Fuel Fill", "ETFi", "Low Seat"],
        "price_per_km": "₹4.5",
        "rating": 4.5,
        "blurb": "Comfortable and practical everyday scooter."
    },
    {
        "name": "Suzuki Access 125",
        "type": "Scooter",
        "cc": "124cc",
        "mileage": "50–55 kmpl",
        "capacity": "2",
        "image": "suzuki-access125.jpg",
        "features": ["SEP", "LED", "USB (var.)"],
        "price_per_km": "₹4.8",
        "rating": 4.6,
        "blurb": "Refined 125cc with strong low-end pull."
    }
]
