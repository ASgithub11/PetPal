import { Link } from 'react-router-dom';
import Auth from '../utils/auth';

const Navbar = () => {
  const isLoggedIn = Auth.loggedIn();

  return (
    <nav className="navbar">
    <ul className='nav-links'>
      <Link to="/">Home</Link>
      <Link to="/about">About</Link>
      <Link to="/pets">Pets</Link>
      <Link to="/adoption">Adoption</Link>
    </ul>
    </nav>
  );
};

export default Navbar;
