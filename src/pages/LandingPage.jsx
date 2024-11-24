import React, { useRef, useState } from 'react';
import { Grid, Button, Typography, Container, TextField } from '@mui/material';
import { loadStripe } from '@stripe/stripe-js';
import { useNavigate } from 'react-router-dom';
import Screenshot1 from '../assets/images/screenshot1.png';
import Screenshot2 from '../assets/images/screenshot2.png';
// Load your publishable key from Stripe
const stripePromise = loadStripe('pk_live_51MIxt5KhH8zNT0eBV69mSH0djmZ50vIKUR71fICATT4g1qC6K6psICHaEePSIfQQqRUvHCRajt5HrQSCLoQzq8Bj00hiQS4fwh');
const renderBackend = 'https://swipemate.onrender.com'
const localhostURL = 'http://localhost:3002';
const LandingPage = () => {
    // References to sections
    const getStartedSectionRef = useRef(null);
    const learnMoreSectionRef = useRef(null);

    const [authToken, setAuthToken] = useState('');
    const navigate = useNavigate();

    // State to manage the auth token placeholder
    const [authTokenPlaceholder, setAuthTokenPlaceholder] = useState(
        "Enter X-Auth-Token"
    );


const handleTinderLogin = async () => {
  try {
    const response = await fetch(`${localhostURL}/tinder-login`, {
      method: "GET", 
      headers: {
        "Content-Type": "application/json", 
      },
    });

    const data = await response.json();

    if (response.ok ) {
    } else {
      throw new Error("Error with logging in.");
    }
  } catch (error) {
    console.error(error);

  }
};

const handlePayNow = async () => {
  try {
    // Step 1: Retrieve the auth token first
    await retrieveAuthToken(); // Ensure this completes before proceeding

    // Step 2: Proceed with payment logic
    const stripe = await stripePromise;

    console.log("The auth token: ", authToken);
    const response = await fetch(`${localhostURL}/create-checkout-session`, {
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
    console.log("session: ", session);

    // Redirect to Stripe Checkout
    window.location.href = session.url;
  } catch (error) {
    console.error("Error during handlePayNow: ", error);
  }
};

const retrieveAuthToken = async () => {
    try {
      const response = await fetch(`${localhostURL}/retrieve-auth-token`, {
        method: "GET", 
        headers: {
          "Content-Type": "application/json", 
        },
      });
  
      const data = await response.json();
  
      if (response.ok && data.token) {
        setAuthToken(data.token); // Update state with the retrieved token
      } else {
        throw new Error(data.error || "Couldn't auto retrieve auth token.");
      }
    } catch (error) {
      console.error(error);
      setAuthTokenPlaceholder(
        "Couldn't auto retrieve auth token. Please refresh the Tinder page or try logging into Tinder again."
      );
    }
};
  



    // Scroll function with offset for "Get Started"
    const scrollToGetStarted = () => {
        if (getStartedSectionRef.current) {
            const elementPosition = getStartedSectionRef.current.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.scrollY - 290; // Add an offset
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth',
            });
        }
    };

    // Scroll function with offset for "Learn More"
    const scrollToLearnMore = () => {
        if (learnMoreSectionRef.current) {
            const elementPosition = learnMoreSectionRef.current.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.scrollY - 100; // Add an offset
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
                    height: '100vh', // Full viewport height
                    display: 'flex', // Use flexbox
                    flexDirection: 'column',
                    justifyContent: 'center', // Center vertically
                    alignItems: 'center', // Center horizontally
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
                    <button
                        style={buttonStyle}
                        onClick={scrollToGetStarted} // Scrolls to the target section
                    >
                        Get Started
                    </button>
                    <button
                        style={{ ...buttonStyle, marginLeft: '1rem' }}
                        onClick={scrollToLearnMore} // Scrolls to the Learn More section
                    >
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
                        marginBottom: '1.5rem', // Add some spacing below the title
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
                            <p style={{ color: '#ccc' }}>Video Placeholder</p>
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
                            <p style={{ color: '#ccc' }}>Video Placeholder</p>
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
                            <p style={{ color: '#ccc' }}>Video Placeholder</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Target Section */}
            <div
                ref={getStartedSectionRef} // Reference to scroll back here
                style={{
                    padding: '2rem',
                    backgroundColor: '#fff',
                    borderRadius: '8px',
                    textAlign: 'center',
                    color: '#D44A7A',
                    marginBottom: '6rem', // Added extra spacing
                }}
            >
                <p style={{ fontSize: '1.125rem', marginBottom: '1.5rem' }}>
                    OR
                </p>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '-1rem', marginBottom: '1.5rem' }}>
                    <button style={buttonStyle} onClick={handleTinderLogin}>Log into Tinder here, then click retrieve token ➡️</button>
                    <button style={buttonStyle} onClick={retrieveAuthToken}>
                        Retrieve Token
                    </button>
                </div>
                <p style={{ fontSize: '1.125rem', marginBottom: '1.5rem' }}>
                    Enter X-Auth-Token below, or auto retrieve token by clicking above ⬆️ (P.S. Leave the browser open after retrieval!)
                </p>
                <input
                    type="text"
                    placeholder={authTokenPlaceholder}
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
                <button 
                    style={buttonStyle}
                    onClick={handlePayNow}
                >
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
                    onClick={scrollToGetStarted} // Scroll back to Get Started section
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