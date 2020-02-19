# How to debugging the project 'mydig-ws':

## In dig-etl-engine directory:
- Switch to the branch "debug-mydig-ws".
- Create an *.env*  file with the configurations like *.env.example*  file.
- Set the value for the variable `DIG_PROJECTS_DIR_PATH` in your *.env*  file.
- Run  `.\engine-debug-mydig-ws.ps1 up`.

## In the mydig-ws directory:
- Switch to the branch "debug-mydig-ws".
- Create a virtual environment for python.
```
	virtualenv --python=C:\Python37\python.exe env
	Activate-Virtenv
	pip install -r requirements.txt
```

- Create an *.env*  file with the configurations like *.env.example*  file.
- Set the value for the variable `DIG_PROJECTS_DIR_PATH` in your *.env*  file.

### Frontend:
	cd frontend
	python service.py --tag-mydig-frontend
	
frontend URL: *http://localhost:9880/*

### Backend:
####Debugging with vs-code:
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
- create a file *local_config.py* (copy the file *config_debug_mydig_ws.py*)
- Debug -> Start debugging.

Backend URL: *http://localhost:9879/*


	

