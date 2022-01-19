# Overview
This guide is divided into two parts, the first part will walk you through creating the Chatscrum image, and the second part will walk you through deploying containers built from the image on different platforms. 

# Table of Content
1. Setting Up the database
2. Building the Chatscrum Image
3. Deploying chatscrum


### 1. Setting up the Database
Chatscrum uses implements a MySQL database, and this guide covers three deployment methods for Chatscrum, which include deployment on Docker, deployment on Kubernetes and deployment on ECS. Depending on the method you choose, you will need to set up a MySQL database which can be accessed easily.

***a. If you will be deploying using Docker then follow these steps to set up your database:***

`sudo docker pull mysql/mysql-server:latest`

`sudo docker network create chatscrum`

`sudo docker run --name=mysql-cs -d --network=chatscrum mysql/mysql-server:latest`

`# note hostname from next command`

`sudo docker inspect mysql-cs | grep Hostname`

`# note password from next command`

`sudo docker logs mysql-cs 2>&1 | grep GENERATED`

`sudo docker exec -it mysql-cs mysql -uroot -p`

`CREATE DATABASE IF NOT EXISTS chat;`

`use chat;`

`CREATE USER IF NOT EXISTS 'linuxjobber'@'%' IDENTIFIED BY '8iu7*IU&' ;`

`GRANT ALL PRIVILEGES ON *.* TO 'linuxjobber'@'%' ;`

***b. If you're going to be deploying to AWS ECS, then follow the guide in this link https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html to setup a "MYSQL" RDS Instance(Set it up using free tier, except this is going to be production).***

`In the "initial database name" section, enter any name of your choice and remember this name because it will be used in a later step.This will ensure that the database is created at the instance creation time.`

`Test that you can connect to the database from the command line using the command "mysql -h <RDS_DNS_NAME> -u <Initial_username> -P <port_you_chose_at_instance_creation> -p", and hit enter`.

`You will get a prompt for a password, enter the password and hit enter.`

`If you are unable to connect to the instance, try editing the security group to allow access from anywhere (0.0.0.0/0) or from the IP address of the server from which you are trying to connect.`

`Upon successful connection, confirm you can see the data base you created using the command: "show databases;"`

***c. If you want to deploy Chatscrum on a Kubernetes cluster, please refer to this guide: https://phoenixnap.com/kb/kubernetes-mysql to set up a MySQL Database in your Kubernetes cluster***

`Post deployment of the MySQL Pod, connect to it using the command "kubectl exec --stdin --tty <id_of_the_sql_pod> -- /bin/bash"`

`Run the command "mysql -p" and you will get the mysql prompt, repeat the following steps to create a database`

`CREATE DATABASE IF NOT EXISTS chat;`

`use chat;`

`CREATE USER IF NOT EXISTS 'linuxjobber'@'%' IDENTIFIED BY '8iu7*IU&' ;`

`GRANT ALL PRIVILEGES ON *.* TO 'linuxjobber'@'%' ;`


### 2. Building the Chatscrum Image

To build Chatscrum from the source code into a docker image, follow these steps.

***a. Clone the chatscrum repo into the / directory (/scrumastr will be created by default, replace branch_name with the desired branch) and cd into it*** 

`git clone https://gitlab.com/showpopulous/scrumastr.git -b branch_name`

`cd /scrumastr`

***b. Copy the contents of the build_files folder into the scrumastr folder***

`cp build_files/* /scrumastr/`

***c. In the environment.ts file, edit the "domain_protocol" to the protocol of the backend domain and "domain_name" to the domain name of the chatscrum backend*** 

***d. In the settings.ini file, edit the "FRONTEND" line to the correct chatscrum frontend***

***e. In the settings.py file, under "DATABASES = {", edit the NAME, USER, PASSWORD, and HOST values to valid credentials to access the MySQL database. This means that on the MySQL server at the ip/hostname specified in HOST, there needs to be a USER accessible remotely with PASSWORD with full permissions on the database called NAME.***

Given the format: 

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', '\n'
        'NAME': 'newcs',
        'USER': 'linuxjobber',
        'PASSWORD': '1qaz#EDC3edc',
        'HOST': 'wt-mysql',
        'PORT': '3306',
        'OPTIONS': {
            #'raise_on_warnings': False,
            #'use_pure': True
        }
    }
}

