| No | Action | Command |
|:-----|:------|:------|
| 1  | Start a container from an image | `docker run <image_name>` |
| 2  | Start a container from an image, while giving it a name | `docker run --name <container_name> <image_name>` |
| 3  | Start a container from an image, while starting an interactive shell | `docker run -it <image_name>` |
| 4  | Start a container from an image, making it detached (running in background) | `docker run -d <image_name>` |
| 5  | List **ALL** containers (running + stopped) | `docker ps -a` |
| 6  | List only the **RUNNING** containers | `docker ps` |
| 7  | Filter **RUNNING** containers by name | `docker ps -f "name=<container_name>"` |
| 8  | View **EXISTING** logs from a container | `docker logs <container_name_or_id>` |
| 9  | View **LIVE** logs from a container | `docker logs -f <container_name_or_id>` |
| 10  | Stop a running container | `docker stop <container_name_or_id>`
| 11 | Force-stop a running container (kill immediately, no graceful shutdown) | `docker kill <container_name_or_id>` |
| 12 | Remove a stopped container | `docker container rm <container_name_or_id>` |
