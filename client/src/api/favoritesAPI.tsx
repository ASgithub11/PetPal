import Auth from '../utils/auth';

// To get favorites
const getFavorites = async () => {
  try {
    const response = await fetch('/api/favorites', {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${Auth.getToken()}`,
      },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch favorites');
    }
    return await response.json();
  } catch (err) {
    console.error('Error retrieving favorites:', err);
    return [];
  }
};

export { getFavorites };
