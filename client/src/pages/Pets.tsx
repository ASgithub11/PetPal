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
    