```

*** If you set up your database in a docker container, "HOST" will be the MySQL container name, if you set it up using RDS, then it will be the DNS name of your RDS instance, usually in the format "db1.123456789012.us-east-1.rds.amazonaws.com". If you set up in a Kubernetes pod, the host name will be the name of the Service created in the C section of the "Setting Up the Database" instructions. Username and Password will be the 'linuxjobber' and '8iu7*IU& respectively, except you entered your own custom values at creation time. 

***f. Copy the Django/ScrumMaster/requirements2.txt file to the top directory of the repo as requirements.txt, and then add lines to install boto3, slack, and cryptography==3.3.2 to the end of the file. Edit the zope.interface and slackclient lines to install the latest version. (You can simply remove the specified version number to have the latest version of the package installed (eg. "slackclient" instead of "slackclient==2.9.3"))*** 

`cp Django/ScrumMaster/requirements2.txt requirements.txt` 

***g. Create a directory named "www" and copy the Django and Chatscrum-Angular folders into the www folder***

`mkdir www`
`cp -r Django/ www/`
`cp -r Chatscrum-Angular/ www/` 

***h. Create an account at https://hub.docker.com/ (if necessary) and use those credentials to login to docker (optional step but recommended)***

`sudo docker login`

***i. Build the image using the docker build command while in the /scrumastr folder. Example:***

`docker build -t username/chatscrum:example_tag .`

***j. Push the image that you just built to your docker hub repository (optional but recommended in case the local image is compromised or is not present)***

`docker push username/chatscrum:example_tag`


### 3. Deploying Chatscrum 

***a. To deploy the chatscrum docker image in a docker container, follow these steps***

- Make sure that a database matching the values in Section a of the Database setup is up and running

- Run the chatscrum image you have built using the below command, replacing "<username/chatscrum:example_tag>" with the image name you built.

`docker run --name cs-name -d -p 5000:5000 -p 5100:5100 <username/chatscrum:example_tag>`

*** If using a docker container MySQL databse running on the same machine, run this command instead:

`docker run --name cs-name -d -p 5000:5000 -p 5100:5100 --net=chatscrum username/chatscrum:example_tag`

- Connect to the same database used and run the following commands in the MySQL database

`use chat;`

`select * from Scrum_chatscrumslackapp;`

`INSERT INTO Scrum_chatscrumslackapp (SLACK_VERIFICATION_TOKEN, CLIENT_ID, CLIENT_SECRET) VALUES ("oeIAvaMSGyT0L96VtyCwKPpo", "516134588580.520839787655", "e97b4cdb649cd9768e5cc5759bb7764c");`

- Access chatscrum in a web browser at the domain you are using or at the IP address and port (your.chatscrum.com or ipaddress:5100 in a web browser).

- Click on the SIGN UP button at the top right and create a user with account type "Owner" and Project Name "linuxjobber"

- After creating the user, go to the login page and login with the credentials of the user. The very first login attempt will give an error, but all subsequent attempts will succed. 

- After logging in, do not connect chatscrum to slack.

- Log back into chatscrum with the same credentials, click on "My Tasks" at the top, then "ADD TASK" at the bottom left to create a new task. You should see "Goal created success." at the bottom. If you can move the task from the "Tasks for the week" box to the "Todays Target" box, and the move persists after a page refresh (Ctrl+F5), then you have successfully deployed chatscrum.

***b. Deploying Chatscrum on a Kubernetes cluster***

To deploy the chatscrum docker image on a kubernetes instruction, you must first have an existing kubernetes cluster

- In the cs-deploy.yaml file, edit the image field with the chatscrum image you wish to deploy (image must be pushed to remote repository).

- On the node of the cluster, create the /opt/dockermounts directory, and place the configured settings.ini file 
from chatscrum at /opt/dockermounts/settings_cs.ini and the configured settings.py at /opt/dockermounts/settings_cs.ini, both with 664 permissions

- Run the below commands to create the chatscrum deployment on the cluster
```
kubectl apply -f cs-serv.yaml
kubectl apply -f cs-deploy.yaml
```
- Refer to step 5 in "Deploying Chatscrum in Docker container" and follow from there

***c. GUIDE FOR CHATSCRUM DEPLOYMENT ON WINDOWS SERVER 2016***
### Prerequisites:
-  Create a gitlab account if you don’t have one already (https://gitlab.com)
-   You should have an accessible EC2 machine running Microsoft Windows server 2016
-   You should have Internet Information Service (IIS) installed and configured on the server. Ensure that CGI application development role service is installed along. If you have carried out IIS installation before now without ticking CGI service, perform a feature-based installation and have it installed.
-  You should have `URL Rewrite` (An IIS extension) installed on your server. https://www.iis.net/downloads/microsoft/url-rewrite
-   Download and install `git` for windows on your server
-   Download and install a code editor you can use on your server. E.g.`Visual Studio Code`
-   You should have `MySQL` installed and configured on the server. (The Chatscrum application uses MySQL database). https://mid.as/kb/00145/install-configure-mysql-on-windows#download-mysql
-  You should have `node` installed and configured on your server: https://phoenixnap.com/kb/install-node-js-npm-on-windows
-   Use `git` to get the chatscrum project source code from the repo onto your server (Request for access to the project repo)
NOTE:
Linuxjobber’s chatscrum application has two major parts. There is the Angular part that handles the frontend view of the application. Then there is the Django path that handles routing and communication with the MySQL database. We will be going through the deployment of both.
 
***d. Deploying the Django part to IIS***
1. Log into mysql and create a database
```bash
mysql> create database chatscrum;
```
2. Prepare your project folder for deployment:
* Create a `django/` folder on your C: drive
* Copy the contents within _Django/ScrumMaster/_, excluding _py34env/_ directory, into _C:/django_
* Create `web.config` file in _C:/django_ and write the following content into it:
```bash
<?xml version="1.0" encoding="utf-8"?>
<configuration>
        <system.webServer>
                <handlers>
                        <add name="Python FastCGI"
                        path="*"
                        verb="*"
                        modules="FastCgiModule"
                        scriptProcessor="<to be filled in>"
                        resourceType="unspecified"
                        requireAccess="Script" />
                </handlers>
        </system.webServer>

        <appSettings>
                <add key="PYTHONPATH" value="C:\django" />
                <add key="WSGI_HANDLER" value="ScrumMaster.wsgi.application" />
                <add key="DJANGO_SETTINGS_MODULE" value="ScrumMaster.settings" />
        </appSettings>
