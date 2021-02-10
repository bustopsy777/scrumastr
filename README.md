# Building Chatscrum
To build Chatscrum from the source code into a docker image, follow these steps.
1. Clone the chatscrum repo into the / directory (/scrumastr will be created by default, replace branch_name with the desired branch) and cd into it 

`git clone https://gitlab.com/showpopulous/scrumastr.git -b branch_name`

`cd /scrumastr`

2. Copy the contents of the build_files folder into the scrumastr folder

`cp build_files/* /scrumastr/`

3. In the environment.ts file, edit the "domain_protocol" to the protocol of the backend domain and "domain_name" to the domain name of the chatscrum backend 
4. In the settings.ini file, edit the "FRONTEND" line to the correct chatscrum frontend
5. In the settings.py file, under "DATABASES = {", edit the NAME, USER, PASSWORD, and HOST values to valid credentials to access the MySQL database. This means that on the MySQL server at the ip/hostname specified in HOST, there needs to be a USER accessible remotely with PASSWORD with full permissions on the database called NAME. 

*** If using a mysql database in a docker container on the same machine the chatscrum docker container will be, do the following:

`sudo docker pull mysql/mysql-server:latest`

`sudo docker network create chatscrum`

`sudo docker run --name=mysql-cs -d --network=chatscrum mysql/mysql-server:latest`

`# note hostname from next command`

`sudo docker inspect mysql-cs | grep Hostname`

`# note password from next command`

`sudo docker logs mysql-cs 2>&1 | grep GENERATED`

`sudo docker exec -it mysql-cs mysql -uroot -p`

If the settings.py file is set like this

        'NAME': 'chat',
        'USER': 'linuxjobber',
        'PASSWORD': '8iu7*IU&',
        'HOST': 'mysql-hostname-replace-with-correct-host',

then when logged into the MySQL as root user, the following commands (or the equivalent) need to have been run before chatscrum is deployed:

`CREATE DATABASE IF NOT EXISTS chat;`

`use chat;`

`CREATE USER IF NOT EXISTS 'linuxjobber'@'%' IDENTIFIED BY '8iu7*IU&' ;`

`GRANT ALL PRIVILEGES ON *.* TO 'linuxjobber'@'%' ;`

6. Create an account at https://hub.docker.com/ (if necessary) and use those credentials to login to docker (optional step but recommended)

`sudo docker login`

7. Build the image using the docker build command while in the /scrumastr folder. Example:

`docker build -t username/chatscrum:example_tag .`

8. Push the image that you just built to your docker hub repository (optional but recommended in case the local image is compromised or is not present)

`docker push username/chatscrum:example_tag`

# Deploying Chatscrum
To deploy the chatscrum docker image in a docker container, follow these steps
1. Make sure that a database matching the values in step 5 of the build process is up and running
2. Run the chatscrum image you have built

`docker run --name cs-name -d -p 5000:5000 -p 5100:5100 username/chatscrum:example_tag`

*** If using a docker container MySQL databse, run this command instead:

`docker run --name cs-name -d -p 5000:5000 -p 5100:5100 --net=chatscrum username/chatscrum:example_tag`

3. Access chatscrum in a web browser at the domain you are using or at the IP address and port (your.chatscrum.com or ipaddress:5100 in a web browser)
4. Click on the SIGN UP button at the top right and create a user with account type "Owner" and Project Name "linuxjobber"
5. After creating the user, go to the login page and login with the credentials of the user. The very first login attempt will give an error, but all subsequent attempts will succed. 
6. After logging in, connect chatscrum to slack and pick a channel to post in (bin is available to everyone).
7. Log back into chatscrum with the same credentials, click on "My Tasks" at the top, then "ADD TASK" at the bottom left to create a new task. You should see "Goal created success." at the bottom.
8. Send a message in the Scrum Chat Messages. If the message appears in the slack channel and soon after in the Scrum Chat Messages itself, you have successfully deployed chatscrum.

