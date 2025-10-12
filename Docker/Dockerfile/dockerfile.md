# 1. In-Dockerfile basic commands

| No | Action | Command |
|:----:|:----|:----|
| 1 | Start from a base image | `FROM <base_image>` |
| 2 | Add a Shell command | `RUN <shell_command>` |
| 3 | Add a Shell command to run, when a container is created from an image (last layer) - **when this command exits, the container stops running** | `CMD <shell_command>` |
| 4 | Copy files from the current working directory to the image filesystem - **files from parent directories can NOT be copied**| `COPY` |
| 5 | Change the current working directory inside the image filesystem (like `cd`) | `WORKDIR` |
| 6 | Change the current user - Best practice is to **install any necessary packages as root user** and then create and **change to a regular user** | `USER` |
| 7 | Create a variable, that will "live" **only in the Dockerfile**, and that van be overwritten during **image's build-time** | `ARG` |
| 8 | Create a variable, that will "live" **both in Dockerfile and in the running container**, and that be overwritten during **container's run-time** | `ENV` |

# 2. Building an image from a Dockerfile

| No | Action | Command |
|:----:|:----|:----|
| 1 | Build an image from a Dockerfile providing the absolute path of Dockerfile | `docker build <absolute_path>` |
| 2 | Build an image from a Dockerfile given that the Dockerfile is in the current directory | `docker build .` |
| 3 | Build an image from a Dockerfile and provide a name for the built image | `docker build -t <image_name> .` |
