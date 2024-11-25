export interface PetData {
    _id: string;
    name: string;
    age: number;
    breed: string;
    description: string;
    imageUrl: string;
    favorited: boolean; // Indicates if the pet is marked as favorite by the user
}
