import { useEffect, useState } from 'react';
import { fetchPets } from '../api/petAPI'; // API function to fetch pets
import { addFavorite, removeFavorite } from '../api/favoritesAPI'; // API functions to handle favorites
import type { PetData } from '../interfaces/PetData'; // Pet interface
import Auth from '../utils/auth';

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
    }, []); // Empty dependency array ensures the effect runs only once on mount
    
    // Handle adding or removing a pet from favorites
    const handleFavorite = async (petId: string) => {
        try {
            if (favorites.includes(petId)) {
                // If the pet is already favorited, remove it from favorites
                await removeFavorite(petId);    // Call the removeFavorite API function to remove the pet
                setFavorites((prevFavorites) => prevFavorites.filter((id) => id !== petId)); // Update the favorites state
                localStorage.setItem(
                    'favorites',
                    JSON.stringify(favorites.filter((id) => id !== petId))
                    );
                } else {
                    // If the pet is not favorited, add it to favorites
                    await addFavorite(petId);   // Call the addFavorite API function to add the pet
                    setFavorites((prevFavorites) => [...prevFavorites, petId]); // Update the favorites state
                    localStorage.setItem('favorites', JSON.stringify([...favorites, petId]));   // Update the local storage
                }
            } catch (error) {
                console.error('Failed to update favorites:', error);    // Log the error to the console
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
                            <div className="pet-card" key={pet._id}>
                                {/* Display the pet's image */}
                                <img src={pet.imageUrl} alt={pet.name} className="pet-image" />
                                {/* Display the pet's details */}
                                <div className="pet-details">
                                    <h2>{pet.name}</h2>
                                    <p>Age: {pet.age}</p>
                                    <p>Breed: {pet.breed}</p>
                                </div>
                                {/* Button to toggle the favorite status */}
                                <button className={`favorite-btn ${favorites.includes(pet._id) ? 'favorited' : ''}`} onClick={() => handleFavorite(pet._id)}>
                                    {/* Show a heart icon depending on the favorite status */}
                                    {favorites.includes(pet._id) ? '❤️' : '🤍'}
                                </button>
                            </div>
                        ))}
                    </div>
                )
            ) : (
                <p>Please login to see available pets.</p>
            )}
        </div>
    )
};

export default Pets;