</configuration>

```

* Create `static/` folder within _C:/django_ to hold static files for your app. Within `C:/django/static`, create a `web.config` file and add the following content:
```bash
<?xml version="1.0" encoding="utf-8"?>
<configuration>
        <system.webServer>
                <handlers>
                        <clear />
                        <add name="StaticFile"
                        path="*"
                        verb="*"
                        modules="StaticFileModule"
                        resourceType="File"
                        requireAccess="Read" />
                </handlers>
        </system.webServer>
</configuration>
```

3. Edit _C:/django/ScrumMaster/settings.py_
* Add your elastic IP address to allowed hosts. If you already have the asterisk, skip this step.
* Set database configurations to use the credentials of your mysql server
* Set the STATIC_ROOT 
```bash
STATIC_ROOT = os.path.join(BASE_DIR, ‘static’))
``` 
This references the folder where static files will be collected at when manage.py collectstatic is run

4. Prepare your server’s environment:
* Install Python 3.6 in `C:/Python36`, and ensure it is added to system path. (Go with custom installation to be able to customize installation location)
* Use the terminal as administrator to install and enable `wfastcgi`.
Open a CMD terminal as Administrator, and run the command `pip install wfastcgi`
* Afterwards, run the command `wfastcgi-enable`
* Copy the Python path, and replace the `scriptProcessor="<to be filled in>"` in _C:/django/web.config_ file with the Python path returned by `wfastcgi-enable`.
* Edit C:/django/requirements2.txt: replace `slackclient` with the latest version. Replace `zope.interface` with the latest version. (You can simply remove the specified version number to have the latest version of the package installed)
* Using the terminal, navigate into _C:/django_ and run `pip install -r requirements2.txt`. This will install all required packages globally. 
* Run `manage.py makemigrations`. fix errors if any
* Run `manage.py migrate` to set up tables in your database
* Run `manage.py createsuperuser --username <your-name>` ,  to create a superuser account.
 
### Application, Application pool, handlers and virtual directory set up on IIS:
1. Open Internet Information Services (IIS) Manager. Under connections select the server, then in the center pane under Management select `Configuration Editor`. Under `Section` select `system.webServer/handlers`. Under Section select `Unlock Section`. This is required because the default website configuration creates a route handler for the whole project.

* On the IIS console, right click on application pools and add a new application pool using `django` as name. Leave other fields at default. Application pool defines the environment that will launch the application.

* Right click on Default Web Site and add a new application. Set alias as `django`. Select the application pool created earlier. Set `C:/django` as the physical path.

* Right click on Default Web Site, and add a virtual directory. Alias should be `static` and the physical path should point to `C:/django/static`. Static files are stored in virtual directories on IIS.

2. Collect static files:
Navigate into `C:/django` via the terminal and run `manage.py collectstatic`. This should collect all static files into `C:/django/static`

3. Configure the URL to recognise your app name (django):
IIS will serve the django app at http://localhost/django. So it is necessary to reconfigure the django app URL’s to accommodate the preceding ‘django’.
Edit `C:/django/ScrumMaster/urls.py` to look like this:
```python
from django.contrib import admin
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static

