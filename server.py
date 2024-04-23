# server.py
from flask import Flask
from flask_graphql import GraphQLView
from schema.schema import schema
from db.model import session
app = Flask(__name__)


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        get_context=lambda: {'session': session}  # Add this line
    )
)

if __name__ == '__main__':
    app.run()
