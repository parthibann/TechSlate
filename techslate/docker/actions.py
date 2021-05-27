import docker
import docker.errors
import logging
import json
import os
import socket
import uuid
import threading
from apscheduler.schedulers.background import BackgroundScheduler


LOG = logging.getLogger(__name__)
sched = BackgroundScheduler()


class DockerActions(object):
    def __init__(self):
        self.docker_client = docker.from_env()
        self.current_file_path = os.path.dirname(__file__)
        self.config_path = os.path.join(self.current_file_path, '../../config/')
        self.tasks_file_path = os.path.join(self.current_file_path, 'tasks.json')

    def list_techslate_images(self):
        try:
            image_list = json.load(open(os.path.join(self.current_file_path,
                                                     'techslate_images.json')))
            LOG.info("Docker images listed successfully.")
            return 200, json.dumps(image_list)
        except Exception as err:
            LOG.error(err)
            raise Exception(err)

    def list_techslate_containers(self):
        try:
            container_details = list()
            containers = self.list_containers()
            for container in containers:
                container_details.append(self.form_container_data(container))
            LOG.info("Docker containers listed successfully.")
            return 200, json.dumps(container_details)
        except Exception as err:
            LOG.error(err)
            raise Exception(err)

    def form_container_data(self, container):
        config = json.load(open(os.path.join(self.config_path, 'config.json')))
        host_ip = config.get('docker_host')
        details = dict()
        details['name'] = container.name
        details['id'] = container.id[0:12]
        port = container.ports
        tcp_4200_port_details = port.get('4200/tcp')
        container_port = ""
        for eachPort in port:
            if eachPort == '4200/tcp':
                continue
            else:
                container_port = port[eachPort][0]['HostPort'] + ": " + eachPort
        details['port'] = container_port
        host_port = tcp_4200_port_details[0]['HostPort']
        details['url'] = 'http://' + host_ip + ':' + str(host_port)
        all_labels = container.labels
        if all_labels.get('user_label'):
            details['label'] = container.labels.get('user_label')
        else:
            details['label'] = ""
        return details

    def start_techslate_container(self, req_body):
        try:
            req_body["task_id"] = str(uuid.uuid4())
            req_body["action"] = "start"
            self.create_task(req_body)
            return 200, json.dumps({"message": "Request taken for processing. Please wait for 10 - 30 seconds for the contatiner to come to ready state."})
        except Exception as err:
            LOG.error(err)
            raise Exception(err)

    def stop_techslate_container(self, container_id):
        try:
            task_data = dict()
            task_data["task_id"] = str(uuid.uuid4())
            task_data["container_id"] = container_id
            task_data["action"] = "stop"
            self.create_task(task_data)
            return 200, json.dumps({"message": "Request taken for processing."})
        except Exception as err:
            LOG.error(err)
            raise Exception(err)

    def pull_image(self, name):
        return self.docker_client.images.pull(name)

    def get_image(self, name):
        return self.docker_client.images.get(name)

    def list_images(self):
        return self.docker_client.images.list()

    def start_container(self, name, port, label):
        container_ports = {'4200/tcp': self.get_available_port()}
        if port:
            port_name = str(port) + '/tcp'
            container_ports[port_name] = self.get_available_port()
        container_labels = {"image": "techslate"}
        if label:
            container_labels["user_label"] = label
        return self.docker_client.containers.run(name, detach=True, ports=container_ports,
                                                 labels=container_labels)

    def list_containers(self, filters=None):
        if not filters:
            filters = {"label": "image=techslate"}
        return self.docker_client.containers.list(filters=filters)

    def stop_container(self, name):
        container = self.docker_client.containers.get(name)
        return container.stop()

    def get_available_port(self):
        new_socket = socket.socket()
        new_socket.bind(("", 0))
        return new_socket.getsockname()[1]

    def create_task(self, task):
        with open(self.tasks_file_path, 'r') as task_file:
            data = json.load(task_file)

        with open(self.tasks_file_path, 'w+') as task_file:
            data.append(task)
            json.dump(data, task_file)

    def delete_task(self, task):
        with open(self.tasks_file_path, 'r') as task_file:
            data = json.load(task_file)

        with open(self.tasks_file_path, 'w+') as task_file:
            data.remove(task)
            json.dump(data, task_file)

    def task_2_start_container(self, task):
        try:
            image_tag = task.get("image_tag")
            port = task.get("port")
            label = task.get("label")
            self.delete_task(task)
            try:
                self.docker_client.images.get(image_tag)
            except docker.errors.ImageNotFound:
                LOG.warning("Docker image '%s' not available locally." % image_tag)
                LOG.info("Pulling docker image '%s'." % image_tag)
                self.docker_client.images.pull(image_tag)
            self.start_container(image_tag, port, label)
        except Exception as err:
            LOG.error("Error wile processing the task %s, ERROR=%s " % str(task), str(err))

    def task_2_stop_container(self, task):
        container_id = task.get("container_id")
        self.delete_task(task)
        try:
            self.docker_client.containers.get(container_id)
            LOG.info("Stopping docker container '%s'." % container_id)
            self.stop_container(container_id)
        except docker.errors.NotFound:
            LOG.info("Docker container '%s' not available" % container_id)


# ---------------

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    threads = []
    da = DockerActions()
    with open(os.path.join(os.path.dirname(__file__), 'tasks.json'), 'r') as task_file:
        data = json.load(task_file)
    for each_task in data:
        action = each_task["action"]
        if action == "start":
            t = threading.Thread(target=da.task_2_start_container, args=(each_task,))
            threads.append(t)
        elif action == "stop":
            t = threading.Thread(target=da.task_2_stop_container, args=(each_task,))
            threads.append(t)
        else:
            LOG.error("Invalid action specified, action = %s" % action)
    for thread in threads:
        thread.start()


sched.start()
