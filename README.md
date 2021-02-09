To build Chatscrum from the source code into a docker image, follow these steps.
1. Clone the chatscrum repo into the / directory (/scrumastr will be created by default) and cd into it 
`cd /scrumastr`
2. Copy the contents of the build_files folder into the scrumastr folder
`cp build_files/* /scrumastr/`
3. In the environment.ts file, edit the "domain_protocol" to the protocol of the backend domain and "domain_name" to the domain name of the chatscrum backend 
4. In the settings.ini file, edit the "FRONTEND" line to the correct chatscrum frontend
5. In the settings.py file, under "DATABASES = {", edit the NAME, USER, PASSWORD, and HOST values to valid credentials to access the MySQL database.
6. Build the image using the docker build command while in the /scrumastr folder. Example:
`docker build -t yourname/chatscrum:example .`
