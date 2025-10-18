import React from 'react';
import { motion } from 'framer-motion';
import { Users, Star, Gauge, Fuel, Bike } from 'lucide-react';
import { Link } from 'react-router-dom';

const bikes = [
  // =======================
  // Superbikes / Hyperbikes
  // =======================
  {
    name: 'Ducati Panigale V4',
    type: 'Superbike',
    cc: '1103cc',
    mileage: '12–15 kmpl',
    capacity: '2',
    image: '/static/bikes/panigale-v4.jpg',
    features: ['Brembo Stylema', 'Cornering ABS', 'Quickshifter'],
    pricePerKm: '₹50',
    rating: 4.9,
    blurb: 'Track-bred performance with MotoGP DNA.'
  },
  {
    name: 'BMW S 1000 RR',
    type: 'Superbike',
    cc: '999cc',
    mileage: '14–16 kmpl',
    capacity: '2',
    image: '/static/bikes/bmw-s1000rr.jpg',
    features: ['ShiftCam', 'DTC', 'Quickshifter Pro'],
    pricePerKm: '₹48',
    rating: 4.9,
    blurb: 'Iconic liter-class superbike with cutting-edge electronics.'
  },
  {
    name: 'Kawasaki Ninja ZX-10R',
    type: 'Superbike',
    cc: '998cc',
    mileage: '13–15 kmpl',
    capacity: '2',
    image: '/static/bikes/zx10r.jpg',
    features: ['KQS', 'S-KTRC', 'Showa BFF'],
    pricePerKm: '₹42',
    rating: 4.8,
    blurb: 'Race-proven superbike with championship pedigree.'
  },
  {
    name: 'Suzuki Hayabusa',
    type: 'Hyperbike',
    cc: '1340cc',
    mileage: '12–14 kmpl',
    capacity: '2',
    image: '/static/bikes/hayabusa.jpg',
    features: ['Bi-dir QS', 'Cornering ABS', 'Cruise Control'],
    pricePerKm: '₹45',
    rating: 4.9,
    blurb: 'Legendary hyperbike—effortless power and comfort.'
  },
  {
    name: 'Ducati Streetfighter V4',
    type: 'Hyper-Naked',
    cc: '1103cc',
    mileage: '12–15 kmpl',
    capacity: '2',
    image: '/static/bikes/streetfighter-v4.jpg',
    features: ['Slide Control', 'Wheelie Control', 'Up/Down QS'],
    pricePerKm: '₹48',
    rating: 4.8,
    blurb: 'Panigale heart with upright aggression.'
  },
  {
    name: 'Aprilia RSV4 Factory',
    type: 'Superbike',
    cc: '1099cc',
    mileage: '12–15 kmpl',
    capacity: '2',
    image: '/static/bikes/aprilia-rsv4.jpg',
    features: ['APRC Suite', 'Öhlins EC 2.0', 'Brembo M50'],
    pricePerKm: '₹50',
    rating: 4.8,
    blurb: 'V4 soundtrack with factory-spec hardware.'
  },

  // =======================
  // Adventure / Touring / Power Cruiser / Premium Naked
  // =======================
  {
    name: 'BMW R 1250 GS Adventure',
    type: 'Adventure',
    cc: '1254cc',
    mileage: '20–22 kmpl',
    capacity: '2',
    image: '/static/bikes/r1250gsa.jpg',
    features: ['ShiftCam Boxer', 'ESA', 'Riding Modes Pro'],
    pricePerKm: '₹40',
    rating: 4.9,
    blurb: 'The gold standard for long-distance adventure touring.'
  },
  {
    name: 'Ducati Multistrada V4 S',
    type: 'Adventure',
    cc: '1158cc',
    mileage: '18–20 kmpl',
    capacity: '2',
    image: '/static/bikes/multistrada-v4s.jpg',
    features: ['Radar Cruise', 'Skyhook', 'Cornering Lights'],
    pricePerKm: '₹44',
    rating: 4.8,
    blurb: 'Radar-assisted touring with superbike intent.'
  },
  {
    name: 'Triumph Tiger 1200 Rally Pro',
    type: 'Adventure',
    cc: '1160cc',
    mileage: '18–20 kmpl',
    capacity: '2',
    image: '/static/bikes/tiger-1200-rally-pro.jpg',
    features: ['Showa Semi-Active', 'IMU ABS', 'QS'],
    pricePerKm: '₹38',
    rating: 4.7,
    blurb: 'Serious off-road ability with highway comfort.'
  },
  {
    name: 'Triumph Rocket 3 R',
    type: 'Power Cruiser',
    cc: '2458cc',
    mileage: '14–16 kmpl',
    capacity: '2',
    image: '/static/bikes/rocket-3r.jpg',
    features: ['IMU Rider Aids', 'Cruise Control', 'QS'],
    pricePerKm: '₹52',
    rating: 4.8,
    blurb: 'Massive torque and road presence.'
  },
  {
    name: 'Harley-Davidson Fat Boy 114',
    type: 'Cruiser',
    cc: '1868cc',
    mileage: '17–19 kmpl',
    capacity: '2',
    image: '/static/bikes/fatboy-114.jpg',
    features: ['Milwaukee-Eight 114', 'LED Lighting', 'Keyless'],
    pricePerKm: '₹36',
    rating: 4.7,
    blurb: 'Classic American cruiser with modern muscle.'
  },
  {
    name: 'KTM 790 Duke',
    type: 'Naked',
    cc: '799cc',
    mileage: '22–25 kmpl',
    capacity: '2',
    image: '/static/bikes/ktm-790-duke.jpg',
    features: ['Track Mode', 'Quickshifter+', 'Cornering MTC'],
    pricePerKm: '₹30',
    rating: 4.7,
    blurb: 'Scalpel-like handling and playful character.'
  },

  // =======================
  // Royal Enfield Lineup (India)
  // =======================
  {
    name: 'Royal Enfield Classic 350',
    type: 'Cruiser',
    cc: '349cc',
    mileage: '35–38 kmpl',
    capacity: '2',
    image: '/static/bikes/re-classic350.jpg',
    features: ['ABS', 'Dual Disc', 'USB Charging'],
    pricePerKm: '₹7.5',
    rating: 4.8,
    blurb: 'Timeless design with a refined J-series engine.'
  },
  {
    name: 'Royal Enfield Bullet 350',
    type: 'Classic',
    cc: '349cc',
    mileage: '35–38 kmpl',
    capacity: '2',
    image: '/static/bikes/re-bullet350.jpg',
    features: ['ABS', 'Comfort Seat', 'Alloy/Spoke Options'],
    pricePerKm: '₹7.0',
    rating: 4.7,
    blurb: 'Iconic thump and old-school charm, updated for today.'
  },
  {
    name: 'Royal Enfield Meteor 350',
    type: 'Cruiser',
    cc: '349cc',
    mileage: '35–40 kmpl',
    capacity: '2',
    image: '/static/bikes/re-meteor350.jpg',
    features: ['Tripper Nav (var.)', 'ABS', 'Low Seat'],
    pricePerKm: '₹7.2',
    rating: 4.7,
    blurb: 'Easygoing city cruiser with touring comfort.'
  },
  {
    name: 'Royal Enfield Hunter 350',
    type: 'Roadster',
    cc: '349cc',
    mileage: '36–40 kmpl',
    capacity: '2',
    image: '/static/bikes/re-hunter350.jpg',
    features: ['ABS', 'Alloy Wheels', 'USB Charging'],
    pricePerKm: '₹7.0',
    rating: 4.7,
    blurb: 'Compact, agile, and stylish—built for urban fun.'
  },
  {
    name: 'Royal Enfield Himalayan 450',
    type: 'Adventure',
    cc: '452cc',
    mileage: '30–32 kmpl',
    capacity: '2',
    image: '/static/bikes/re-himalayan450.jpg',
    features: ['Liquid-Cooled', 'Ride-by-Wire', 'Long Travel'],
    pricePerKm: '₹9.0',
    rating: 4.8,
    blurb: 'Go-anywhere ADV with modern tech and rugged build.'
  },
  {
    name: 'Royal Enfield Interceptor 650',
    type: 'Twin Roadster',
    cc: '648cc',
    mileage: '25–28 kmpl',
    capacity: '2',
    image: '/static/bikes/re-interceptor650.jpg',
    features: ['Parallel-Twin', 'ABS', 'Assist & Slipper Clutch'],
    pricePerKm: '₹10',
    rating: 4.8,
    blurb: 'Smooth twin, classic lines, and relaxed ergonomics.'
  },
  {
    name: 'Royal Enfield Continental GT 650',
    type: 'Café Racer',
    cc: '648cc',
    mileage: '24–27 kmpl',
    capacity: '2',
    image: '/static/bikes/re-continental-gt650.jpg',
    features: ['Clip-ons', 'Twin-Pod', 'ABS'],
    pricePerKm: '₹10.5',
    rating: 4.8,
    blurb: 'Retro racer stance with tractable twin performance.'
  },

  // =======================
  // Popular Indian Commuters / Basics
  // =======================
  {
    name: 'Hero Splendor Plus',
    type: 'Commuter',
    cc: '97cc',
    mileage: '60–65 kmpl',
    capacity: '2',
    image: '/static/bikes/hero-splendor.jpg',
    features: ['i3S (var.)', 'Alloy Wheels', 'ES'],
    pricePerKm: '₹4.5',
    rating: 4.6,
    blurb: 'India’s mileage king—ultra low running cost.'
  },
  {
    name: 'Honda Shine 125',
    type: 'Commuter',
    cc: '123.9cc',
    mileage: '55–60 kmpl',
    capacity: '2',
    image: '/static/bikes/honda-shine125.jpg',
    features: ['eSP', 'Silent Start', 'CBS'],
    pricePerKm: '₹5.0',
    rating: 4.6,
    blurb: 'Refined, reliable 125cc for daily use.'
  },
  {
    name: 'TVS Apache RTR 160 4V',
    type: 'Sport Commuter',
    cc: '159.7cc',
    mileage: '45–50 kmpl',
    capacity: '2',
    image: '/static/bikes/tvs-apache-160-4v.jpg',
    features: ['Ride Modes', 'Slipper Clutch (var.)', 'GTT'],
    pricePerKm: '₹5.8',
    rating: 4.6,
    blurb: 'Peppy 160cc with sharp dynamics and features.'
  },
  {
    name: 'Bajaj Pulsar 150',
    type: 'Sport Commuter',
    cc: '149.5cc',
    mileage: '45–50 kmpl',
    capacity: '2',
    image: '/static/bikes/pulsar-150.jpg',
    features: ['DTS-i', 'Tubeless', 'Disc/Drum (var.)'],
    pricePerKm: '₹5.5',
    rating: 4.6,
    blurb: 'Tried-and-true Pulsar—balanced power and economy.'
  },
  {
    name: 'Honda Unicorn',
    type: 'Commuter',
    cc: '162.7cc',
    mileage: '50–55 kmpl',
    capacity: '2',
    image: '/static/bikes/honda-unicorn.jpg',
    features: ['Monoshock', 'PGM-FI', 'Comfort Seat'],
    pricePerKm: '₹5.5',
    rating: 4.6,
    blurb: 'Buttery-smooth engine with all-day comfort.'
  },
  {
    name: 'Yamaha FZ-S FI V3',
    type: 'Street',
    cc: '149cc',
    mileage: '45–50 kmpl',
    capacity: '2',
    image: '/static/bikes/yamaha-fzs-v3.jpg',
    features: ['Fuel Injection', 'LED', 'Bluetooth (var.)'],
    pricePerKm: '₹5.8',
    rating: 4.6,
    blurb: 'Muscular styling with refined city manners.'
  },
  {
    name: 'Yamaha MT-15 V2',
    type: 'Naked',
    cc: '155cc',
    mileage: '40–45 kmpl',
    capacity: '2',
    image: '/static/bikes/yamaha-mt15.jpg',
    features: ['VVA', 'Assist & Slipper', 'USD Forks'],
    pricePerKm: '₹6.2',
    rating: 4.7,
    blurb: 'Lightweight, torquey, and fun—great for city.'
  },

  // =======================
  // Popular Scooters (Basics)
  // =======================
  {
    name: 'Honda Activa 6G',
    type: 'Scooter',
    cc: '109cc',
    mileage: '50–55 kmpl',
    capacity: '2',
    image: '/static/bikes/activa6g.jpg',
    features: ['Silent Start', 'Telescopic Forks', 'eSP'],
    pricePerKm: '₹4.5',
    rating: 4.6,
    blurb: 'India’s favorite scooter—easy, reliable, efficient.'
  },
  {
    name: 'TVS Jupiter',
    type: 'Scooter',
    cc: '110cc',
    mileage: '48–52 kmpl',
    capacity: '2',
    image: '/static/bikes/tvs-jupiter.jpg',
    features: ['External Fuel Fill', 'ETFi', 'Low Seat'],
    pricePerKm: '₹4.5',
    rating: 4.5,
    blurb: 'Comfortable and practical everyday scooter.'
  },
  {
    name: 'Suzuki Access 125',
    type: 'Scooter',
    cc: '124cc',
    mileage: '50–55 kmpl',
    capacity: '2',
    image: '/static/bikes/suzuki-access125.jpg',
    features: ['SEP', 'LED', 'USB (var.)'],
    pricePerKm: '₹4.8',
    rating: 4.6,
    blurb: 'Refined 125cc with strong low-end pull.'
  }
];

