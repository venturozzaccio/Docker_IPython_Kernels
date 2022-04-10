# Custom Dockerized Ipython kernels
 This project let's you use IPython kernels in containers, the idea is to have a single Jupyter Lab instead of one in each container (like in jupyterlabstacks containers e.g. jupyter/datascience-notebook). Additionally, now the degubber is enabled by default so we can debug the code.
 Another advantage is that in this way we can connect our VSCode or Jetbrain DataSpell to our single Jupyter Lab and use our containerized kernels, debug the code and having complete control of the environment. 
 
 The python script is called by the kernel command that it's executed everytime jupyter starts a new kernel. The script creates a container and dinamically changes the connection parameters and the random ports used to communicate with the IPython. The IPython in the container reads the ports and use them to communicate with the Lab, we only forward those ports from the container to the host. 

```bash
pip install -r requirements.txt
```

Place your Dockerfile in any folder

```bash
cat /tmp/tmp.beePtQNXkS/Dockerfile

FROM python:3.7-slim-buster
RUN pip install --upgrade pip ipython ipykernel
```

Install the kernel

```bash
python install.py /tmp/tmp.beePtQNXkS/ my_new_shiny_kernel      
```

Now just launch your Jupyter Lab and you should see your kernel available.

```bash
jupyter lab
```

The kernel is a folder in a directory:

```bash
❯ jupyter --paths
 ....
runtime:
    {HOME}/.local/share/jupyter/runtime
```

To check installed kernels use:

```bash
ls {HOME}/.local/share/jupyter/kernels/
```