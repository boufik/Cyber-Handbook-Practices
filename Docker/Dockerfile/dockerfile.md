# 1. Dockerfile basic Commands

| No | Action | Command |
|:----:|:----|:----|
| 1 | Start from a base image | `FROM <base_image>` |
| 2 | Add a Shell command | `RUN <shell_command>` |
| 3 | Add a Shell command to run, when a container is created from an image (last layer) - when this command exits, the container stops running | `CMD <shell_command>` |
| 4 | Create a variable, that will "live" only in the Dockerfile, and that van be overwritten during image build-time | `ARG` |
| 5 | Create a variable, that will "live" both in Dockerfile and in the running container, and that be overwritten during runtime | `ENV` |
| 6 | Change the current working directory inside the image filesystem (like `cd`) | `WORKDIR` |
| 7 | Change the current user - Best practice is to install any necessary packages as root user and then create and change to a regular user | `USER` |
