# Blog Post API (RESTful FastAPI)
APIs developed using the Python FastAPI library for CRUD operations, stored in Postgres database, and tested with Postman to perform the following:

### User Creation
- User profile can be created and retrieved
- Password in the database is hashed

<!-- todo: update & is active | show error for duplicate email or username -->
  
### Login & Authentication
- User login and credential verification with hashed password
- JWT Bearer token is generated with expiration time per login
- Generated(valid) user token is used with (all) operations

### Post Operations
- Blog posts can be created, retrieved, updated, and deleted
> New posts, updating posts, and deleting posts are user-specific, but retrieval can be modified this way as well
- Option to use query parameters to control data responses
- User can upvote a post

### _Frameworks & Libraries_
- FastAPI: API development
- SQLAlchemy: SQL Database ORM tool for Postgres
- Bcrypt: Password hashing function (encoding & decoding)
- OAuth2: Login Authorization
- JWT: Authentication & User security*
