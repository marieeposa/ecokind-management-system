# ecokind-management-system

The proposed system, developed in collaboration with Ecokind’s management, is designed to automate and streamline their key business processes. Following an initial interview with the company's owner and key staff members, we gathered insights into their operational workflows. These include inventory management, supplier coordination, sales order processing, and customer relationship management. The system will feature modules for Products, Suppliers, Sales Orders, Purchase Orders, Logistics, Invoices, Staff, and Customers.

**Install Python**

For Windows
- Go to the Python download page (https://www.python.org/downloads/).
- Click on "Download Python 3.x.x" (the latest version).
- Run the installer and check the box that says "Add Python to PATH".
- Click "Install Now" and follow the installation steps.

Once the installation is complete, you can verify it by opening a command prompt and typing “python --version”



**Install Visual Studio Code (VS Code)**
For Windows
- Go to the Visual Studio Code download page “https://code.visualstudio.com/Download”.
- Click on the "Download for Windows" button.
- Once the installer is downloaded, run the installer.
- Follow the installation wizard steps:
- Accept the license agreement.
- Choose the destination location.
- Select additional tasks such as creating a desktop icon and adding VS Code to your PATH.
- Click "Install" and wait for the installation to complete.
- Once the installation is done, click "Finish" to launch VS Code.


**Clone Github**
_Prerequisites_
- Visual Studio Code (VS Code) installed on your computer.
- Git installed on your computer.
- A GitHub account and a repository to clone.
- Steps
- Install Git
- If you haven't already installed Git, download and install it from Git's official website.
- “https://git-scm.com/downloads”
- Open VS Code
- Launch Visual Studio Code.
- Open Command Palette
- Press Ctrl + Shift + P to open the Command Palette.
- Clone Repository
- In the Command Palette, type Git: Clone and select Git: Clone from the list of options.
- Link: “https://github.com/marieeposa/sales-and-inventory-system”
-  Enter Repository URL

- You will be prompted to enter the URL of the GitHub repository you want to clone. Go to GitHub, navigate to the repository, and click on the green Code button. Copy the URL (it should look like https://github.com/username/repository.git).
- Select Local Directory
- 
- After entering the repository URL, you will be prompted to select a local directory where you want to clone the repository. Choose a directory on your computer.
- Open the Cloned Repository
- Once the repository is cloned, you will see a notification asking if you want to open the cloned repository. Click Open.
- Install Extensions (Optional)

- If the repository you cloned requires specific VS Code extensions (like Python, JavaScript, etc.), VS Code might prompt you to install them. You can choose to install these extensions to get a better development experience.
- Open Integrated Terminal
- To start working with your cloned repository, you might need to use the terminal. Open the integrated terminal in VS Code by pressing Ctrl + ~
- Verify Cloning
- To ensure that the repository is cloned successfully, you can use Git commands. In the terminal, type:
- “git status”
- This command will show the status of the repository and confirm that you are in a Git repository. 


**Install PostgreSQL**
For Windows
- Go to the PostgreSQL download page “https://www.postgresql.org/download/”
- Click on "Windows" and then download the PostgreSQL installer.
- Run the installer and follow the steps:
- Click the downloaded file
- Select the components you want to install (leave default selections).
- Choose the installation directory.
- Set a password for the PostgreSQL superuser (make sure to remember this password).
- Choose the port number (default is 5432).
- Set the locale.
- Click "Next" and then "Finish" to complete the installation.

Optionally, install pgAdmin, a graphical interface for managing PostgreSQL databases.

When you clone a Django project from Git, the database settings in the settings.py file might not match your local database configuration. To fix this, you need to set up the database locally and adjust the settings accordingly. 
Here's a step-by-step guide to set up and fix the database connection:

- Install PostgreSQL
- Open VS Code. Open terminal.
- Create a PostgreSQL Database (Sales and Inventory Management) and User
- psql -U postgres
- Create a New Database:
- CREATE DATABASE ecokind;
- Create a New User:
- CREATE USER admin WITH PASSWORD 'admin1234';
- Grant Privileges to the User:
- GRANT ALL PRIVILEGES ON DATABASE ecokind TO admin;
- |q
-  Install Required Python Packages. (Make sure that python is installed accordingly and that the path matches so that you can run pip).
- pip install -r requirements.txt 
- pip install psycopg2
- Apply Migrations. Run the following commands to apply migrations and set up the database schema. (Make sure that python is installed accordingly and that the path matches so that you can run pip).
- python manage.py makemigrations
- python manage.py migrate

_If there is an error in migrations_
- Connect to PostgreSQL
- psql -U postgres
- Switch to the target database
- \c ecokind
- Grant all privileges on the public schema to the user
- GRANT ALL PRIVILEGES ON SCHEMA public TO your_db_user;
- Grant create table permission to the user
- ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_db_user;
- Quit Postgre
- \q

**Run migrations**
- python manage.py makemigrations
- 	python manage.py migrate
- Run server
- python manage.py runserver 


