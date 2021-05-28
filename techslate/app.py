import os
from flask import Flask
from flask import render_template
from flask_restful import Api
from techslate.utils.route_utils import error_handler
from techslate.docker.route import Docker

current_path = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(current_path, os.pardir, "techslate_ui")

app = Flask("techslate", template_folder=ui_path, static_folder=ui_path + os.sep + 'static')
app.register_error_handler(Exception, error_handler)
api = Api(app)

# resource = images / containers -> to list them
# action = start / stop, start using image name and stop using container id.
api.add_resource(Docker, '/v1/<resource>', '/v1/docker/<action>', '/v1/docker/stop/<container_id>')


@app.route('/')
def homepage():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return "404 - Not Found. The requested resource is not available on the server."

