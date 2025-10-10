# 1. DockerHub

| No | Action | Command |
|:----:|:----|:----|
| 1 | Pull an image (at first searches **locally**, otherwise in **DockerHub**) | `docker pull <image_name>` |
| 2 | Pull a **specific version** of an image | `docker pull <image_name>:<image_version>` |


# 2. Private Registries

| No | Action | Command |
|:----:|:----|:----|
| 1 | Login to private registry | `docker login <private_registry_url>` |
| 2 | Pull an image from a **private registry** | `docker pull <private_registry_url>/<image_name>` |
| 3 | **Rename** an image to start with registry URL (and then **to push**) | `docker tag <image_name> <private_registry_url>/<image_name>` |
| 4 | Push an image to a private registry | `docker image push <private_registry_url>/<image_name>` |


# 3. Inspection and Storage

| No | Action | Command |
|:----:|:----|:----|
| 1 | List **all local** images | `docker images` |
| 2 | Save an image to a `.tar` file | `docker save -o <tar_file> <image_name>` |
| 3 | Load an image from a `.tar` file | `docker load -i <tar_file>` |
| 4 | Remove **a local image** (requires its containers to have been stopped in prior) | `docker image rm <image_name>` |
| 5 | Remove **all unused images** | `docker image prune -a` |
