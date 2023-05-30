# Backend for Web-Based Advertisement Platform

### Tech task

The project task is to develop a backend for a classified ads web application. This platform necessitates the capacity for authorized users to create ads, while ad viewing functionality should not be restricted to authorization.  
Additionally, safeguards must be put in place to ensure that ads cannot be falsely created on behalf of others. A regulation should be implemented that restricts users to no more than ten open ads concurrently.  
Ads on the platform will feature two statuses: OPEN and CLOSED. The backend should facilitate updates and deletions of ads by their original creators only. Alongside this, an administration function should be introduced, enabling administrators to edit or delete any ad as required.  
A favorites feature should be incorporated as well, allowing users to mark specific ads as favorites for easy access.  
The backend should also provide filtration capabilities for ads based on their status and date of creation, to be utilized by the frontend.  
A separate draft status should be implemented. This status renders the ad visible only to its creator, effectively hiding it from other users until the status is changed.  
In terms of system security, rate limits are to be enforced to protect against potential bot activity and malicious usage. Specifically, non-authorized users should be limited to 10 requests per minute, with authorized users permitted up to 20 requests per minute.  

### Realization features
**Advertisements:** The Advertisement model is defined in the models.py file, which includes fields for title, description, status, creator, created_at, updated_at, and a draft boolean field. Advertisement statuses are defined in the AdvertisementStatusChoices class with options for OPEN and CLOSED. The draft field is used to mark an advertisement as a draft, making it visible only to the creator.  
**Advertisement Creation:** In the serializers.py, the AdvertisementSerializer redefines the create method where the creator is automatically set to the current authenticated user. Meanwhile, a validation method checks the number of open ads created by the user and throws a validation error if the user has reached the limit of 10 open advertisements.  
**Favorites:** A Favorite model is also defined in the models.py, which represents a many-to-many connection between a User and an Advertisement. The FavoriteSerializer in the serializers.py file provides the methods for serializing the data of a Favorite instance. The representation of favorites differ, depending on whether a stuff user requests the data or an ordinary authenticated user, allowing admins to see all of the user-adverisement pairs, while a user can only operate his own favorites list. When a Favorite is created, the serializer checks if the advertisement is already in the user's favorites and raises a validation error if it is.  
**Permissions:** In the views.py file, the AdvertisementViewSet and FavoriteViewSet classes define the permissions required for different actions. The AdvertisementViewSet includes a get_permissions method that checks if the authenticated user is the ad's creator before allowing update or deletion actions. This method also allows admins to gain unlimitted access to all entries.  
The use of Django's Q objects in the AdvertisementViewSet's get_queryset method allows complex database queries, enabling the function to return different querysets based on whether the user is staff, anonymous, or a regular authenticated user. This is an example of how the project provides a different level of access based on user type.  
**Database:** The project uses PostgreSQL as its database, as specified in the settings.py file. The credentials for the database are fetched from environment variables for improved security.  
Additionally, the implementation uses the TokenAuthentication class from Django Rest Framework for authentication, which provides secure, token-based authentication for the application's users.  
**Rate Limits:** Request rate limiting is set in the settings.py file using Django Rest Framework's throttle classes. Non-authorized users are limited to 10 requests per minute, and authorized users are limited to 20 requests per minute.  

### Setup and Run

To set up and run follow standard instruction for a Django app:
- Clone the Repository: The project is stored in a git repository, you will need to clone it to your local system.
- Virtual Environment: Create a virtual environment using Python's venv module or a tool like virtualenv. This isolates the dependencies for the project.
- Install Dependencies: With your virtual environment activated, install the project's dependencies. They are listed in requirements.txt file. You can install them with 'pip install -r requirements.txt'.
- Set Up .env: Rename .env (example) to .env and fill in your environment variables. These will include things like your SECRET_KEY, database information, etc.
- Database Setup: Create your database. Ensure that the database settings in your .env file match your actual database setup.
- Run Migrations: Django uses migrations to manage database schema. You can apply these with 'python manage.py migrate'.
- Run the Server: Finally, you can run your server with 'python manage.py runserver'. By default, this will start the server on localhost:8000.

This setup assumes a development environment. For a production deployment, you will need to follow the standard procedures for your specific production environment. This usually involves setting up a production-ready web server like Gunicorn or uWSGI, setting up a reverse proxy like Nginx, and securing your application. For more information, refer to the Django deployment checklist.
Set Up for Testing

The application offers a unique feature for setting up the environment for a quick testing, to check the application features:
- Create Test Users: Run 'python manage.py create_test_users'. This command will automatically create several test users and an admin user, saving their authentication tokens to the http-client.env.json file for use with HTTP clients.
- Connect Virtual Environment for your http-client: In your HTTP client, connect to the 'dev' virtual environment from the http-client.env.json file. The method to do this may vary depending on your client. Generally, this can be done through a setting or command such as @env http-client.env.json.
- Maintain Request Order: When running the requests in request-examples.http, it's important to maintain the order of execution. Some requests depend on the state of the application after previous requests.  
Throttling and Constraints Checks: The request-examples.http file includes requests designed to check rate limiting (throttling) and constraints on the number of 'OPEN' advertisements. Please follow the comments in the file to execute these tests correctly.

Note: With these steps, there's no need to manually create users through the Django admin interface, making the setup process smoother and easier to automate. This unique setup feature allows for robust, thorough testing of the application's functionality, ensuring the quality and reliability of your application.
