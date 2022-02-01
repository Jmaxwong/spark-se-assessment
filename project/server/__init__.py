import os
import sys

if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(
        branch=True,
        include='project/*',
        omit=[
            'project/tests/*',
            'project/server/config.py',
            'project/server/*/__init__.py'
        ]
    )
    COV.start()

import click
from flask import Flask, make_response, jsonify #ADDED make_response and jsonify and blueprint
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.server.models import User
migrate = Migrate(app, db)

# from project.server.auth.views import auth_blueprint
# app.register_blueprint(auth_blueprint)

@app.route("/")
def root_site():
#def get():
    return "<p>It works!</p>"
    # responseObject = {
    #         'status': 'success',
    #         'message': 'Welcome to the website!'
    # }
    # return make_response(jsonify(responseObject)), 201

# class HomeAPI(MethodView):
#     """
#     Home Resource 
#     """
#     def get(self):
#         responseObject = {
#             'status': 'success',
#             'message': 'Welcome.'
#         }
#         return make_response(jsonify(responseObject)), 201

# home_view = HomeAPI.as_view('home_api')
# auth_blueprint.add_url_rule(
#     '/',
#     view_func=home_view,
#     methods=['GET']
# )

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
                help='Run tests under code coverage.')
def test(coverage):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        if COV:
            COV.stop()
            COV.save()
            print('Coverage Summary:')
            COV.report()
            basedir = os.path.abspath(os.path.dirname(__file__))
            covdir = os.path.join(basedir, 'tmp/coverage')
            COV.html_report(directory=covdir)
            print('HTML version: file://%s/index.html' % covdir)
            COV.erase()
        return 0
    return 1
