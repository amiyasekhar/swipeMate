import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
// Import other necessary components or assets if needed
import tinder1 from '../assets/images/Tinder 1.png';
import tinder2 from '../assets/images/Tinder 2.png';
import tinder3 from '../assets/images/Tinder 3.png';

// Load your publishable key from Stripe
import { loadStripe } from '@stripe/stripe-js';
const stripePromise = loadStripe('YOUR_PUBLISHABLE_KEY_HERE');

const renderBackend = 'https://swipemate.onrender.com';

const LandingPage = () => {
  // References to sections
  const getStartedSectionRef = useRef(null);
  const learnMoreSectionRef = useRef(null);

  const [authToken, setAuthToken] = useState('');
  const navigate = useNavigate();

  // State to manage messages or errors
  const [message, setMessage] = useState('');

  const downloadFile = () => {
    window.open('http://localhost:3000/downloads/SwipeMate-optimized.dmg', '_blank');
  };

  /*const downloadFile = async () => {
    try {
      console.log('Attempting to fetch the local file...');
      const response = await fetch('http://localhost:3000/downloads/SwipeMate-optimized.dmg', {
        method: 'HEAD',
      });
  
      console.log('Fetch response:', response);
  
      if (response.ok) {
        console.log('Local file found. Initiating download...');
        window.open('http://localhost:3000/downloads/SwipeMate-optimized.dmg', '_blank');
      } else {
        console.error('Local file not found. Response status:', response.status, response.statusText);
        throw new Error('Local file not found');
      }
    } catch (error) {
      console.error('Error during local fetch attempt:', error.message || error);
  
      console.warn('Falling back to hosted file...');
      console.log('Opening hosted URL: https://swipemate.ai/downloads/SwipeMate-optimized.dmg');
      window.open('https://swipemate.ai/downloads/SwipeMate-optimized.dmg', '_blank');
    }
  };*/

  const handlePayNow = async () => {
    try {
      // Ensure the auth token is set
      if (!authToken) {
        alert('Please retrieve or enter your X-Auth-Token before proceeding to payment.');
        return;
      }

      // Proceed with payment logic
      const stripe = await stripePromise;

      console.log('The auth token: ', authToken);
      const response = await fetch(`${renderBackend}/create-checkout-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ authToken }), // Include auth token in the request
      });

      if (!response.ok) {
        throw new Error('Failed to create checkout session');
      }

      const session = await response.json();
      console.log('session: ', session);

      // Redirect to Stripe Checkout
      window.location.href = session.url;
    } catch (error) {
      console.error('Error during handlePayNow: ', error);
      alert('An error occurred during payment. Please try again.');
    }
  };

  // Scroll functions (optional, depending on your layout)
  const scrollToGetStarted = () => {
    if (getStartedSectionRef.current) {
      const elementPosition = getStartedSectionRef.current.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.scrollY - 290; // Adjust as needed
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth',
      });
    }
  };

  const scrollToLearnMore = () => {
    if (learnMoreSectionRef.current) {
      const elementPosition = learnMoreSectionRef.current.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.scrollY - 100; // Adjust as needed
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth',
      });
    }
  };

  // Common button styles
  const buttonStyle = {
    background: '#D44A7A',
    border: '6px solid #E02844',
    padding: '0.5rem 1.5rem',
    borderRadius: '4px',
    boxShadow: 'none',
    color: 'white',
    cursor: 'pointer',
    fontSize: '1rem',
  };

  const instructionStyle = {
    textAlign: 'center',
    fontSize: '1.125rem',
    marginBottom: '1rem',
  };

  return (
    <div style={{ width: '100%', minHeight: '100vh' }}>
      {/* Header Section */}
      <div
        style={{
          height: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center',
          color: '#D44A7A',
        }}
      >
        <h1
          style={{
            fontFamily: "'Segoe Script', 'Brush Script MT', cursive",
            fontSize: '2.5rem',
            marginBottom: '1.5rem',
          }}
        >
          SwipeMate AI
        </h1>
        <p style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>
          Go from simping to pimping!
        </p>
        <p style={{ fontSize: '1.125rem', marginBottom: '2rem' }}>
          SwipeMate is an AI that is trained to swipe right only on the most attractive women
        </p>

        {/* Buttons */}
        <div>
          <button style={buttonStyle} onClick={scrollToGetStarted}>
            Get Started
          </button>
          <button style={{ ...buttonStyle, marginLeft: '1rem' }} onClick={scrollToLearnMore}>
            Learn More
          </button>
        </div>
      </div>

      {/* Instructions Section */}
      <div style={{ padding: '2rem', textAlign: 'center', color: '#D44A7A', marginBottom: '-5em' }}>
        {/* Title above instructions */}
        <h2
          style={{
            fontSize: '1.5rem',
            fontWeight: 'bold',
            marginBottom: '1.5rem',
            textAlign: 'center',
          }}
        >
          Get Started
        </h2>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '2rem', marginBottom: '2rem' }}>
          {/* Step 1 */}
          <div style={{ flex: 1 }}>
            <p style={instructionStyle}>1. Log into the Tinder web app</p>
            <div
              style={{
                height: '150px',
                background: '#f5f5f5',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <img
                src={tinder1}
                style={{
                  width: '100%', // Fixed width
                  height: '100%', // Fixed height to make it square
                  objectFit: 'contain', // Ensures the image fills the square without distortion
                  borderRadius: '8px', // Optional: Keeps the rounded corners
                }}
              />
            </div>
          </div>

          {/* Step 2 */}
          <div style={{ flex: 1 }}>
            <p style={instructionStyle}>
              2. Left click, choose inspect element, open network tab, get X-Auth-Token
            </p>
            <div
              style={{
                height: '150px',
                background: '#f5f5f5',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <img
                src={tinder2}
                style={{
                  width: '100%', // Fixed width
                  height: '100%', // Fixed height to make it square
                  objectFit: 'contain', // Ensures the image fills the square without distortion
                  borderRadius: '8px', // Optional: Keeps the rounded corners
                }}
              />
            </div>
          </div>

          {/* Step 3 */}
          <div style={{ flex: 1 }}>
            <p style={instructionStyle}>3. Enter Token Below and Pay</p>
            <div
              style={{
                height: '150px',
                background: '#f5f5f5',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <img
                src={tinder3}
                style={{
                  width: '100%', // Fixed width
                  height: '150px', // Fixed height to make it square
                  objectFit: 'contain', // Ensures the image fills the square without distortion
                  borderRadius: '8px', // Optional: Keeps the rounded corners
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Target Section */}
      <div
        ref={getStartedSectionRef}
        style={{
          padding: '2rem',
          backgroundColor: '#fff',
          borderRadius: '8px',
          textAlign: 'center',
          color: '#D44A7A',
          marginBottom: '6rem',
        }}
      >
        <p style={{ fontSize: '1.125rem', marginBottom: '1.5rem' }}>OR, MAKE SURE YOU HAVE CHROME AND EITHER...</p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
          <button style={buttonStyle}>
            ➡️ DOWNLOAD SWIPEMATE ON MAC TO RETRIEVE TOKEN ⬅️
          </button>
          <button style={buttonStyle} onClick={() => {console.log('Button clicked'); downloadFile();}}>
            ➡️ DOWNLOAD SWIPEMATE ON WINDOWS TO RETRIEVE TOKEN ⬅️
          </button>
        </div>

        <p style={{ fontSize: '1.125rem', marginBottom: '1.5rem' }}>
          Enter X-Auth-Token below
        </p>
        <input
          type="text"
          value={authToken}
          onChange={(e) => setAuthToken(e.target.value)}
          style={{
            display: 'block',
            margin: '0 auto 1rem',
            padding: '0.5rem',
            border: '1px solid #D44A7A',
            borderRadius: '4px',
            width: '60%',
            color: '#D44A7A',
            outline: 'none',
          }}
        />
        {message && (
          <p style={{ color: message.includes('successfully') ? 'green' : 'red', marginBottom: '1rem' }}>
            {message}
          </p>
        )}
        <button style={buttonStyle} onClick={handlePayNow}>
          Proceed to Payment
        </button>
      </div>

      {/* Learn More Section */}
      <div
        ref={learnMoreSectionRef}
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem',
          backgroundColor: '#fff',
          color: '#D44A7A',
          textAlign: 'center',
        }}
      >
        <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>About SwipeMate</h2>
        <p style={{ fontSize: '1.125rem', marginBottom: '1.5rem', maxWidth: '800px' }}>
          SwipeMate is an AI model trained on more than 50,000 images of the most objectively attractive
          women in the world. From playboy models to runway models to the most beautiful girl you
          personally know—if they're on Tinder, SwipeMate will 100% swipe right on them. So what are you waiting for??
        </p>
        <button
          style={{
            background: '#D44A7A',
            border: '6px solid #E02844',
            padding: '0.5rem 1.5rem',
            borderRadius: '4px',
            boxShadow: 'none',
            color: 'white',
            cursor: 'pointer',
            fontSize: '1rem',
            marginBottom: '2rem',
          }}
          onClick={scrollToGetStarted}
        >
          Find Me Women, SwipeMate!
        </button>

        <h2 style={{ fontSize: '1.5rem', margin: '2rem 0 1rem' }}>Upcoming Features</h2>
        <ul
          style={{
            fontSize: '1.125rem',
            listStyle: 'none',
            padding: 0,
            textAlign: 'left',
            maxWidth: '800px',
          }}
        >
          <li>- Personalize SwipeMate according to your exact taste</li>
          <li>- Direct dating app login through SwipeMate page</li>
          <li>- Integration of other dating apps</li>
        </ul>
        <p style={{ marginTop: '1.5rem', fontSize: '1.125rem' }}>Stay tuned for more... 😊</p>
      </div>
    </div>
  );
};

export default LandingPage;