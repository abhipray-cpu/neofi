# Notes App API

This API provides functionality for managing user accounts and notes.

## Endpoints

### User Registration
- **Endpoint:** POST user/signup
- **Functionality:** Allows users to create an account by providing necessary information such as username, email, and password.
- **Output:** 
  - If the registration is successful, return a success message or status code.
  - If there are validation errors or the username/email is already taken, return appropriate error messages or status codes.

### User Login
- **Endpoint:** POST user/login
- **Functionality:** Allows users to log in to their account by providing their credentials (username/email and password).
- **Output:** 
  - If the login is successful, return an authentication token or a success message with the user details.
  - If the credentials are invalid, return an error message or status code.

### Create new note
- **Endpoint:** POST /notes/create
- **Functionality:** Create a new note, only authenticated users can create a new note.
- **Note:** note owner needs to be stored in the db. Because notes are shareable. 
- **Output:** 
  - If the request is valid, return a success message with status code.
  - If the request is invalid, return an error message or status code.

### Get a note
- **Endpoint:** GET /notes/{id}
- **Functionality:** GET a note by its id. Only authenticated users. A note is viewable by its owner and the shared users only.
- **Output:** 
  - If the request is valid, return a success message with the note content. 
  - If the request is invalid, return an error message with status code.

### Share a note
- **Endpoint:** POST /notes/share
- **Functionality:** Share a note with other users. You can parse multiple users in this request. Once the note admin executes this POST api, the users embedded in the request body will be able to view and edit the note.
- **Output:** 
  - If the request is valid, return a success message with the appropriate status code.
  - If the request is invalid, return an error message or status code.

### Update a note
- **Endpoint:** PUT /notes/{id}
- **Functionality:** The note will be editable by admin, and all the shared users. All the users who have access to the note will be able to perform an edit anywhere on the note. For the sake of simplicity, let’s assume no existing sentences can be edited. But new sentences can be added in between existing lines of the note. All the updates to the notes need to be tracked with a timestamp, and stored somewhere.
- **Output:** 
  - If the request is valid, return a success message with the appropriate status code.
  - If the request is invalid, return an error message or status code.

### Get note version history
- **Endpoint:** GET notes/version-history/{id}
- **Functionality:** Accessible by users having access only. GET the version history of the note. This includes all the changes made to the note, since it has been created. The response will contain a list of timestamp, user who made the change, and the changes made to the
