# 1. Basics

| No | Action | Command |
|:----:|:----|:----|
| 1  | Pull an image (first searches locally, otherwise in DockerHub) | `docker pull <image_name>` |
| 2  | Pull a **specific version** of an image | `docker pull <image_name>:<image_version>` |
| 3  | List **all local** images | `docker images` |
| 4  | Remove **a local image** (requires its containers to have been stopped in prior) | `docker image rm <image_name>` |
| 5  | Remove **all unused images** | `docker image prune -a` |
| 6  | Pull an image from **private registry** | `docker pull <private_registry_url>/<im_name>` |
| 7  | Rename an image to start with registry URL (and then to push) | `docker tag <im_name> <private_registry_url>/<im_name>` |
| 8  | Push an image to a private registry | `docker image push <private_registry_url>/<im_name>` |
| 9  | Login to private registry | `docker login <private_registry_url>` |
| 10 | Save an image to a `.tar` file | `docker save -o <tar_file> <im_name>` |
| 11 | Load an image from a `.tar` file | `docker load -i <tar_file>` |
