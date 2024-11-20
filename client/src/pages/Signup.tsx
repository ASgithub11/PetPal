import { useState, type FormEvent, type ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { createUser } from '../api/userAPI'; // API function to create a new user
import type { UserData } from '../interfaces/UserData'; // Interface for user data

const Signup = () => {
  // State to manage signup form data
  const [signupData, setSignupData] = useState<UserData>({
    id: 0,
    username: '',
    email: '',
    password: '',
  });

  // The navigate function from the router to redirect the user after signup
  const navigate = useNavigate();

  // Update the form data state as the user types
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSignupData({
      ...signupData,  // Keep the existing form data
      [name]: value,  // Update only the changed field
    });
  };

  // Handle form submission
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault(); // Prevent page reload on form submission
    try {
      // Register new user through API call
      const data = await createUser(signupData);
      if (data) {
        navigate('/login'); // Redirect to login page after successful signup
      }
    } catch (err) {
      console.error('Failed to sign up', err);  // Log the error to the console
    }
  };

  // Render the signup form
  return (
    <div className='form-container'>
      <form className='form signup-form' onSubmit={handleSubmit}>
        <h1>Sign Up</h1>
        {/* Username input */}
        <div className='form-group'>
          <label>Username</label>
          <input
            className='form-input'
            type='text'
            name='username'
            value={signupData.username || ''}
            onChange={handleChange}
            required
          />
        </div>
        {/* Email input */}
        <div className='form-group'>
          <label>Email</label>
          <input
            className='form-input'
            type='email'
            name='email'
            value={signupData.email || ''}
            onChange={handleChange}
            required
          />
        </div>
        {/* Password input */}
        <div className='form-group'>
          <label>Password</label>
          <input
            className='form-input'
            type='password'
            name='password'
            value={signupData.password || ''}
            onChange={handleChange}
            required
          />
        </div>
        {/* Submit button */}
        <div className='form-group'>
          <button className='btn btn-primary' type='submit'>
            Sign Up
          </button>
        </div>
      </form>
    </div>
  );
};

export default Signup;
