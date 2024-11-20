import Auth from '../utils/auth';

// Function to fetch the user's list of favorite pets
const getFavorites = async () => {
  try {
    // Make a request to the server endpoint '/api/favorites' to get the user's list of favorite pets
    const response = await fetch('/api/favorites', {
      headers: {
        'Content-Type': 'application/json', // Tell the server we are sending data in JSON format
        Authorization: `Bearer ${Auth.getToken()}`, // Attach the user's token for authentication
      },
    });

    // If the server's response is not OK, throw an error
    if (!response.ok) {
      throw new Error('Failed to fetch favorites');
    }
    // Return the list of favorite pets in JSON format
    return await response.json();
  } catch (err) {
    // If something goes wrong, log the error to the console for debugging and return an empty array
    console.error('Error retrieving favorites:', err);
    return [];
  }
};

// Function to add a pet to the user's list of favorite pets
const addFavorite = async (petId: string): Promise<void> => {
  try {
    // Send a POST request to the server endpoint '/api/favorites' to add a pet to the user's list of favorite pets
    const response = await fetch('/api/favorites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', // Tell the server we are sending data in JSON format
        Authorization: `Bearer ${Auth.getToken()}`, // Attach the user's token for authentication
      },
      body: JSON.stringify({ petId }),  // Send the pet's ID in JSON format
    });

    // If the server's response is not OK, throw an error
    if (!response.ok) {
      throw new Error('Failed to add favorite');
    }
  } catch (err) {
    // Log the error to the console for debugging
    console.error('Error adding favorite:', err);
  }
};

// Function to remove a pet from the user's list of favorite pets
const removeFavorite = async (petId: string) => {
  try {
    // Send a DELETE request to the server to remove the pet from favorites
    const response = await fetch(`/api/favorites/${petId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${Auth.getToken()}`, // Attach the user's token for authentication
      },
    });

    // If the server's response is not OK, throw an error
    if (!response.ok) {
      throw new Error('Failed to remove favorite');
    }
  } catch (err) {
    // Log the error to the console
    console.error('Error removing favorite:', err);
  }
};

// Export the functions to be used in other files
export { getFavorites, addFavorite, removeFavorite };
