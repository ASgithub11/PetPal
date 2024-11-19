import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './AdoptForm.css';

const AdoptForm = () => {
  const { petId } = useParams<{ petId: string }>(); // Get the pet ID from the URL
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
  });
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch('/api/adopt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ...formData, petId }),
      });

      if (response.ok) {
        setIsSubmitted(true);
        setTimeout(() => navigate('/'), 3000); // Redirect after 3 seconds
      } else {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Something went wrong');
      }
    } catch (err) {
      console.error('Error submitting adoption form:', err);
      setError('Failed to submit the form. Please try again.');
    }
  };

  if (isSubmitted) {
    return (
      <div className="form-container">
        <h1>Thank You!</h1>
        <p>Your adoption application for Pet ID: {petId} has been submitted successfully.</p>
      </div>
    );
  }

  return (
    <div className="form-container">
      <form className="form adopt-form" onSubmit={handleSubmit}>
        <h1>Adopt a Pet</h1>
        {error && <p className="error-message">{error}</p>}
        <div className="form-group">
          <label>Name</label>
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
          <textarea
            name="message"
            value={formData.message}
            onChange={handleChange}
            rows={4}
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Submit Application
        </button>
      </form>
    </div>
  );
};

export default AdoptForm;
