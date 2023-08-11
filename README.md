# Continuous Intelligence Final Project

- Repository: [cintel-07-final](https://github.com/bambee26./cintel-07-final)
- Website: [cintel-07-final](https://bambee26.github.io/cintel-07-final/)
- Author: [Bambee Garfield](https://github.com/bambee26)

-----

## Create New Repository

Import Module 6 repository into a new cintel-07-final repo in Github

-----

## Setup project in VS Code

Using a PowerShell terminal in this cintel-07-final folder on your machine. 
Create a virtual environment named .venv in the current directory. 
Verify that a .venv folder was created after running the command. 

```shell
python -m venv .venv
```

If VS Code asks to use it as the workspace folder, select Yes.

## Activate the Environment

Run the following command to activate the virtual environment we just created.
Verify that the PowerShell prompt now shows (.venv) at the beginning of the line.

```shell
.venv\Scripts\activate
```

## Prepare the Environment

Run the following commands to upgrade pip and install required packages.
Rerun as needed until everything is successfully installed.

```shell
python -m pip install --upgrade pip wheel pyodide-py
python -m pip install --upgrade -r requirements.txt
```
-----

## Run the App

Verify your virtual environment is activated and packages have been installed. 
Run the following PowerShell command to start the app.

```shell
shiny run app.py
```
Hit CTRL c (at the same time) to quit the app. 
