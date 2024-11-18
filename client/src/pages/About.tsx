import './About.css';

const About = () => {
  return (
    <div className="about-container">
      <h1>About Us</h1>
      <p>
        Welcome to PetPal! We are dedicated to connecting pets with loving families. Our mission is to provide a reliable and user-friendly platform where users can browse available pets, learn about them, and apply for adoption. At PetPal, we believe every pet deserves a home and that the adoption process should be as smooth as possible.
      </p>
      <p>
        Our team is passionate about animal welfare and strives to create an environment where adoption becomes a positive experience for both pets and their future owners. We collaborate with shelters and foster homes to ensure every pet listed on our platform has received proper care.
      </p>
      <h2>Contact Us</h2>
      <p>
        If you have any questions or would like to get in touch with our team, please reach out to us at <a href="mailto:contact@petpal.com">contact@petpal.com</a>. We’re here to help!
      </p>
    </div>
  );
};

export default About;
