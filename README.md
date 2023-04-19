# python-rest-api-docker

This is a basic python rest api that utilises docker and persists data to a containerised postgres volume

There are 2 services; flask_app, flask_db

Commands to run this api:

1) docker compose up -d flask_db

2) docker compose build

3) docker compose up flask_app

4) docker compose up --build flask_app

You can check the success of this by trying to access the test endpoint http://localhost:4000/test which should return 

{'message':'test route'}

If successful, you can create users following this POST request 
```
curl -X POST -H "Content-Type: application/json" -d '{"username":"Niki", "email":"niki.ross49@gmail.com"}' http://localhost:4000/users
```

All users can be displayed with the following GET request 
```
curl -X GET http://localhost:4000/users
```
