import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './AdoptForm.css';
import auth from '../utils/auth';

const AdoptForm = () => {
  // Get the pet ID from the URL 
  const { petId } = useParams<{ petId: string }>(); 
  const navigate = useNavigate(); // Use navigate to redirect the user after form submission
  const isLoggedIn = auth.loggedIn();

  // State to manage form inputs
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
  });

  const [isSubmitted, setIsSubmitted] = useState(false); // Tract if the form is submitted
  const [error, setError] = useState<string | null>(null); // Track any errors during form submission

  // Handle form input changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target; // Get the field name and value
    setFormData((prevData) => ({
      ...prevData,  // Keep the existing form fields unchanged
      [name]: value,  // Update the specific field that changed
    }));
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent the page from reloading
    setError(null); //Clear any existing errors

    try {
      // Send the form data to the server
      const response = await fetch('/api/adopt', {
        method: 'POST', // The request method is POST
        headers: {
          'Content-Type': 'application/json', // The content type is JSON
        },
        body: JSON.stringify({ ...formData, petId }), // Include form data and pet ID in the request body
      });

      if (response.ok) {
        setIsSubmitted(true); // Mark form as submitted
        setTimeout(() => navigate('/'), 3000); // Redirect the user to homepage after 3 seconds
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Something went wrong');
      }
    } catch (err) {
      // Console log error and display an error message to the user
      console.error('Error submitting adoption form:', err);
      setError('Failed to submit the form. Please try again.');
    }
  };

  // If the form is submitted successfully, show a success message
  if (isSubmitted) {
    return (
      <div className="form-container">
        <h1>Thank You!</h1>
        <p>Your adoption application for Pet ID: {petId} has been submitted successfully.</p>
      </div>
    );
  }
  
  // Render the adoption form
  return (
    <div className="form-container">
      {isLoggedIn ? (
      <form className="form adopt-form" onSubmit={handleSubmit}>
        <h1>Adopt a Pet</h1>
        {/* Display error message */}
        {error && <p className="error-message">{error}</p>}
        <div className="form-group">
          <label>Name</label>
          {/* Input field for the user's name */}
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Email</label>
          {/* Input field for the user's email */}
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Phone</label>
          {/* Input field for the user's phone number */}
          <input
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Message</label>
          {/* Textarea for the user to write a message(optional) */}
          <textarea
            name="message"
            value={formData.message}
            onChange={handleChange}
            rows={4}
          />
        </div>
        {/* Submit button */}
        <button type="submit" className="btn btn-primary">
          Submit Application
        </button>
      </form>
      ) : (
        <div className="login-prompt">
          <p>Please log in to submit an application.</p>
        </div>
      )}
    </div>
  );
};

export default AdoptForm;
