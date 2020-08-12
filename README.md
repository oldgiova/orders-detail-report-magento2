# orders-detail-report-magento2
A flask application which shows you an orders detail report from Magento2

## Credits
A huge thanks to [Miguel Grinberg](https://blog.miguelgrinberg.com/index) and its [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world): this work is strongly inspired by this wonderful tutorial.


## Database
The database is for users only and I'm using a local sqllite, but you can set anything you want in (config.py) file

### DB Initialization
```
(venv) $ flask db init
(venv) $ flask db migrate -m "users table"
(venv) $ flask db upgrade
```

## User setup
You first need to define a login user:
```
>>> from app import db
>>> from app.models import User
>>> u = User(username='admin', email='admin@example.com')
>>> u.set_password('mypassword')
>>> db.session.add(u)
>>> db.session.commit()
```

If you want to query:
```
>>> users = User.query.all()
```

## starting the app
```
pip install -r requirements.txt
source ./venv/bin/activate
flask run
```
