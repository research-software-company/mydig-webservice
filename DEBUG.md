# How to debugging the project 'mydig-ws':

## In dig-etl-engine directory:
- Switch to the branch "debug-mydig-ws".
- Create an *.env*  file with the configurations like *.env.example*  file.
- Create empty directory and set the value of the variable `DIG_PROJECTS_DIR_PATH` in your *.env*  file to the new dir path.
- Run  `.\engine-debug-mydig-ws.ps1 up`. (This command will run the docker-compose-debug-mydig-ws with the file dig_no_auth_basic.conf)

## In the mydig-ws directory:
- Switch to the branch "user-projects".
- Create a virtual environment for python.
```
	virtualenv --python=C:\Python37\python.exe env
	Activate-Virtenv
	pip install -r requirements.txt
```

- Create an *.env*  file with the configurations like *.env.example*  file.
- Set the value for the variable `DIG_PROJECTS_DIR_PATH` in your *.env*  file to the directory you've created in dig-etl-engine.
- Create a file `local_config.py` from the file `local_config.example.py`.

### Frontend:
Run the frontend from your frontend directory:
`cd frontend`

There is a Frontend task configured in Visual Studio Code

frontend URL: *http://localhost:9880/*

### Backend:
#### Debugging with vs-code:

There is a Backend Launch Configuration in Visual Studio code, use it.

- Debug -> Start debugging.

Backend URL: *http://localhost:9879/*

### Create db
- Follow the instructions in db/DB_MANAGER.md

	

