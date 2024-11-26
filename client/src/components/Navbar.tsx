import { Link } from 'react-router-dom';
import Auth from '../utils/auth';
import PetPalLogo from '../assets/images/PetPalLogo.png';
import './Navbar.css';
import { useState } from 'react';

const Navbar = () => {
  const isLoggedIn = Auth.loggedIn();
  const [menuOpen, setMenuOpen] = useState(false); 
  const toggleMenu = () => {
    setMenuOpen((prevState) => !prevState); // Toggle the menu open/close
  };
  const closeMenu = () => {
    setMenuOpen(false); // Close the menu
  };

  return (
    <nav className="navbar">
      <img className='logo' src={PetPalLogo} alt="PetPal Logo" />
      <div className="menu-icon" onClick={toggleMenu}>
        ☰
      </div>
      <ul className={`nav-links ${menuOpen ? 'open' : ''}`}>
        <Link to="/"onClick={closeMenu}>Home</Link>
        <Link to="/about"onClick={closeMenu}>About</Link>
        <Link to="/pets"onClick={closeMenu}>Pets </Link>
        <Link to="/adoption"onClick={closeMenu}>Adoption</Link>
        {isLoggedIn && <Link to="/favorites"onClick={closeMenu}>Favorites</Link>}
        {isLoggedIn ? (
        <button onClick={() => Auth.logout()}>Logout</button>
        ) : (
        <Link to="/login"onClick={closeMenu}>Login</Link>
        )}
        <Link to="/signup"onClick={closeMenu}>Signup</Link>
      </ul>
    </nav>
  );
};

export default Navbar;
