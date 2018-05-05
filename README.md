#BlogApp
## Setting up the VirtualEnv
#### For UNIX based devices(linux/mac)
To be able to run the project, you should either be having libraries mentioned in requirnments.txt in your PC(The same version) or you can create your virtual env with all these libraries in few simple steps! (Recommended)<br>

```
$ python -m venv env # where env is name of our virtual environment
$ source env/bin/activate
$ (env) pip install -r requirnments.txt
```
<hr></hr>

#### Windows 
Open windows power shell and change directory to the same as home directory of project (where readme.md is)<br>
Write in the following commands to set up your virtualenv

```
> pip install virtualenv # if virtualenv isn't installed
> virtualenv env # where env is name of virtual env
> env/Scripts/activate
> (env) pip install -r requirnments.txt
```
<strong>NOTE: If you aren't able to activate the environment, you may need to change your execution policy. It's really simple, open powershell as an admin and write the following command -></strong>
```
Set-ExecutionPolicy -ExecutionPolicy Unrestricted
```

# Running the project ->
clone the project or download zip<br>
Run the following command in terminal to run the app (while being in the BlogApp directory) ->
```
$python3 app.py
```

# Add an admin ->
write the following commands in terminal (while being in BlogApp directory) ->
```
$ python
>>> from app import db, Admin
>>> from werkzeug.security import generate_password_hash
>>> admin = Admin(username="YOUR_USERNAME", password=generate_password_hash("YOUR_PASSWORD", method='sha256'))
>>> db.session.add(admin)
>>> db.session.commit()
```
<hr> </hr>

### ~Neverwannafly
