import React, { useRef, useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import TestimonialsCarousel from '../components/TestimonialsCarousel.jsx';
import tinder1 from '../assets/images/Tinder 1.png';
import tinder2 from '../assets/images/Tinder 2.png';
import tinder3 from '../assets/images/Tinder 3.png';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe('pk_live_51QIlLMAnUfawcEVZyheb0Asq2W5Gn3k6OphgXIe4lmfgcyXgActd33ZIHi7pqdCvOtF57W5Huu7TEjHLnRkdiciH00vEurEtCg');
const renderBackend = 'https://swipemate.onrender.com';

const LandingPage = () => {
  const navigate = useNavigate();

  const buttonStyle = {
    background: '#D44A7A',
    border: '6px solid #E02844',
    padding: '0.5rem 1.5rem',
    borderRadius: '4px',
    boxShadow: 'none',
    color: 'white',
    cursor: 'pointer',
    fontSize: '1rem',
    marginTop: '1rem',
  };

  return (
    <div style={{ width: '100%', minHeight: '100vh', background: 'linear-gradient(to right, #ffffff, #e695b1)' }}>
      {/* Hero Section */}
      <div style={{ textAlign: 'center', padding: '4rem 1rem', color: '#D44A7A' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1.5rem' }}>SwipeMate AI</h1>
        <p style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>Go from simping to pimping!</p>
        <button
          style={buttonStyle}
          onClick={() => navigate('/privacy')} // Navigate to Privacy Policy
        >
          Privacy Policy
        </button>
      </div>

      {/* Other sections */}
      <div>
        <TestimonialsCarousel />
      </div>
    </div>
  );
};

export default LandingPage;
