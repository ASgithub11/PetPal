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

    