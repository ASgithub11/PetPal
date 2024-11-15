import { useState, type FormEvent, type ChangeEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { createUser } from '../api/userAPI';
import Auth from '../utils/auth';
import type { UserData } from '../interfaces/UserData';

const Signup = () => {
  const [signupData, setSignupData] = useState<UserData>({
    username: '',
    email: '',
    password: '',
  });

  const navigate = useNavigate();

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSignupData({
      ...signupData,
      [name]: value,
    });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      // Register new user through API call
      const data = await createUser(signupData);
      if (data.token) {
        Auth.login(data.token);
        navigate('/login'); // Redirect to login page after successful signup
      }
    } catch (err) {
      console.error('Failed to sign up', err);
    }
  };

  return (
    <div className='form-container'>
      <form className='form signup-form' onSubmit={handleSubmit}>
        <h1>Sign Up</h1>
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
