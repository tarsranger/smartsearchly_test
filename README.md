install dependencies
```pip install -r requirements.txt```

run migration
```python manage.py migrate```

put the files at the root directory then run:
```python manage.py import_pois yourpoisfile.csv```
```python manage.py import_pois yourpoisfile.json yourpoisfile.xml```

create a super user
```python manage.py createsuperuser```

run server
```python manage.py runserver 8080```

go to ```http://127.0.0.1:8080/admin```
login with your superuser


There seemed to be different POIs with identical external_id, so it couldn't be relied on to check for duplicate values.
