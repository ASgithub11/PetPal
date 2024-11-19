import { useEffect, useState } from 'react';
import type { PetData } from '../interfaces/PetData';
import Auth from '../utils/auth';

const Favorites = () => {
  const [favorites, setFavorites] = useState<PetData[]>([]);

  // Fetch favorites when the component mounts
  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        const response = await fetch('/api/favorites', {
          headers: {
            Authorization: `Bearer ${Auth.getToken}`,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch favorites');
        }

        const data: PetData[] = await response.json();
        setFavorites(data);
      } catch (err) {
        console.error('Error fetching favorites:', err);
      }
    };

    if (Auth.loggedIn()) {
      fetchFavorites();
    }
  }, []);

  // Handle unfavorite logic
  const unfavorite = async (petId: string) => {
    try {
      const response = await fetch(`/api/favorites/${petId}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${Auth.getToken}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to unfavorite the pet');
      }

      // Update the favorites list by removing the unfavorited pet
      setFavorites((prevFavorites: PetData[]) =>
        prevFavorites.filter((pet: PetData) => pet.id !== petId.toString())
      );
    } catch (err) {
      console.error('Error unfavoriting pet:', err);
    }
  };

  return (
    <div className="favorites-container">
      <h1>Your Favorite Pets</h1>
      {favorites.length === 0 ? (
        <p>You have no favorite pets yet.</p>
      ) : (
        <div className="favorites-grid">
          {favorites.map((pet) => (
            <div key={pet.id} className="favorite-item">
              <img src={pet.imageUrl} alt={pet.name} />
              <h2>{pet.name}</h2>
              <p>{pet.age} years old</p>
              <p>{pet.breed}</p>
              <p>{pet.description}</p>
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
