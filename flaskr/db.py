import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
	"""
	Return database stored in g?
	"""
	if "db" not in g:
		g.db = sqlite3.connect(
			current_app.config["DATABASE"],
			detect_types = sqlite3.PARSE_DECLTYPES
			)
		g.db.row_factory = sqlite3.Row
	return g.db

def close_db(e=None):
	"""
	close the db
	"""
	db = g.pop("db", None)
	if db is not None:
		db.close()

def init_db():
	"""
	init the db by opening the sql table
	"""
	db = get_db()

	with current_app.open_resource("schema.sql") as f:
		db.executescript(f.read().decode('utf8'))

@click.command("init-db") # defines command line command "flask init-db" that executes init_db_command
@with_appcontext
def init_db_command():
	"""
	establishes CLI command to init db and return positive response
	"""
	init_db()
	click.echo("Initialized database")

# is this a special name fct? no it's not! it's just called in init.py
def init_app(app):
	"""
	link these methods to __init__.py factory app creating function thign
	"""
	app.teardown_appcontext(close_db) # link the tearing down of flask app with callign close_db
	app.cli.add_command(init_db_command) # link the new CLI command created via init_db_command to app
