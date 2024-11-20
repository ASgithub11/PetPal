import { useEffect, useState } from 'react';
import type { PetData } from '../interfaces/PetData';
import Auth from '../utils/auth';

const Favorites = () => {
  // Initialize the state to store the user's favorite pets
  const [favorites, setFavorites] = useState<PetData[]>([]);

  // Fetch the user's favorite pets when the component mounts
  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        // Make a GET request to fetch the favorites
        const response = await fetch('/api/favorites', {
          headers: {
            Authorization: `Bearer ${Auth.getToken}`, // Attach the user's token for authentication
          },
        });

        // If the server's response is not OK, throw an error
        if (!response.ok) {
          throw new Error('Failed to fetch favorites');
        }

        // Get the data in JSON format
        const data: PetData[] = await response.json();
        setFavorites(data); // Update the state with the user's favorite pets
      } catch (err) {
        console.error('Error fetching favorites:', err);  // Log the error to the console
      }
    };

    // Only fetch the favorites if the user is logged in
    if (Auth.loggedIn()) {
      fetchFavorites();
    }
  }, []); // Empty dependency array ensures the effect runs only once on mount

  // Function to handle remving a pet from favorites
  const unfavorite = async (petId: string) => {
    try {
      // Make a DELETE request to remove the pet from favorites
      const response = await fetch(`/api/favorites/${petId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${Auth.getToken}`, // Attach the user's token for authentication
        },
      });

      // If the server's response is not OK, throw an error
      if (!response.ok) {
        throw new Error('Failed to unfavorite the pet');
      }

      // Update the favorites list by removing the unfavorited pet
      setFavorites((prevFavorites: PetData[]) =>
        prevFavorites.filter((pet: PetData) => pet.id !== petId.toString())
      );
    } catch (err) {
      console.error('Error unfavoriting pet:', err); // Log the error to the console
    }
  };

  // Render the component
  return (
    <div className="favorites-container">
      <h1>Your Favorite Pets</h1>
      {/* Display a message if there are no favorites */}
      {favorites.length === 0 ? (
        <p>You have no favorite pets yet.</p>
      ) : (
        <div className="favorites-grid">
          {/* Display each favortie pet */}
          {favorites.map((pet) => (
            <div key={pet.id} className="favorite-item">
              <img src={pet.imageUrl} alt={pet.name} /> {/* Display the pet's image */}
              <h2>{pet.name}</h2>
              <p>{pet.age} years old</p>
              <p>{pet.breed}</p>
              <p>{pet.description}</p>
              {/* Button to remove the pet from favorites */}
              <button
                className="btn btn-danger"
                onClick={() => unfavorite(pet.id)}
              >
                Remove
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Favorites;
