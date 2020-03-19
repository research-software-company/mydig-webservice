
Flask-Migrate==2.5.2
Flask-SQLAlchemy==2.4.1
Flask-Login==0.5.0
### Create the DB:

```sell

$env:FLASK_APP = "ws\app_base"
flask db init
flask db migrate
flask db upgrade

cd ..

``
Important- for the first time:
```python
from ws.app_base import db, app
db.metadata.clear()
from db.models import User, Project, UserType
with app.app_context():
    db.create_all(app=app)
    User.query.all()
```
Example- add a new user:

```python
admin = User(email='admin@gmail.com', password='123', user_type=UserType.ADMIN)
db.session.add(admin)
db.session.commit()

# db.session.rollback()

```

```python

# create a new user
user1 = User(email='admin2@gmail.com', password='123abc', type=)

# add the first project to user1
Project(name='p1', dir='my_path', user=user1)

# add the second project to user1
project2 = Project(name='p2', dir='my_path_2', user=user1)
user1.projects.append(project2)

# add user1 to the db
db.session.add(user1)
db.session.commit()

```

You can used the script: 'add_entity_db.py' to add a new user.