import { useState, type FormEvent, type ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import Auth from '../utils/auth';
import { login } from '../api/authAPI';
import type { UserLogin } from '../interfaces/UserLogin';
import './Login.css';

const Login = () => {
  // State to manage login form data
  const [loginData, setLoginData] = useState<UserLogin>({
    username: '', // Initialize username as empty strings
    password: '', // Initialize password as empty strings
  });

  // The navigate function from the router to redirect the user after login
  const navigate = useNavigate();

  // Handle changes to the form input fields
  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target; // Get the field name and value from the event
    setLoginData({
      ...loginData, // Keep the existing form data
      [name]: value,  // Update only the changed field
    });
  };

  // Handle form submission
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault(); // Prevent the default form submission behavior
    try {
      // Call the login API with the form data
      const data = await login(loginData);

      Auth.login(data.token); // Store the token in local storage
      navigate('/');  // Redirect to home page after successful login
    } catch (err) {
      console.error('Failed to login', err);  // Log the error to the console and show an alert
      alert('Login failed. Please check your credentials and try again.');
    }
  };

  // Render the login form
  return (
    <div className='form-container'>
      <form className='form login-form' onSubmit={handleSubmit}>
        <h1>Login</h1>
        <div className='form-group'>
          {/* Username input field */}
          <label>Username</label>
          <input
            className='form-input'
            type='text'
            name='username'
            value={loginData.username || ''}
            onChange={handleChange}
            required
          />
        </div>
        <div className='form-group'>
          {/* Password input field */}
          <label>Password</label>
          <input
            className='form-input'
            type='password'
            name='password'
            value={loginData.password || ''}
            onChange={handleChange}
            required
          />
        </div>
        <div className='form-group'>
          {/* Submit button */}
          <button className='btn btn-primary' type='submit'>
            Login
          </button>
        </div>
      </form>
    </div>
  );
};

export default Login;
