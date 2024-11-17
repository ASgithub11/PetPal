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

// To add a favorite
const addFavorite = async (petId: string): Promise<void> => {
  try {
    const response = await fetch('/api/favorites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${Auth.getToken()}`,
      },
      body: JSON.stringify({ petId }),
    });
    if (!response.ok) {
      throw new Error('Failed to add favorite');
    }
  } catch (err) {
    console.error('Error adding favorite:', err);
  }
};

// To remove a favorite
const removeFavorite = async (petId: string) => {
  try {
    const response = await fetch(`/api/favorites/${petId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${Auth.getToken()}`,
      },
    });
    if (!response.ok) {
      throw new Error('Failed to remove favorite');
    }
  } catch (err) {
    console.error('Error removing favorite:', err);
  }
};

export { getFavorites, addFavorite, removeFavorite };
