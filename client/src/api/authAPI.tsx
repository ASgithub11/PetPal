import type { UserLogin } from '../interfaces/UserLogin';

const login = async (userInfo: UserLogin) => {
  try {
    // Send a POST request to the '/auth/login' endpoint with the user's login information.
    const response = await fetch('/auth/login', {
      method: 'POST', // Send a POST request. This means we are sending data to the server
      headers: {
        'Content-Type': 'application/json',   // Tell the server we are sending data in JSON format
      },
      body: JSON.stringify(userInfo), // Convert the user's login information to a JSON string
    });

    // Get the server's response and convert it to JSON
    const data = await response.json();

    // If the server's response is not OK, throw an error
    if (!response.ok) {
      throw new Error('User information not retrieved, check network tab!');
    }

    // If all went well, return the data which is the user's information from the server
    return data;
  } catch (err) {
    // If something goes wrong, log the error to the console for debugging and return a rejected promise with an error message
    console.log('Error from user login: ', err);
    return Promise.reject('Could not fetch user info');
  }
};

export { login };
