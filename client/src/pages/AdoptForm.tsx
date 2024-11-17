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

  