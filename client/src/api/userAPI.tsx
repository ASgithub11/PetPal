import Auth from '../utils/auth';
import type { UserData } from '../interfaces/UserData';

// Retrieve all users from the server
const retrieveUsers = async () => {
  try {
    // Send a Get request to the server endpoint '/api/users' to get all users
    const response = await fetch('/api/users', {
      headers: {
        'Content-Type': 'application/json', // The content type is JSON
        Authorization: `Bearer ${Auth.getToken()}`, // Attach the user's token for authentication
      },
    });

    // Get the server's response and convert it to JSON
    const data = await response.json();

    // If the server's response is not OK, throw an error
    if (!response.ok) {
      throw new Error('invalid user API response, check network tab!');
    }

    // Return the data (array of users)
    return data;
  } catch (err) {
    // Log the error to console and return an empty array
    console.log('Error from data retrieval:', err);
    return [];
  }
};

// Retrieve a specific user by their ID
const retrieveUser = async (id: number): Promise<UserData> => {
  try {
    // Send a Get request to the server '/api/users/:id' endpoint
    const response = await fetch(`/api/users/${id}`, {
      headers: {
        'Content-Type': 'application/json', // The content type is JSON
        Authorization: `Bearer ${Auth.getToken()}`, // Attach the user's token for authentication
      },
    });

    // Get the server's response and convert it to JSON
    const data = await response.json();

    // If the server's response is not OK, throw an error
    if (!response.ok) {
      throw new Error('invalid user API response, check network tab!');
    }

    // Return the data (user information)
    return data;
  } catch (err) {
    // Console log the error and return a rejected promise with an error message
    console.log('Error from data retrieval:', err);
    return Promise.reject('Could not fetch user');
  }
};

// create a new user
const createUser = async (userData: UserData): Promise<UserData> => {
  try {
    // Send a POST resquest to the server '/api/users' endpoint with the new user's information
    const response = await fetch('/api/users', {
      method: 'POST', // The request method is POST
      headers: {
        'Content-Type': 'application/json', // The content type is JSON
        Authorization: `Bearer ${Auth.getToken()}`, // Attach the user's token for authentication
      },
      body: JSON.stringify(userData), // Convert the user's information to a JSON string
    });

    // Get the server's response and convert it to JSON
    const data = await response.json();

    // If the server's response is not OK, throw an error
    if (!response.ok) {
      throw new Error('invalid user API response, check network tab!');
    }

    // Return the data (new user information)
    return data;
  } catch (err) {
    // Console log the error and return a rejected promise with an error message
    console.log('Error from user creation:', err);
    return Promise.reject('Could not create user');
  }
};

// Export the functions to be used in other files
export { retrieveUsers, retrieveUser, createUser };
