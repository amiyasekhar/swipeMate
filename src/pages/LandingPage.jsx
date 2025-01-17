import React, { useRef, useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import TestimonialsCarousel from '../components/TestimonialsCarousel.jsx';
import tinder1 from '../assets/images/Tinder 1.png';
import tinder2 from '../assets/images/Tinder 2.png';
import tinder3 from '../assets/images/Tinder 3.png';
import { loadStripe } from '@stripe/stripe-js';
//import './LandingPage.css'; // <-- Import your CSS file

const stripePromise = loadStripe('pk_live_51QIlLMAnUfawcEVZyheb0Asq2W5Gn3k6OphgXIe4lmfgcyXgActd33ZIHi7pqdCvOtF57W5Huu7TEjHLnRkdiciH00vEurEtCg');
const renderBackend = 'https://swipemate.onrender.com';

const LandingPage = () => {
  const getStartedSectionRef = useRef(null);
  const learnMoreSectionRef = useRef(null);
  
  const [authToken, setAuthToken] = useState('');
  const navigate = useNavigate();
  const [message, setMessage] = useState('');

  // This ref will hold all sections that need to fade in
  const fadeSectionRefs = useRef([]);

  // A callback ref to add each fade section to our array
  const addFadeSectionRef = useCallback((el) => {
    if (el && !fadeSectionRefs.current.includes(el)) {
      fadeSectionRefs.current.push(el);
    }
  }, []);

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Element has come into view. Add the fade-in class.
          entry.target.classList.add('fade-in');
        } else {
          // Element has left the viewport. Remove the fade-in class.
          entry.target.classList.remove('fade-in');
        }
      });
    }, { threshold: 0.1 });
  
    fadeSectionRefs.current.forEach((section) => {
      if (section) observer.observe(section);
    });
  
    return () => {
      if (fadeSectionRefs.current) {
        fadeSectionRefs.current.forEach((section) => {
          if (section) observer.unobserve(section);
        });
      }
    };
  }, [fadeSectionRefs]);

  const downloadFile = async () => {
    const localURL = 'http://localhost:3000/downloads/SwipeMate-Download.dmg';
    const hostedURL = 'https://swipemate.ai/downloads/SwipeMate-Download.dmg';
  
    try {
      const localResponse = await fetch(localURL, { method: 'HEAD' });
      if (localResponse.ok) {
        window.open(localURL, '_blank');
        console.log('Downloading from local server...');
        return;
      } else {
        console.warn('Local server not reachable, falling back to hosted URL.');
      }
    } catch (errorLocal) {
      console.error('Error checking local server:', errorLocal);
    }
  
    try {
      const hostedResponse = await fetch(hostedURL, { method: 'HEAD' });
      if (hostedResponse.ok) {
        window.open(hostedURL, '_blank');
        console.log('Downloading from hosted server...');
        return;
      } else {
        console.warn('Hosted server not reachable.');
      }
    } catch (errorHosted) {
      console.error('Error checking hosted server:', errorHosted);
    }
  
    alert(
      'Both local and hosted downloads failed. Please check your network connection or contact support.'
    );
  };

  const handlePayNow = async () => {
    try {
      if (!authToken) {
        alert('Please retrieve or enter your X-Auth-Token before proceeding to payment.');
        return;
      }

      const stripe = await stripePromise;
      console.log('The auth token: ', authToken);

      const response = await fetch(`${renderBackend}/create-checkout-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ authToken }),
      });

      if (!response.ok) {
        throw new Error('Failed to create checkout session');
      }

      const session = await response.json();
      console.log('session: ', session);

      window.location.href = session.url;
    } catch (error) {
      console.error('Error during handlePayNow: ', error);
      alert('An error occurred during payment. Please try again.');
    }
  };

  const scrollToGetStarted = () => {
    if (getStartedSectionRef.current) {
      const elementPosition = getStartedSectionRef.current.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.scrollY - 290; 
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth',
      });
    }
  };

  const scrollToLearnMore = () => {
    if (learnMoreSectionRef.current) {
      const elementPosition = learnMoreSectionRef.current.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.scrollY - 100;
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth',
      });
    }
  };

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

  // FAQ State
  const [openFAQ, setOpenFAQ] = useState(null);
  
  const faqs = [
    {
      question: "I don't feel comfortable downloading an app from a random site",
      answer: "It's ok! You don't need to. You can always use the chrome extension to retrieve the auth token, or use inspect element."
    },
    {
      question: "Is my data safe?",
      answer: "Safer than all birth control methods out there ;) We're kidding, but seriously, your auth token only enables us to literally only swipe right and left on tinder. You won't need to worry about safety, worry about not having more fun with whomever you meet ;)"
    },
    {
      question: "How many swipes do you guarantee me?",
      answer: "Our AI will swipe right on attractive girls either 500 times for each purchase, or until tinder restricts swiping (in the case of having a basic unpaid tinder account). We don't guarantee you matches...yet ;)"
    },
    {
      question: "Will I get matches?",
      answer: "Our AI can only swipe for you...for now until we make it more robust. The matches you get depends on the quality of your profile."
    }
  ];

  const toggleFAQ = (index) => {
    setOpenFAQ(openFAQ === index ? null : index);
  };

  return (
    <div style={{ width: '100%', minHeight: '100vh', background: 'linear-gradient(to right, #ffffff, #e695b1)' }}>
      {/* Hero Section */}
      <div
        className="fade-section"
        ref={addFadeSectionRef}
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
          color: '#D44A7A',
          padding: '4rem 1rem'
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
        <div
          style={{
            maxWidth: '700px',
            margin: '0 auto',
            textAlign: 'center',
            padding: '1rem',
            color: '#D44A7A'
          }}
        >
          <p style={{ fontSize: '1.125rem', marginBottom: '2rem' }}>
            Tired of spending hours on dating apps? SwipeMate is an AI that is trained to swipe right only on the most attractive women. Think of an AI wingman that swipes right only on the most objectively attractive women.
          </p>
        </div>

        <div>
          <button style={buttonStyle} onClick={scrollToGetStarted}>
            Get Started
          </button>
          <button style={{ ...buttonStyle, marginLeft: '1rem' }} onClick={scrollToLearnMore}>
            Learn More
          </button>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="fade-section" ref={addFadeSectionRef}>
        <TestimonialsCarousel />
      </div>

      {/* Instructions Section */}
      <div 
        className="fade-section"
        ref={addFadeSectionRef}
        style={{ padding: '2rem', textAlign: 'center', color: '#D44A7A', marginBottom: '-5em' }}
      >
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
                  width: '100%',
                  height: '100%',
                  objectFit: 'contain',
                  borderRadius: '8px',
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
                  width: '100%',
                  height: '100%',
                  objectFit: 'contain',
                  borderRadius: '8px',
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
                  width: '100%',
                  height: '150px',
                  objectFit: 'contain',
                  borderRadius: '8px',
                }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Get Started Token Section */}
      <div
        ref={getStartedSectionRef}
        className="fade-section"
        ref={addFadeSectionRef}
        style={{
          padding: '2rem',
          background: 'linear-gradient(to right, #ffffff, #e695b1)',
          borderRadius: '8px',
          textAlign: 'center',
          color: '#D44A7A',
          marginBottom: '6rem',
        }}
      >
        <p style={{ fontSize: '1.125rem', marginBottom: '1.5rem' }}>OR, MAKE SURE YOU HAVE CHROME AND EITHER...</p>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
          <button style={buttonStyle} onClick={() => {console.log('Button clicked'); downloadFile();}}>
            ➡️ DOWNLOAD SWIPEMATE ON MAC TO RETRIEVE TOKEN ⬅️
          </button>
          <button style={buttonStyle}>
            ➡️ DOWNLOAD SWIPEMATE ON WINDOWS TO RETRIEVE TOKEN ⬅️
          </button>
        </div>
        <div
              style={{
                maxWidth: '700px',
                margin: '0 auto',
                textAlign: 'center',
                padding: '1rem',
                color: '#D44A7A'
              }}
            >
          <p style={{ fontSize: '1.125rem', marginBottom: '1.5rem' }}>
            You may need to allow popups new windows to be opened when you click download
          </p>   
        </div>
        <div
              style={{
                maxWidth: '700px',
                margin: '0 auto',
                textAlign: 'center',
                padding: '1rem',
                color: '#D44A7A'
              }}
            >
          <p style={{ fontSize: '1.125rem', marginBottom: '1.5rem' }}>
            Once downloaded, make sure you go into your system's security settings if necessary, and allow SwipeMate to open and run!
          </p>
        </div>
        <div
              style={{
                maxWidth: '700px',
                margin: '0 auto',
                textAlign: 'center',
                padding: '1rem',
                color: '#D44A7A'
              }}
            >
          <p style={{ fontSize: '1.125rem', marginBottom: '1.5rem' }}>
            If not already logged in, SwipeMate will wait only 120 seconds for you to log in, and then scan for the token. Feel free to reopen and rerun SwipeMate if it takes you more than 120 seconds to log in
          </p>
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
        className="fade-section"
        ref={addFadeSectionRef}
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem',
          background: 'linear-gradient(to right, #ffffff, #e695b1)',
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
      
      {/* FAQ Section */}
      <div 
        className="fade-section" 
        ref={addFadeSectionRef}
        style={{
          padding: '2rem',
          background: '#fff', // Changed to white
          color: '#D44A7A',
          maxWidth: '800px',
          margin: '2rem auto',
          borderRadius: '8px'
        }}
      >
        <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem', textAlign: 'center' }}>FAQ</h2>
        {faqs.map((faq, index) => (
          <div key={index} style={{ marginBottom: '1rem', borderBottom: '1px solid #D44A7A', paddingBottom: '1rem' }}>
            <div 
              onClick={() => toggleFAQ(index)} 
              style={{ cursor: 'pointer', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}
            >
              <span style={{ fontSize: '1.125rem' }}>{faq.question}</span>
              <span style={{ fontSize: '1.5rem', transform: openFAQ === index ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.3s' }}>
                ▼
              </span>
            </div>
            {openFAQ === index && (
              <p style={{ marginTop: '0.5rem', fontSize: '1rem' }}>
                {faq.answer}
              </p>
            )}
          </div>
        ))}
      </div>
      
      {/* Footer */}
      <footer 
        className="fade-section" 
        ref={addFadeSectionRef}
        style={{
          textAlign: 'center',
          padding: '1rem',
          color: '#D44A7A',
          fontSize: '0.875rem'
        }}
      >
        © SwipeMate AI 2024
      </footer>
    </div>
  );
};

export default LandingPage;