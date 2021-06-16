# Jupyter notebook image 

This notebook folder contains Dockerfile for a single user notebook image which based on Jupyter docker stack.
In addition to the base notebook, it contains all of the necessary packages for the tools. 
The docker image is suitable for running/testing locally and for deploying it by the jupyterhub on a kubernetes cluster.

## Building/using your own docker image

```bash
git clone https://github.com/fekad/surfascope-docker.git
cd surfascope-docker
```

### Building the docker image locally

```bash
docker build -t surfascope-docker:latest .
```

### Testing/Developing the notebooks locally
- Use the following command to run the docker image locally:
  ```bash
  docker run --rm \
             -p 8888:8888 \
             -v $PWD/notebooks:/home/jovyan/notebooks \
             --name surfascope-docker \
             surfascope-docker:latest 
  ```
  Note: Although the `--rm` option is useful, you have to use it very carefully. When you stop the notebook server, you can lose all of your modifications which hasn't been stored into the mounted folder.

- To attach a terminal to the running container, you can use the following command:
  ```bash
  docker exec -it surfascope-docker start.sh
  ```
  
More info: https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html?highlight=root#alternative-commands
    
    
### Useful tricks for Linux

- For mounting a folder, you may need to use an absolute path or other tricks if the PWD environmental variable is not accessible in your shell:
  ```bash
  docker run --rm \
             -p 8888:8888  \
             -v /path/for/the/notebooks:/home/jovyan/notebooks  \
             --name workflows-workshop \
             surfascope-docker:latest
  ```
- you may need to change the user id in the container - by adding `--user root` and `-e NB_UID=1001` options to your command - to have access for the mounted folders:
  ```bash
  docker run --rm \
             --user root \
             -e NB_UID=1001 \
             -p 8888:8888  \
             -v $PWD/notebooks:/home/jovyan/notebooks  \
             --name workflows-workshop \
             surfascope-docker:latest
  ```
- you can have a password-less sudo access in the container for debugging by adding `--user root` and `-e GRANT_SUDO=yes` options to your command:
  ```bash
  docker run --rm \
             --user root \
             -e GRANT_SUDO=yes \
             -p 8888:8888  \
             -v $PWD/notebooks:/home/jovyan/notebooks  \
             --name workflows-workshop \
             surfascope-docker:latest
  ```
    
More information about the command line options: https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html#notebook-options



