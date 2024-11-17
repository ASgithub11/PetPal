import { useEffect, useState } from 'react';
import { fetchPets } from '../api/petAPI'; // API function to fetch pets
import type { PetData } from '../interfaces/PetData'; // Pet interface

const Pets = () => {
    const [pets, setPets] = useState<PetData[]>([]);
    const [favorites, setFavorites] = useState<string[]>([]); // Array of pet IDs

    // Fetch pets on component mount
    useEffect(() => {
        const loadPets = async () => {
            try {
                const data = await fetchPets();
                setPets(data);
                const storedFavorites = JSON.parse(localStorage.getItem('favorites') || '[]');
                setFavorites(storedFavorites);
            } catch (error) {
                console.error('Failed to fetch pets:', error);
            }
        };
        loadPets();
    }, []);

    // Toggle favorite status
    const handleFavorite = async (petId: string) => {
        try {
            if (favorites.includes(petId)) {
                await removeFavorite(petId);
                setFavorites((prevFavorites) => prevFavorites.filter((id) => id !== petId));
                localStorage.setItem(
                    'favorites',
                    JSON.stringify(favorites.filter((id) => id !== petId))
                    );
                } else {
                    await addFavorite(petId);
                    setFavorites((prevFavorites) => [...prevFavorites, petId]);
                    localStorage.setItem('favorites', JSON.stringify([...favorites, petId]));
                }
            } catch (error) {
                console.error('Failed to update favorites:', error);
        }
    };

    return (
        <div className="pets-container">
            <h1>Available Pets</h1>
            {pets.length === 0 ? (
                <p>No pets available at the moment. Please check back later!</p>
                ):(
                    <div className="pets-grid">
                        {pets.map((pet) => (
                            <div className="pet-card" key={pet.id}>
                                <img src={pet.imageUrl} alt={pet.name} className="pet-image" />
                                <div className="pet-details">
                                    <h2>{pet.name}</h2>
                                    <p>Age: {pet.age}</p>
                                    <p>Breed: {pet.breed}</p>
                                </div>
                                <button className={`favorite-btn ${favorites.includes(pet.id) ? 'favorited' : ''}`} onClick={() => handleFavorite(pet.id)}>
                                    {favorites.includes(pet.id) ? '❤️' : '🤍'}
                                </button>
                            </div>
                        ))}
                    </div>
                )
            }
        </div>
    )
};

export default Pets;
