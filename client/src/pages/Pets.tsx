import { useEffect, useState } from 'react';
import { motion } from 'motion/react';
import { fetchPets } from '../api/petAPI'; // API function to fetch pets
import { addFavorite, removeFavorite } from '../api/favoritesAPI'; // API functions to handle favorites
import type { PetData } from '../interfaces/PetData'; // Pet interface
import Auth from '../utils/auth';
import './pet.css'; 

const Pets = () => {
    // Initialize state to store the list of pets and the IDs of user's favorite pets
    const [pets, setPets] = useState<PetData[]>([]);
    const [favorites, setFavorites] = useState<string[]>([]);
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    
    // Fetch the list of pets and any saved favorites when component mounts
    useEffect(() => {
        const loadPets = async () => {
            try {
                if (isLoggedIn) {
                // Fetch the list of pets
                const data = await fetchPets();
                setPets(data);  // Update the state with the list of fetched pets

                // Load the user's favorite pets from local storage
                const storedFavorites = JSON.parse(localStorage.getItem('favorites') || '[]');
                setFavorites(storedFavorites);
                }
            } catch (error) {
                console.error('Failed to fetch pets:', error);  // Log the error to the console
            }
        };
        setIsLoggedIn(Auth.loggedIn());
        loadPets(); // Call the loadPets function to fetch pets
    }, [isLoggedIn]); // Add 'isLoggedIn' to the dependency array
    
    // Handle adding or removing a pet from favorites
    const handleFavorite = async (petId: string, swipeRight: boolean) => {
        try {
            if (swipeRight) {
                await addFavorite(petId);
                setFavorites((prev) => [...prev, petId]);
                localStorage.setItem('favorites', JSON.stringify([...favorites, petId]));
            } else {
                await removeFavorite(petId);
                setFavorites((prev) => prev.filter((id) => id !== petId));
                localStorage.setItem('favorites', JSON.stringify(favorites.filter((id) => id !== petId)));
            }
        } catch (error) {
            console.error('Failed to update favorites:', error);
        }
    };
    
    // Render the list of pets with favorite buttons
        return (
            <div className="pets-container">
                <h1>Available Pets</h1>
            {isLoggedIn ? (pets.length === 0 ? (
                // Display a message if no pets are available
                <p>No pets available at the moment. Please check back later!</p>
                ):(
                    // Display a grid of pet cards if pets are available
                    <div className="pets-grid">
                        {pets.map((pet) => (
                            <motion.div 
                                key={pet._id}
                                className="pet-card"
                                drag="x"
                                dragConstraints={{ left: 0, right: 0 }}
                                onDragEnd={(event, info) => {
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
                                <img src={pet.imageUrl} alt={pet.name} className="pet-image" />
                                {/* Display the pet's details */}
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
                <p>Please login to see available pets.</p>
            )}
        </div>
    );
};


export default Pets;
