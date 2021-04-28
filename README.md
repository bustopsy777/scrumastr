## Building Chatscrum
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

*** In the MySQL database you are connecting to, run these commands as root user (or the equivalent) before chatscrum is deployed (if on a kubernetes cluster,
*** refer to the last section on how to create a mysql database in a cluster)

`CREATE DATABASE IF NOT EXISTS chat;`

`use chat;`

`CREATE USER IF NOT EXISTS 'linuxjobber'@'%' IDENTIFIED BY '8iu7*IU&' ;`

`GRANT ALL PRIVILEGES ON *.* TO 'linuxjobber'@'%' ;`

6. Copy the Django/ScrumMaster/requirements2.txt file to the top directory of the repo as requirements.txt, and then add lines to install boto3, slack, and cryptography==3.3.2 to the end of the file. Edit the zope.interface and slackclient lines to install the latest version. (You can simply remove the specified version number to have the latest version of the package installed (eg. "slackclient" instead of "slackclient==2.9.3")) 

`cp Django/ScrumMaster/requirements2.txt requirements.txt` 

7. Create a directory named "www" and copy the Django and Chatscrum-Angular folders into the www folder

`mkdir www`
`cp -r Django/ www/`
`cp -r Chatscrum-Angular/ www/` 

8. Create an account at https://hub.docker.com/ (if necessary) and use those credentials to login to docker (optional step but recommended)

`sudo docker login`

9. Build the image using the docker build command while in the /scrumastr folder. Example:

`docker build -t username/chatscrum:example_tag .`

10. Push the image that you just built to your docker hub repository (optional but recommended in case the local image is compromised or is not present)

`docker push username/chatscrum:example_tag`

## Deploying Chatscrum in Docker container
To deploy the chatscrum docker image in a docker container, follow these steps
1. Make sure that a database matching the values in step 5 of the build process is up and running
2. Run the chatscrum image you have built

`docker run --name cs-name -d -p 5000:5000 -p 5100:5100 username/chatscrum:example_tag`

*** If using a docker container MySQL databse running on the same machine, run this command instead:

`docker run --name cs-name -d -p 5000:5000 -p 5100:5100 --net=chatscrum username/chatscrum:example_tag`

3. Connect to the same database used in step 5 and run the following commands in the MySQL database

`use chat;`

`select * from Scrum_chatscrumslackapp;`

`INSERT INTO Scrum_chatscrumslackapp (SLACK_VERIFICATION_TOKEN, CLIENT_ID, CLIENT_SECRET) VALUES ("oeIAvaMSGyT0L96VtyCwKPpo", "516134588580.520839787655", "e97b4cdb649cd9768e5cc5759bb7764c");`

4. Access chatscrum in a web browser at the domain you are using or at the IP address and port (your.chatscrum.com or ipaddress:5100 in a web browser)
5. Click on the SIGN UP button at the top right and create a user with account type "Owner" and Project Name "linuxjobber"
6. After creating the user, go to the login page and login with the credentials of the user. The very first login attempt will give an error, but all subsequent attempts will succed. 
7. After logging in, do not connect chatscrum to slack.
8. Log back into chatscrum with the same credentials, click on "My Tasks" at the top, then "ADD TASK" at the bottom left to create a new task. You should see "Goal created success." at the bottom. If you can move the task from the "Tasks for the week" box to the "Todays Target" box, and the move persists after a page refresh (Ctrl+F5), then you have successfully deployed chatscrum.

## Deploying Chatscrum on a Kubernetes cluster
To deploy the chatscrum docker image on a kubernetes instruction, you must first have an existing kubernetes cluster
1. In the cs-deploy.yaml file, edit the image field with the chatscrum image you wish to deploy (image must be pushed to remote repository)
2. On the node of the cluster, create the /opt/dockermounts directory, and place the configured settings.ini file 
from chatscrum at /opt/dockermounts/settings_cs.ini and the configured settings.py at /opt/dockermounts/settings_cs.ini, both with 664 permissions
*** creating a MySQL database on the kubernetes cluster
3. Run the commands below to create the mysql database in a pod 
```
kubectl apply -f mysql-svc.yaml
# Wait for the service to be created
kubectl apply -f mysql-deploy.yaml
```
4. Run the below commands to create the chatscrum deployment on the cluster
```
kubectl apply -f cs-serv.yaml
kubectl apply -f cs-deploy.yaml
```
5. Refer to step 5 in "Deploying Chatscrum in Docker container" and follow from there


