import React from 'react';
import Slider from 'react-slick';

// Import your 7 images (adjust the paths to match your actual file structure)
// Ensure these image paths are correct.
import img1 from '../assets/images/Test1.png';
import img2 from '../assets/images/Test2.png';
import img3 from '../assets/images/Test3.png';
import img4 from '../assets/images/Test4.png';
import img5 from '../assets/images/Test5.png';
import img6 from '../assets/images/Test6.png';
import img7 from '../assets/images/Test7.png';

// Testimonials data
const testimonials = [
  {
    image: img1,
    text: "Before SwipeMate, my matches always felt random. Now, I’m with someone who makes me feel cherished every single day. We’re creating moments I never imagined possible.",
    name: "Ryan T."
  },
  {
    image: img2,
    text: "I was tired of endless swipes with no real sparks. SwipeMate’s recommendations led me straight to someone who sets my heart on fire. We clicked from the first moment!",
    name: "Jake M."
  },
  {
    image: img3,
    text: "From candlelit dinners to late-night city strolls, SwipeMate matched me with someone who shares my sense of adventure. We went from small talk to unforgettable nights out.",
    name: "Ethan L."
  },
  {
    image: img4,
    text: "SwipeMate isn’t just about romance—it introduced me to a whole new social circle! I’ve gained amazing friends who turn ordinary weekends into epic stories.",
    name: "Alex R."
  },
  {
    image: img5,
    text: "I never expected a dating app to broaden my world this much. SwipeMate brought me people who lift my spirits and show me that life’s best moments are shared.",
    name: "Sam K."
  },
  {
    image: img6,
    text: "SwipeMate found someone who matches my vibe to a tee. From music festivals to impromptu road trips, we’re always in sync and having the time of our lives.",
    name: "Liam P."
  },
  {
    image: img7,
    text: "I didn’t think it was possible to meet someone who ‘just got me’ online. Thanks to SwipeMate, I’ve found a partner who adds warmth, laughter, and meaning to my everyday life.",
    name: "Tom C."
  }
];

const TestimonialsCarousel = () => {
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 4000,
    pauseOnHover: true,
    arrows: false
  };

  return (
    <div style={{ 
      maxWidth: '600px', 
      margin: '4rem auto',  // Added ample margin for spacing
      padding: '2rem', 
      textAlign: 'center',
    }}>
      <h2 style={{ textAlign: 'center', color: '#D44A7A', marginBottom: '2rem' }}>
        What Our Users Say
      </h2>
      <Slider {...settings}>
        {testimonials.map((item, index) => (
          <div key={index} style={{ padding: '1rem', textAlign: 'center' }}>
            <div
              style={{
                width: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <img
                src={item.image}
                alt={`testimonial-${index}`}
                style={{
                  width: '200px',
                  height: '200px',
                  objectFit: 'cover',
                  borderRadius: '50%',
                  marginBottom: '1rem'
                }}
              />
              <p style={{ 
                fontSize: '1.125rem', 
                color: '#D44A7A', 
                maxWidth: '500px', 
                margin: '0 auto 0.5rem' 
              }}>
                “{item.text}”
              </p>
              <p style={{ fontSize: '1rem', color: '#D44A7A', margin: '0' }}>
                <em>{item.name}</em>
              </p>
            </div>
          </div>
        ))}
      </Slider>
    </div>
  );
};

export default TestimonialsCarousel;