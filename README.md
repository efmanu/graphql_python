# graphql_python
Example code to create graphql implementation with python


# GQL With Graphene + SQLAlchemy + Flask + Alembic

# Setup postgres db using docker 
```
docker run -d --name postgres-alembic-test-container \
    -e POSTGRES_DB=testdb \
    -e POSTGRES_USER=root \
    -e POSTGRES_PASSWORD=password \
    -p 5466:5432 \
    postgres:latest

```

# Create Virtual Environemnt
```
virtualenv -p python3 venv
source venv/bin/activate 
```

# Install necessary packages
```
pip install graphene graphene-sqlalchemy flask sqlalchemy alembic uuid flask_graphql
```

If you are using Mac ARM processor
```
pip install psycopg2-binary --force-reinstall --no-cache-dir
```

# DB Migration
# Init Alembic
```
alembic init alembic
```

# Update alembic.ini file
This is to update connection details
```
sqlalchemy.url = postgresql://root:password@localhost:5466/testdb
```

# Update alembic/env.py file
This is to insert the Base model. Import Base and update the target_metadata
```
from models import Base


target_metadata = Base.metadata
```

# Create Revison and migrate
Replace message with custom messages related to each revision
```
alembic revision -m "intial migration"

alembic upgrade head
```

OR

```
alembic-autogen-check || alembic revision --autogenerate -m 'Add new updates'
alembic upgrade head
```


# Run APp

```
python3 server.py
```


# Sample graphQL query and Mutations:

Open [http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql?operationName=cre&query=mutation%20cre%7B%0A%20%20createUser(userDetails%3A%5B%0A%20%20%20%20%7B%0A%20%20%20%20%20%20username%3A%22manu123%22%0A%20%20%20%20%20%20firstName%3A%22manu%22%0A%20%20%20%20%20%20lastName%3A%22Francis%22%0A%20%20%20%20%7D%0A%20%20%5D)%7B%0A%20%20%20%20users%7B%0A%20%20%20%20%20%20userId%0A%20%20%20%20%20%20username%0A%20%20%20%20%20%20firstName%0A%20%20%20%20%20%20lastName%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A%0Aquery%20liU%7B%0A%20%20getUser(username%3A%22manu123%22)%7B%0A%20%20%20%20username%0A%20%20%20%20firstName%0A%20%20%20%20lastName%0A%20%20%7D%0A%7D) in browser
``` 
mutation cre{
  createUser(userDetails:[
    {
      username:"manu123"
      firstName:"manu"
      lastName:"Francis"
    }
  ]){
    users{
      userId
      username
      firstName
      lastName
    }
  }
}

query liU{
  getUser(username:"manu123"){
    username
    firstName
    lastName
  }
}
```