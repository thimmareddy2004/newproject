import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import BikeRental from './pages/BikeRental';

function App() {
  return (
    <BrowserRouter>
      <header style={{ padding: '12px', borderBottom: '1px solid #e5e7eb', background: '#fff' }}>
        <nav style={{ display: 'flex', gap: '12px' }}>
          <Link to="/">Home</Link>
          <Link to="/bike-rental">Bike Rentals</Link>
        </nav>
      </header>
      <Routes>
        <Route path="/" element={<div style={{ padding: 16 }}>Home (placeholder)</div>} />
        <Route path="/bike-rental" element={<BikeRental />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
