import os
from flask import Flask

def create_app(test_config=None):

	# create, configure the app
	app = Flask(__name__, instance_relative_config=True)

	# set default configs (secret_key is that value, DATABASE located at that path)
	app.config.from_mapping(
		SECRET_KEY="dev",
		DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
		)


	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile("config.py", silent=True)
	else:
		# load test config
		app.config.from_mapping(test_config)

	# make sure app.instance_path exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route("/hello")
	def hello():
		return "Hello, World!"


	from . import db
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)
	
	return app