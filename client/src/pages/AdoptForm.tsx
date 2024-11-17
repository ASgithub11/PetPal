import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

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
  