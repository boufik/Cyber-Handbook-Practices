# 1. DockerHub

| No | Action | Command |
|:----:|:----|:----|
| 1 | Search an image on DockerHub | `docker search <keyword>` |
| 2 | Pull an image from DockerHub, if not found locally | `docker pull <image_name>` |
| 3 | Pull a **specific version** of an image | `docker pull <image_name>:<image_version>` |


# 2. Private Registries

| No | Action | Command |
|:----:|:----|:----|
| 1 | Login to a private registry | `docker login <private_registry_url>` |
| 2 | Pull an image from a private registry | `docker pull <private_registry_url>/<image_name>` |
| 3 | Rename an image to start with registry URL (and then **to push**) | `docker tag <image_name> <private_registry_url>/<image_name>` |
| 4 | Push an image to a private registry | `docker image push <private_registry_url>/<image_name>` |


# 3. Inspection

| No | Action | Command |
|:----:|:----|:----|
| 1 | List **all local** images | `docker images` |
| 2 | List **all local** images including the **dangling** ones | `docker images -a` |
| 3 | List **all image IDs** | `docker images -q` |
| 4 | Show detailed **metadata** about an image | `docker inspect <image_name>` |
| 5 | Show an image's **history** - including the layers used (do NOT store secrets in Dockerfile layers) | `docker history <image_name>` |

# 4. Maintenance

| No | Action | Command |
|:----:|:----|:----|
| 1 | Save an image to a `.tar` file | `docker save -o <tar_file> <image_name>` |
| 2 | Load an image from a `.tar` file | `docker load -i <tar_file>` |
| 3 | Export a container's filesystem as a `.tar` file | `docker export <container_name> -o <tar_file>` |
| 4 | Import an exported filesystem as an image | `docker import <tar_file> <image_name>` |

# 5. Cleanup

| No | Action | Command |
|:----:|:----|:----|
| 1a | Remove a local image (requires **its containers to have been stopped in prior**) | `docker image rm <image_name>` |
| 1b | Remove a local image (requires **its containers to have been stopped in prior**) | `docker rmi <image_name>` |
| 2  | **Force-remove** a local image (requires its containers to have been stopped in prior) | `docker rmi -f <image_name>` |
| 3  | Remove **unused/dangling** images | `docker image prune` |
| 4  | Remove **all unused** images | `docker image prune -a` |
