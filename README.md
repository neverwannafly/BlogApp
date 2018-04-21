# Evaluation Project

# Running the project ->
clone the project or download zip
Run the following command in terminal to run the app (while being in the BlogApp directory) ->
```
$source ../venv/bin/activate
$python3 app.py
```

# Add an admin ->
write the following commands in terminal (while being in BlogApp directory) ->
```
$python3
>>> from app import db, Admin
>>> admin = Admin(username="YOUR_USERNAME", password=generate_password_hash("YOUR_PASSWORD", method='sha256'))
>>> db.session.add(admin)
>>> db.session.commit()
```

### @Neverwannafly~
