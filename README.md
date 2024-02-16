# Todo App

A fullstack todo app using Python/Flask for the backend and Jinja2-rendered frontend templates. There are four pages: `create`, `home`, `rename`, `remove`. These correspond to the basic CRUD operations.

## Storage

Internally, this uses SQLAlchemy as an ORM. To connect a database, ensure one is running, then set the environment `DB_URL` to the connection URI. This can be set either in the terminal or put in the `.env` file