patterns = [
        path('admin/', admin.site.urls),
        path('scrum/', include('Scrum.urls')),
        path('accounts/', include('django.contrib.auth.urls'))
]
urlpatterns = [

        path('django/', include(patterns))
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

4. Grant full access to python to the application pool django app uses:
Navigate to `C:/`, right-click on `Python36`, and edit Properties. Under `Security` tab, add `IIS AppPool\django` and grant full control. App pools are responsible for launching applications. So you need to give it permission to python so that it can run your django application.

5. Allow all traffic in your server’s security group and/or firewall:
* Edit the inbound rule of your server’s security group and allow `All traffic`. Source should be set to `Anywhere`.

6. Refresh the server and navigate to localhost:
* Head over to IIS console and refresh the Default Web Site.
Navigate to http://localhost/django (or http://IP-address/django or https://domain/django ) to view the django application.
 
7. Create a record in Chatscrum Slack Apps table:
* Navigate to http://IP-address/django/admin and login with your superuser credentials. You will be needing a Chatscrum Slack App record in place before authentication can be carried out successfully. For now, fill in random content in the three fields. It will suffice.
 

***e. Deploying the Angular Part on IIS***
 
1.  Prep your application for production deployment:
* One thing to note in this step has to do with paths specified in your html files. Preceding paths with a forward slash (/) will not work in production environment, so it is necessary you remove all preceding slashes in reference paths and hrefs. This option will work well in development, as well as production environment. Use the code editor to edit the codes.

* Set your environment variables in `environments.prod.ts` as this is the file that production environment will take cognizance of. The domain_protocol + domain_name setup just points to our django app for communication with the Angular part: 

* Within the angular workspace directory (Chatscrum-Angular), run `npm install` from the terminal to install all required packages. At this point, you can test the app if everything is working fine before proceeding to the next steps. 

* Run `ng serve` to start up a local server and then navigate to http://localhost:4200 via your machine’s browser to view and test your app.

2. Run `ng build --prod --base-href /chatscrum/` from within the workspace directory. This will compile the Angular app into an output directory named `dist/`. `-–base-href` defines the reference to the application in production. `dist/` will contain `chatscrum/` folder ready for production deployment.

3.  Copy the project folder onto the server’s `C:` drive:
* Copy `chatscrum/` directory within dist/, and paste into `C:` drive

* Create a configuration file `web.config` within _C:/chatscrum_ folder, and write the following xml configuration into the file:
```bash
<?xml version="1.0" encoding="utf-8"?>
        <configuration>
                <system.webServer>
                        <rewrite>
                                <rules>
                                        <rule name="Angular Routes" stopProcessing="true">
                                        <match url=".*" />
                                                <conditions logicalGrouping="MatchAll">
                                                        <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true"/>
                                                        <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true"/>
                                                </conditions>
                                        <action type="Rewrite" url="/chatscrum/" />
                                        </rule>
                                </rules>
                        </rewrite>
                </system.webServer>
        </configuration>
```
 
4.  Create a new application pool for your angular app:
* From the IIS console, create a new application pool. It is good practice to have each application within a website use a separate application pool.

5.  Create a new application within the Default Web Site on IIS:
* From the IIS console, add a new application to the default website. Name it `chatscrum`, and select the `C:/chatscrum` as the physical path. Also select the application pool created in (4). 

6.  Visit [IP ADDRESS]/chatscrum/ via your browser:
* Replace [IP ADDRESS] with the IP of your server. Or if you have configured a domain name, navigate to https://<domain>/chatscrum  

***f. GUIDE FOR CHATSCRUM DEPLOYMENT ON LINUX SERVER***
### Prerequisites:
* In order to complete this guide, you should have a fresh CentOS 8 server instance with a non-root user with sudo privileges configured (Instance type: t2.medium atleast)
* Allow all traffic in your server’s security group if you are using AWS EC2 machines
* Install `httpd` and `git` on your server using `yum` package manager
* You should have `MySQL` installed and configured on the server. Ensure to start the service and enable it to start automatically on server reboot. The Chatscrum application uses MySQL database. [here](#https://www.hostinger.com/tutorials/how-to-install-mysql-on-centos-7)

NOTE:
Linuxjobber’s chatscrum application has two major parts. There is the Angular part that handles the frontend view of the application. Then there is the Django path that handles routing and communication with the MySQL database. 
 
***g. Deploying the Django part to Linux server***
1. Log into mysql and create a database
```bash
mysql> create database chatscrum;
```
2. Prepare your project folder for deployment:
* Use git to get the chatscrum project source code into your home directory (/home/youruser; “youruser” reps the logged in user)
* Edit /home/youruser/chatscrum/Django/ScrumMaster/ScrumMaster/settings.py:
* Set `DEBUG` to "False"
* Add your elastic IP address to allowed hosts. If you already have the asterisk, skip this step.
* Set database configurations to use the credentials of your mysql server
* Set the STATIC_ROOT:
```bash
STATIC_ROOT = os.path.join(BASE_DIR, ‘static’))
``` 
This references the folder where static files will be collected at when manage.py collectstatic is run

#### Prepare your server’s environment:
* Install python: https://tecadmin.net/install-python-3-7-on-centos/ (Use these options during configuration => `./configure --prefix=/usr/local --enable-shared  --enable-optimizations`)
* Install mod_wsgi: An interface that will run python applications on apache: (https://www.marek.tokyo/2018/08/apache-24-modwsgi-python-37-django.html) If you encounter any error during ‘make altinstall’, run the following command before ‘make altinstall’:  sudo ldconfig /usr/local/lib  
* Install virtualenv; A cli utility for creating virtual environments (pip3.7 install virtualenv)
* Create a virtual environment named `venv` within the project. ( virtualenv /home/youruser/chatscrum/Django/ScrumMaster/venv)
* Activate the virtual environment (`source /home/youruser/chatscrum/Django/ScrumMaster/venv/bin/activate`)
* Edit _/home/youruser/chatscrum/Django/ScrumMaster/requirements2.txt_: add comment out `mysqlclient` package as it won’t be needed; `pymysql` was used instead. Replace `slackclient` version with the latest version. Replace `zope.interface` with the latest version. (You can simply remove the specified version number to have the latest version of the package installed ‘==xxx’)
* Install all required packages by running `sudo pip3.7 install -r requirements2.txt`. This will install all required packages within the virtual environment created. 
* Navigate into /home/youruser/chatscrum/Django/ScrumMaster/ where `manage.py` is, and run `python3.7 manage.py makemigrations` to read all django models
* Run `python3.7 manage.py migrate` to set up tables in your database
* Run `python3.7 manage.py collectstatic` to collate static files 
* Run `python3.7 manage.py createsuperuser --username <your-name>` and follow the prompt to create a superuser account.
* Start up the django server and create a record in the admin. Still in /home/youruser/chatscrum/Django/ScrumMaster/, run `python3 manage.py runserver 0.0.0.0:8000` to start up the django server
* Navigate to `[address]:8000/admin` via your browser to access the django admin interface. Replace [address] with the IP address of your machine
* You will be needing a Chatscrum Slack Apps record in place before authentication can be carried out successfully. For now, log in and create a new record in `Chatscrum Slack Apps`. Fill in random contents in the three fields and save it. It will suffice.

 
#### Interfacing with Apache (httpd)
The last thing we want to do is to interface the application with an apache web server using mod_wsgi. 
1. Create `chatscrum.conf` file within /etc/httpd/conf.d/ ; this file will contain our apache virtual host configuration for chatscrum app.
* Write the following content into the file:
```bash
LoadModule wsgi_module /usr/lib64/httpd/modules/mod_wsgi.so

<VirtualHost *:80>
        ServerAdmin     admin@<domain name>   
        ServerName      <domain name>
        ServerAlias     www.<domain name>
        DocumentRoot    /home/<your-user>/chatscrum/Django/ScrumMaster
        ErrorLog        /var/log/httpd/error.log
        CustomLog       /var/log/httpd/access.log combined

        Alias   /static   /home/your-user/chatscrum/Django/ScrumMaster/static
        <Directory      /home/your-user/chatscrum/Django/ScrumMaster/static>
                Require all granted
        </Directory>

        Alias   /static   /home/your-user/chatscrum/Django/ScrumMaster/media
        <Directory      /home/your-user/chatscrum/Django/ScrumMaster/media>
                Require all granted
        </Directory>

        <Directory      /home/your-user/chatscrum/Django/ScrumMaster/ScrumMaster>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

        WSGIDaemonProcess       chatscrum       python-path=/home/<your-user>/chatscrum/Django/ScrumMaster:/home/your-user/chatscrum/Django/ScrumMaster/venv/lib/python3.6/site-packages        python-home=/home/<your-user>/chatscrum/Django/ScrumMaster/venv
        WSGIProcessGroup        chatscrum
        WSGIScriptAlias /       /home/<your-user>/chatscrum/Django/ScrumMaster/ScrumMaster/wsgi.py

TimeOut 10000

</VirtualHost>
```

NB: Ensure you replace [domain name] with the domain name pointing to your elastic IP. Also replace ‘youruser’ with the logged in username. Also specify your correct python version installation in the `python-path`=> python3.7 

* Run `apachectl configtest` to confirm there are no errors in your configuration
* wsgi.py is the entry point of our application using python’s module syntax. Inside this file, a function named application is defined, and is used to communicate with the application. We will write some codes that will activate the virtual environment where we installed our required packages for the chatscrum app.
* Edit /home/youruser/chatscrum/Django/ScrumMaster/ScrumMaster/wsgi.py and add the following contents just before application = get_wsgi_application():
:		
```python
def execfile(filepath, globals=None, locals=None):
        if globals is None:
                globals = {}
        globals.update({
                "__file__": filepath,
                "__name__": "__main__",
        })
        
        with open(filepath, 'rb') as file:
                exec(compile(file.read(), filepath, 'exec'), globals, locals)
        
        python_home = /home/<your-user>/chatscrum/Django/ScrumMaster/venv
        activate_this = python_home + '/bin/activate_this.py'
        execfile(activate_this, dict(__file__=activate_this))
```
* Set SElinux security to Permissive
* Grant access to all files within your home directory to apache so it can read the chatscrum folder. Best way to do this will be to grant `rx` access to the ‘youruser’ group bits of your home directory(/home/youruser), then add apache to this group.
* Run `sudo chmod -R 766 /var/log` to open access to apache to write logs

* Activate the virtual environment and start up the server just like before. Fix errors if there is.
* Stop the server and start `httpd` service using systemctl utility. Now, apache will be able to access and server the django application through the WSGI interface.
* Navigate to http://<IP/hostname>/admin via your browser to access the Django admin interface. (Replace IP or hostname with the correct value)

  

***g. Deploying the Angular Part (Linux server)***
1.  Prep your server environment: 
* Install and configure node and npm on your server: https://linuxize.com/post/how-to-install-node-js-on-centos-7/
* Using npm, install angular cli globally on your server: (sudo npm install -g @angular/cli@9)

2.  Prep your application for production deployment:
* Edit _/home/youruser/chatscrum/Chatscrum-Angular/src/environments/environment.prod.ts_ and set your environment variables in `environments.prod.ts` as this is the file that production environment will take cognizance of. Value of the `domain_name` should be the actual elastic IP or hostname of your server. The `domain_protocol` + `domain_name` setup just points to our django app for communication with the Angular part: (you can see the content within `environment.ts` file which is in same directory as environments.prod.ts. The former is used in a development environment)

* Within the angular workspace directory (Chatscrum-Angular) where package.json exists, run `npm install` from the terminal to install all required packages. 
* Run `ng build --prod`  from within the workspace directory. This will compile the Angular app into an output directory named `dist/`. _dist/_ will contain chatscrum/ folder ready for production deployment.

3.  Edit the `chatscrum.conf` configuration file to add a new virtualhost (/etc/httpd/conf.d/chatscrum.conf):
```bash
listen 8000
<VirtualHost *:8080>
        ServerAdmin     admin@djangoproject.locahost
        ServerName      djangoproject.localhost
        DocumentRoot    /home/<your-user>/chatscrum/Chatscrum-Angular/dist/chatscrum
        ErrorLog        /var/log/httpd/error.log
        CustomLog       /var/log/httpd/access.log       combined

        <Directory     /home/<your-user>/chatscrum/Chatscrum-Angular/dist/chatscrum>
                Require all granted
        </Directory>
</VirtualHost>
```

NB: You can use any free port you desire. Replace ‘youruser’ with your username. In essence, The angular app will be served on PORT 8080, while the Django app will be served on PORT 80.

4.   Edit httpd default conf file(`/etc/httpd/conf/httpd.conf`) and define fallback resource for the Angular app:
```bash
<Directory      "/home/<your-user>/chatscrum/Chatscrum-Angular/dist/chatscrum">
        FallbackResource        /index.html
        Options Indexes FollowSymLinks
        AllowOverride   None
        Require all granted
</Directory>
```
This will help apache point back to index.html whenever a url endpoint without a file is navigated to.

5.  Visit http://<IP_ADDRESS>:8080 via your browser:
Replace <IP_ADDRESS> with the elastic IP or domain name of your server

***h. Deploying Chatscrum in AWS ECS***

To deploy the chatscrum docker image in ECS, follow these steps:

1. Ensure you already have an ECS cluster running. For this we recommend using the Fargate cluster type. If you do not have a cluster already set up, then follow these steps to set it up:
In the navigation pane, choose Clusters.

- On the Clusters page, choose Create cluster.


- Under Cluster configuration, for Cluster name, enter a unique name.


- The name can contain up to 255 letters (uppercase and lowercase), numbers, and hyphens.


- (Optional) To change the VPC and subnets where your tasks and services launch, under Networking, perform any of the following operations:

```

To remove a subnet, under Subnets, choose X for each subnet that you want to remove.

To change to a VPC other than the default VPC, under VPC, choose an existing VPC, and   then under Subnets, select each subnet.

```


- (Optional) To turn on Container Insights, expand Monitoring, and then turn on Use Container Insights.


- (Optional) To manage the cluster tags, expand Tags, and then perform one of the following operations:

```

[Add a tag] Choose Add tag and do the following:

   For Key, enter the key name.

   For Value, enter the key value.

[Remove a tag] Choose Remove to the right of the tag’s Key and Value.

```


- Choose Create. Refer to the documentation: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create_cluster.html, if you get a view not aligned with the steps above, to set up a Fargate cluster.


2. When the cluster is created, set up a Task definition file, which is quite similar to a manifest file in Kubernetes. In the image section of the task definition, enter in the Image URI for your image, this will differ depending on the repository you pushed your image to. For the port, use port 5100.


3. If you will like to use a load balancer for your services/task, then setup an application load balancer, listeners and target groups, which you will connect to your service/task, by following the below steps:
 
- Go to the EC2 Console in AWS.


- From the left-hand menu, expand Load Balancing and select Load balancers.


- Click Create Load balancer, and under Application Load Balancer, click Create.


- Set the Basic configuration properties:

```
Load Balancer Name: Enter a name for the load balancer.

Scheme: Select Internet-facing.
    
IP address type: Select IPv4. Note that an elastic IP is not required. If you select assigned by AWS, use the DNS name when creating the gateway token.

Set the Network Mapping properties:
    
    VPC: Select the VPC where this ECS gateway will be hosted.
    
    Mappings: Select the availability zone where you want the load balancer to be hosted (i.e., where the public subnet resides).

Set the Listeners and routing properties:
    
    Port: Select TCP port 5100. Note that 5100 is the default TCP port specified for the Django part of the application.
    
    Create target group: Click the link, which will open a new tab.
    
    On the Specify group details page that opens
        
        Target type: Select IP Addresses as the target group.
        
        Target group name: Set the name of the target group.
        
        Port: Set TCP port 5100 for the listener. This port needs to match the port you plan to expose on the Fargate container.

```

- Click Next.


- On the next page, leave the options blank and click Create target group. Note that a target will be set later once the ECS container is created.


- Go back to the Load Balancers properties page, and click the refresh button next to Target group.


- Select the target group that was just created.


- Click Create load balancer.


- Click View load balancers, and copy the ALB DNS name of the ALB that you just created.


4. Set up a service in the cluster you created, and base it on the task definition you created in step 2, ensure that you add your container to the Load balancer in the Load balancer section, if you want to use a load balancer, using the below steps:

- On the Clusters Management page, click your cluster name. On that page, click the Services tab and then click Create.


- On the Create Service page that opens:

```
Launch type: Select FARGATE.

Task Definition: Select the task definition created earlier.

Service name: Enter a name for this service.
    
Number of tasks: Set 1.
    
Minimum healthy percent: Set 0.

Maximum healthy percent: Set 100.

Deployment type: Set Rolling update.

Click Next step.

```


- On the Configure network page:

```
Cluster VPC: Select the Fargate VPC where the cluster is hosted.

Subnets: Select a private subnet. Without this, the NLB will not be able to reach the container (e.g., 10.0.7.0/24).

Security Groups: Click Edit and do the following:
    Click Create a new security group.
        In Basic details:
            Security group name: Name the group.
            Description: Describe what the group is for.
            VPC: Select the VPC.
            Under Inbound rules:
            Type: Choose Custom TCP.
            Port range: Choose the port (e.g., "5100") you are mapping from the load balancer to the service.
           Source: Choose Anywhere. Please note: The load balancer is only open on the ports you forward, and the service is on a private network. You can, however, specify the IP address or range of the load balancer if you prefer. We recommend starting with an open security group for testing; you can modify it later.
           Click Create security group.
```

- Auto-assign public IP: Set to ENABLED

- Load balancer type: Select Application Load Balancer.

- Load balancer name: Select the ALB that you created earlier.

- Click Add to load balancer.

- Production listener port: Select 5100 TCP.

- These steps also enable the Health check grace period field. Scroll up and enter a value of 600 (seconds), for a 10-minute grace period.

- Click Next step.

- On the Set Auto Scaling page:

- Make sure that Auto-scaling is set to Do not adjust the service’s desired count.

- Click Next step.

- Click Create Service.

- Click View Service

5. When the task in your service show up as running, confirm that you can access the application using the DNS of your load balancer, in the format DNS_NAME:5100. This should return a Django Admin page. If this does not return a response, ensure that the Security Group of the load balancer is open for connections from the internet on Port 5100.

6. When the application loads up, connect again, to your RDS instance which you set up and run the following commands in the MySQL database:

`use chat;`

`select * from Scrum_chatscrumslackapp;`

`INSERT INTO Scrum_chatscrumslackapp (SLACK_VERIFICATION_TOKEN, CLIENT_ID, CLIENT_SECRET) VALUES ("oeIAvaMSGyT0L96VtyCwKPpo", "516134588580.520839787655", "e97b4cdb649cd9768e5cc5759bb7764c");`

7. If you notice that your tasks are being restarted or you're unable to still connect to the application after opening up port 5100 on the security group of your Load balancer, confirm from the task logs, the error leading to the restart of the tasks.




