#!/usr/bin/python

import argparse
import json
from pathlib import Path

import docker

parser = argparse.ArgumentParser(description="Installing new container")
parser.add_argument("dockerfile_folder")
parser.add_argument("tag")
args = parser.parse_args()

dockerfile_folder = args.dockerfile_folder
tag = args.tag

folder_path = Path.home() / Path(f".local/share/jupyter/kernels/{tag}/")
folder_path.mkdir(parents=True, exist_ok=True)

kernel_file = folder_path / "kernel.json"
kernel_file.unlink(missing_ok=True)

kernel = json.dumps(
    {
        "display_name": tag,
        "language": "python",
        "metadata": {"debugger": True},
        "argv": [
            "python",
            str(Path(__file__).resolve().parent / "docker_kernels.py"),
            "{connection_file}",
            tag,
        ],
    }
)

try:
    kernel_file.write_text(kernel)
except Exception as err:
    print('Error writing the new kernel:', err)
    exit(1)

client = docker.from_env()
client.images.build(path=dockerfile_folder, tag=tag)