const card = {
  hidden: { opacity: 0, y: 14 },
  show: (i) => ({ opacity: 1, y: 0, transition: { delay: 0.05 * i, duration: 0.25 } })
};

const BikeFleet = () => {
  return (
    <section className="max-w-7xl mx-auto px-4 py-12">
      <div className="text-center mb-8">
        <h2 className="text-4xl font-extrabold tracking-tight">Our Premium Bikes</h2>
        <p className="mt-3 text-gray-400">
          Choose from our diverse range of well-maintained bikes for every travel need
        </p>
      </div>

      <div className="flex items-center justify-center gap-4 mb-10">
        {/* Visual chips; remove if you already have page-level tabs */}
        <span className="px-5 py-3 rounded-full bg-gray-700 text-gray-300 inline-flex items-center gap-2">
          Cars
        </span>
        <span className="px-5 py-3 rounded-full bg-yellow-500 text-black shadow-lg inline-flex items-center gap-2">
          <Bike className="w-5 h-5" /> Bikes
        </span>
      </div>

      <div className="grid gap-7 sm:grid-cols-2 lg:grid-cols-3">
        {bikes.map((b, i) => (
          <motion.div
            key={b.name}
            className="relative overflow-hidden rounded-2xl bg-[#0f172a] border border-gray-800 shadow-sm hover:shadow-md"
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, amount: 0.2 }}
            variants={card}
            custom={i}
          >
            {/* Price badge */}
            <div className="absolute top-3 right-3 z-10">
              <span className="rounded-full bg-yellow-500 text-black text-sm font-semibold px-3 py-1">
                {b.pricePerKm}/km
              </span>
            </div>

            {/* Image */}
            <div className="aspect-[16/10] w-full bg-gray-900 overflow-hidden">
              <img
                src={b.image}
                alt={b.name}
                className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
                onError={(e) => { e.currentTarget.src = '/static/bikes/placeholder-bike.jpg'; }}
              />
            </div>

            {/* Body */}
            <div className="p-5">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h3 className="text-xl font-semibold">{b.name}</h3>
                  <p className="text-xs text-gray-400 mt-0.5">{b.type}</p>
                </div>

                {/* Rating */}
                <div className="inline-flex items-center gap-1 bg-black/40 text-yellow-400 px-2 py-1 rounded-full">
                  <Star className="w-4 h-4 fill-current" />
                  <span className="text-sm font-semibold">{b.rating}</span>
                </div>
              </div>

              <p className="mt-3 text-sm text-gray-300 line-clamp-2">{b.blurb}</p>

              {/* Meta */}
              <div className="mt-4 flex flex-wrap gap-3 text-sm text-gray-300">
                <span className="inline-flex items-center gap-1">
                  <Users className="w-4 h-4" /> {b.capacity}
                </span>
                <span className="inline-flex items-center gap-1">
                  <Gauge className="w-4 h-4" /> {b.cc}
                </span>
                <span className="inline-flex items-center gap-1">
                  <Fuel className="w-4 h-4" /> {b.mileage}
                </span>
              </div>

              {/* Features */}
              <ul className="mt-4 flex flex-wrap gap-2">
                {b.features.map((f) => (
                  <li key={f} className="text-xs bg-gray-800 text-gray-200 rounded-full px-2.5 py-1">
                    {f}
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <div className="mt-5 flex items-center justify-between">
                <p className="text-base font-semibold">From {b.pricePerKm} per km</p>
                <Link to="/contact" className="text-sm font-medium underline underline-offset-4">
                  Book now
                </Link>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
};

export default BikeFleet;
