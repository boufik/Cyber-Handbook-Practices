# 1. Manage Containers Lifecycle

| No | Action | Command |
|:----:|:----|:----|
| 1  | Start a container from an image | `docker run <image_name>` |
| 2  | Start a container from an image, while giving it a **name** | `docker run --name <container_name> <image_name>` |
| 3  | Start a container from an image, while starting an **interactive shell** | `docker run -it <image_name>` |
| 4  | Start a container from an image, making it **detached** (running in background) | `docker run -d <image_name>` |
| 5  | Restart a container (**running or stopped**) | `docker restart <container_name>` |
| 6  | Rename a container | `docker rename <old_name> <new_name>` |
| 7  | Stop a running container | `docker stop <container_name>` |
| 8  | Force-stop a running container (**kill immediately, no graceful shutdown**) | `docker kill <container_name_or_id>` |
| 9  | Remove **a stopped** container | `docker container rm <container_name>` |
| 10 | Remove **all stopped** containers | `docker container prune` |
| 11 | Override a Dockerfile-declared `ENV` variable during runtime | `docker run --env <ENV_name>=<ENV_value> <image_name>` |


# 2. Inspection and Interaction

| No | Action | Command |
|:----:|:----|:----|
| 1  | List **all** containers (running + stopped) | `docker ps -a` |
| 2  | List **running** containers | `docker ps` |
| 3  | Filter **running** containers by name | `docker ps -f "name=<container_name>"` |
| 4  | View **existing** logs from a container | `docker logs <container_name>` |
| 5  | View **live** logs from a container | `docker logs -f <container_name>` |
| 6  | Execute **a single command** inside a running container | `docker exec -it <container_name> <command>` |
| 7  | Spawn **an interactive shell** inside a running container (to execute commands) | `docker exec -it <container> /bin/bash` |
| 8  | Inspect detailed **configuration and metadata** of a container | `docker inspect <container_name>` |
| 9  | View **real-time resources usage** (CPU, memory) of a container | `docker stats <container_name>` |
| 10 | View the **processes running** inside a container | `docker top <container_name>` |

# 3. Notes

In every command that we can use `<image_name>` or `<container_name>`, we can instead use the image/container's ID like this: `<image_id>` or `<container_id>`.
