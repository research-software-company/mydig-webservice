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
**Or** create a tasks.json file like this:
```
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "frontend",
            "type": "shell",
            "windows": {
                "command": "${workspaceFolder}/env/scripts/python.exe"
            },
            "args": ["service.py", "--tag-mydig-frontend"],
            "options": {
                "cwd": "${workspaceFolder}/frontend"
            },
            "problemMatcher": [],
        },
    ],
  }
```
	
frontend URL: *http://localhost:9880/*

### Backend:
#### Debugging with vs-code:
- create a lanch.json file, with the following configurations:
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: mydig-backend",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/ws/ws.py",
            "args" : ["-u", "--tag-mydig-backend"]
        }
    ]
}
```

- Debug -> Start debugging.

Backend URL: *http://localhost:9879/*

### Create db
- Follow the instructions in db/db_manager.md

	

