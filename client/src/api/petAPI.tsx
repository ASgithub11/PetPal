import type { PetData } from '../interfaces/PetData';

// Function to fetch the list of pets from the server
export const fetchPets = async (): Promise<PetData[]> => {
  // Make a request to the server endpoint '/api/pets' to get the list of all pets
  const response = await fetch('/api/pets');

  // If the server's response is not OK, throw an error
  if (!response.ok) {
    throw new Error('Failed to fetch pets');
  }
  
  // Return the response in JSON format (an array of pets)
  return response.json();
};
