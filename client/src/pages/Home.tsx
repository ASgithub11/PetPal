import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="home-container">
      <header className="home-header">
        <h1>Welcome to PetPal</h1>
        <p>Your trusted platform for pet adoption</p>
      </header>

      <section className="home-features">
        <h2>Why Choose PetPal?</h2>
        <div className="feature">
          <h3>Find Your Perfect Match</h3>
          <p>Every pet has a unique personality, and so do you! Our platform helps you find a pet that matches your lifestyle and preferences. From playful companions to serene cuddle buddies, your ideal pet is just a few clicks away.</p>
        </div>
        <div className="feature">
          <h3>Browse Pets from Shelters</h3>
          <p>View pets from shelters and foster homes in need of loving families.</p>
        </div>
        <div className="feature">
          <h3>Connect with Animal Welfare</h3>
          <p>We collaborate with shelters to ensure that each pet listed on PetPal has been properly cared for.</p>
        </div>
      </section>

      <section className="home-testimonials">
        <h2>What Our Users Are Saying</h2>
        <blockquote>
          "PetPal made adopting our dog so easy. We found the perfect match and couldn't be happier!"
          <footer>- Happy Pet Owner</footer>
        </blockquote>
        <blockquote>
          "The process was smooth and simple. I'm grateful for PetPal in helping me find my new best friend!"
          <footer>- Another Happy Pet Owner</footer>
        </blockquote>
      </section>

      <footer className="home-footer">
        <p>© 2024 PetPal. All Rights Reserved.</p>
      </footer>
    </div>
  );
};

export default Home;
