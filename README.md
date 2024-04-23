# graphql_python
Example code to create graphql implementation with python


# GQL With Graphene + SQLAlchemy + Flask

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