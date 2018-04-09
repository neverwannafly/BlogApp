# Evaluation Project

# Running the project ->
## clone the project or download zip
## Run the following command in terminal to run the app (while being in the BlogApp directory) ->
### $source ../env/bin/activate
### $python3 app.py

# Add an admin ->
## write the following commands in terminal (while being in BlogApp directory) ->
### $python3
### >>> from app import db, Admin
### >>> admin = Admin(username="YOUR_USERNAME", password=generate_password_hash("YOUR_PASSWORD", method='sha256'))
### >>> db.session.add(admin)
### >>> db.session.commit()

# Infinite Scroll ->
### Currently I am experiencing a lot of UI bugs due to implementation of infinite scroll.
### I'll look onto fixing the bug
### However the backend code could be easily written as:
### posts = Post.query.filter(Post.unique_id>=int(CURRENT_INDEX)).limit(5).all()
### which returns only 5 posts, as we keep track of CURRENT_INDEX counter
### in your program

### @Neverwannafly~
