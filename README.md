# Web-Dev-Group-L
The repo for submission of all the code related to the web development group assignment. 


# To run

1. Make sure you are in the directory ../Web-Dev-Group-L\backend

2. Run "docker build -t myapp ." to create the docker image

3. Run "docker volume create myapp-storage" 

4. Finally run "docker run -ti -e "DATABASE_URL=mysql://myappdbuser:myappdbpass@host.docker.internal:3306/myappdb" -v myapp-storage:/app/storage -p 8000:8000 myapp" 
This will run the app at http://localhost:8000.

5. Important to make sure your MySQL database is running when you run the command in step 4.

# Test logins

For test accounts provided with the initial_data.json

Manager login
Username: manager
Password: manager123

Technician login
Username: tech1
Password: tech123

Repair login
Username: repair1
Password: repair123
