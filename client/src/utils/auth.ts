// Importing specific types and functions from the 'jwt-decode' library.
// JwtPayload: A type definition representing the structure of a JSON Web Token payload.
// jwtDecode: A function used to decode a JSON Web Token (JWT) and extract its payload.
import { type JwtPayload, jwtDecode } from 'jwt-decode';

// Extending the JwtPayload type to include additional data fields specific to the application.
interface ExtendedJwt extends JwtPayload {
  data:{
    id: number;
    username: string;
    email: string;
  };
}

class AuthService {
  // This method decodes the JWT token to get the user's profile information.
  getProfile() {
    // jwtDecode is a function that is used to decode the JWT token and return its payload.
    return jwtDecode<ExtendedJwt>(this.getToken());
  }

  // This method checks if the user is logged in by verifying the presence and validity of the JWT token.
  loggedIn() {
    const token = this.getToken();
    // Returns true if the token exists and is not expired.
    return !!token && !this.isTokenExpired(token);
  }

  // This method checks if the provided token is expired.
  isTokenExpired(token: string) {
    try {
      // jwtDecode decodes the token to check its expiration date.
      const decoded = jwtDecode<JwtPayload>(token);

      // Check if the decoded token has an 'exp' (expiration) property and if it is less than the current time in seconds.
      if (decoded?.exp && decoded?.exp < Date.now() / 1000) {
        // If the token is expired, return true indicating that it is expired.
        return true;
      }
    } catch (err) {
      // If decoding fails (e.g., due to an invalid token format), catch the error and return false.
      return false;
    }
  }

  // This method retrieves the JWT token from local storage.
  getToken(): string {
    const loggedUser = localStorage.getItem('id_token') || '';
    // Returns the token stored in local storage.
    return loggedUser;
  }

  // This method logs in the user by storing the JWT token in local storage and redirecting to the home page.
  login(idToken: string) {
    localStorage.setItem('id_token', idToken);
    window.location.assign('/');
  }

  // This method logs out the user by removing the JWT token from local storage and redirecting to the home page.
  logout() {
    localStorage.removeItem('id_token');
    window.location.assign('/');
  }
}

export default new AuthService();
