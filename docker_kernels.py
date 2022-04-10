#!/usr/bin/python

import argparse
import json
from pathlib import Path

import docker


def set_connection_ip(connection_file, ip: str = "0.0.0.0"):
    connection = json.loads(Path(connection_file).read_text())
    connection["ip"] = ip
    connection["kernel_name"] = "my_custom_kernel"
    Path(connection_file).write_text(json.dumps(connection))
    return connection

parser = argparse.ArgumentParser(description="Running new container")
parser.add_argument("connection_file")
parser.add_argument("my_container")

args = parser.parse_args()

try:
    with open('args.connection_file', 'w') as f:
        set_connection_ip(f)
        raise 
        data = json.load(f)
except ValueError: 
    print('Decoding JSON has failed')
    exit()
except Exception as err:
    print('Error reading connection_file:', err)
    exit()

image_name = str(args.my_container)

ports = [
    data["shell_port"],
    data["iopub_port"],
    data["control_port"],
    data["stdin_port"],
    data["hb_port"],
]
port_mapping = {}
for i in ports:
    port_mapping[i] = i

env_vars = {}

CONTAINER_CONNECTION_SPEC_PATH = "/kernel-connection-spec.json"
CONTAINER_CONNECTION_SPEC_ENV_VAR = "DOCKERNEL_CONNECTION_FILE"

client = docker.from_env()
containers = client.containers

connection_file_mount = docker.types.Mount(
    target=CONTAINER_CONNECTION_SPEC_PATH,
    source=str(args.connection_file),
    type="bind",
    read_only=False,
)

try:
    containers.run(
        image=image_name,
        tty=True,
        command=f"python -m ipykernel_launcher -f {CONTAINER_CONNECTION_SPEC_PATH}",
        auto_remove=True,
        environment=env_vars,
        mounts=[connection_file_mount],
        ports=port_mapping,
        stdout=True,
        stderr=True,
    )
except Exception as err:
    print('Error running the container:', err)