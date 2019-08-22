## DPLog

An application of differential privacy to security monitorings

## Intro
Privacy and security auditing are always seen as opposing forces,
but does it have to be like that? Differential privacy offers
the mathematical tools to strike a balance between privacy and auditing.
This is why I have started to develop DPLog a host based agent that implements
state of the art algorithms to allow security queries with privacy.

## Components
The project is divided into the client which will run on multiple hosts and a server which will run
on a single host.

Folder structure explained:
* client: the client component
* server: the server component written in Django
* docker: containerized version of the server only
* docs: documents
* screens: screenshots

## Run server
The server currently runs on a file sqlite database.
Create a pyenv with python 3.6 and install the requirements:
* pip3 install -r requirements.txt
To run the server:
* remove the db.sqlite3
* manage.py check
* manage.py makemigrations
* manage.py migrate

Add an admin user with a password you want:

```
manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
```

Run the server:
* manage.py runserver

You should see something like this:

```
Django version 2.2, using settings 'controlstation.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

## Run client

Create a pyenv with python 3.6 and install the requirements:
* pip3 install -r requirements.txt

Compile the client to a windows binary by running:
```
compile.bat
```

Once the binary is compiled will be available in the dist folder.

You can then run it via the scheduler:
* start the task via scheduletask.ps1
* stop the task via stoptask.ps1






