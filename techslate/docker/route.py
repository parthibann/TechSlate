import json
from flask_restful import request
from flask_restful import Resource
from techslate.utils.route_utils import get_response
from techslate.utils.route_utils import error_handler
from techslate.docker.actions import DockerActions


class Docker(Resource):
    def __init__(self):
        self.actions = DockerActions()

    def get(self, resource=None, container_id=None):
        try:
            if resource == 'images':
                status, res_body = self.actions.list_techslate_images()
            elif resource == 'containers':
                status, res_body = self.actions.list_techslate_containers()
            elif container_id:
                status, res_body = self.actions.stop_techslate_container(container_id)
            else:
                status, res_body = 400, json.dumps({"message": "Bad request"})
            return get_response(status, res_body)
        except Exception as err:
            return error_handler(err)

    def post(self, action=None):
        try:
            ui_data = request.form.to_dict()
            req_body = ui_data if ui_data else json.loads(request.get_data())
            if action == "start":
                status, res_body = self.actions.start_techslate_container(req_body)
            else:
                status, res_body = 400, json.dumps({"message": "Bad request"})
            return get_response(status, res_body)
        except Exception as err:
            return error_handler(err)
