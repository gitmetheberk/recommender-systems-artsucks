### Starting backend server locally
1. Open a cmd/terminal and ensure pipenv is installed
2. Navigate to the backend directory for the repository and run "pipenv install" (It should automatically locate Pipfile.lock and install all the required packages)
3. Run "pipenv shell" to enter the shell
4. Run "python manage.py runserver" in the shell to start the server

### Interesting code locations:
* Code to generate reports can be found in artrec/admin.py
* Code that maintain's the user's feature profile can be found in artrec/models.py
* Code that generates and returns recommendations can be found in artrec/views.py
