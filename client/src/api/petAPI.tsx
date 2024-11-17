import type { PetData } from '../interfaces/PetData';

export const fetchPets = async (): Promise<PetData[]> => {
  const response = await fetch('/api/pets');
  if (!response.ok) {
    throw new Error('Failed to fetch pets');
  }
  return response.json();
};
