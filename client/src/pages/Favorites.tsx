import { useEffect, useState } from 'react';
import { motion } from 'motion/react';
import { fetchPets } from '../api/petAPI';
import { addFavorite, removeFavorite } from '../api/favoritesAPI';
import type { PetData } from '../interfaces/PetData';
import Auth from '../utils/auth';
import './pet.css';

const Favorites = () => {
  // Initialize the state to store the user's favorite pets
  const [favorites, setFavorites] = useState<string[]>([]);
  const [pets, setPets] = useState<PetData[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  // Fetch the user's favorite pets when the component mounts
  useEffect(() => {
    const loadFavorites = async () => {
      try {
        if (isLoggedIn) {
          // Fetch the list of all pets
          const data = await fetchPets();
          setPets(data);

          // Get the stored favorite pet IDs from local storage
          const storedFavorites = JSON.parse(localStorage.getItem('favorites') || '[]');
          setFavorites(storedFavorites);
        }
      } catch (error) {
        console.error('Failed to fetch pets:', error);
      }
    };

    setIsLoggedIn(Auth.loggedIn());
    loadFavorites();
  }, [isLoggedIn]);

  const favoritePets = pets.filter((pet) => favorites.includes(pet._id));

  // Handle adding or removing a pet from favorites (same as in Pets component)
  const handleFavorite = async (petId: string, swipeRight: boolean) => {
    try {
      if (swipeRight) {
        // Add to favorites
        await addFavorite(petId);
        setFavorites((prev) => [...prev, petId]);
        localStorage.setItem('favorites', JSON.stringify([...favorites, petId]));
      } else {
        // Remove from favorites
        await removeFavorite(petId);
        setFavorites((prev) => prev.filter((id) => id !== petId));
        localStorage.setItem('favorites', JSON.stringify(favorites.filter((id) => id !== petId)));
      }
    } catch (error) {
      console.error('Failed to update favorites:', error);
    }
  };

  // Render the list of favorite pets
  return (
    <div className="pets-container">
      <h1>Your Favorite Pets</h1>
      {isLoggedIn ? (
        favoritePets.length === 0 ? (
          <p>You have no favorite pets yet. Start favoriting some!</p>
        ) : (
          <div className="pets-grid">
            {favoritePets.map((pet) => (
              <motion.div
                key={pet._id}
                className="pet-card"
                drag="x"
                dragConstraints={{ left: 0, right: 0 }}
                onDragEnd={(_event, info) => {
                  if (info.offset.x > 100) {
                    // Swipe right to add to favorites
                    handleFavorite(pet._id, true);
                  } else if (info.offset.x < -100) {
                    // Swipe left to remove from favorites
                    handleFavorite(pet._id, false);
                  }
                }}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0 }}
                whileTap={{ scale: 0.95 }}
              >
                <img src={pet.image_url} alt={pet.name} className="pet-image" />
                <div className="pet-details">
                  <h2>{pet.name}</h2>
                  <p>Age: {pet.age}</p>
                  <p>Breed: {pet.breed}</p>
                </div>
                <div className="favorite-status">
                  {favorites.includes(pet._id) ? '❤️' : '🤍'}
                </div>
              </motion.div>
            ))}
          </div>
        )
      ) : (
        <p>Please log in to see your favorite pets.</p>
      )}
    </div>
  );
};

export default Favorites;
