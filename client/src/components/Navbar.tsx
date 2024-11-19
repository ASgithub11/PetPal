import { Link } from 'react-router-dom';
import Auth from '../utils/auth';
import PetPalLogo from '../assets/images/PetPalLogo.png';
import './Navbar.css';

const Navbar = () => {
  const isLoggedIn = Auth.loggedIn();

  return (
    <nav className="navbar">
      <img className='logo' src={PetPalLogo} alt="PetPal Logo" />
      <ul className='nav-links'>
        <Link to="/">Home</Link>
        <Link to="/about">About</Link>
        <Link to="/pets">Pets</Link>
        <Link to="/adoption">Adoption</Link>
        {isLoggedIn && <Link to="/favorites">Favorites</Link>}
        {isLoggedIn ? (
        <button onClick={() => Auth.logout()}>Logout</button>
        ) : (
        <Link to="/login">Login</Link>
        )}
        <Link to="/signup">Signup</Link>
      </ul>
    </nav>
  );
};

export default Navbar;
