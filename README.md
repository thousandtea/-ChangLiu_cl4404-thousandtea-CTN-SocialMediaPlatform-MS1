# CTN-SocialMediaPlatform-MS1-User 
This microservice is a part of the CTN Social Media Platform and handles user-related operations. 
## Setup Instructions 
Before running the service, ensure all dependencies are installed: 
``` pip install -r requirements.txt ``` 
## Initial Database Setup 
1. Run ```database_init.py``` to create the required schema and tables in your database. 
2. Update the database connection settings in ```main.py``` and ```database_init.py``` to match your local setup. 
## Running the Service 
Start the service with: ``` python main.py ``` 
The FastAPI server will typically be accessible at ```http://localhost:8012```. 

# API Usage 
## User Creation via Google OAuth2 
User accounts are automatically created upon their first login through Google OAuth2. 
The login flow is initiated at: ``` GET /auth/login ``` 
This endpoint redirects to Google's OAuth2 service for user authentication. Upon successful authentication, the user is redirected back to the specified callback URL ```(/auth/callback)```, where their account is created. 

## Example to CURL 
Here are some example ```curl``` commands for interacting with the API: 
### Get User 
1. Get all users: 
``` 
curl -X GET "http://localhost:8012/api/users" 
``` 
2. Get a specific user by email: 
``` 
curl -X GET "http://localhost:8012/api/users/{email}" 
``` 
### Update a User (Admin Only) 
``` 
curl -X PUT "http://localhost:8012/api/users/{email}" \ -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN" \ -H "Content-Type: application/json" \ -d '{"new_username": "updated_username"}' 
``` 
### Delete a User (Admin Only) 
``` 
curl -X DELETE "http://localhost:8012/api/users/{email}" \ -H "Authorization: Bearer YOUR_ADMIN_JWT_TOKEN" 
```