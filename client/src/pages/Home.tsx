import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Welcome to PetPal</h1>
      </header>

      <h2>Why Choose PetPal?</h2>
        <div className="feature">
          <h3>Find Your Perfect Match</h3>
          <p>Every pet has a unique personality, and so do you! Our platform helps you find a pet that matches your lifestyle and preferences. From playful companions to serene cuddle buddies, your ideal pet is just a few clicks away.</p>
        </div>
    </div>
  );
};

export default Home;
