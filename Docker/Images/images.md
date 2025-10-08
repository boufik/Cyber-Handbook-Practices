# 1. Basics

| No | Action | Command |
|:----:|:----|:----|
| 1  | Pull an image (if image is not found locally, Docker pulls from DockerHub) | `docker pull <image_name>` |
| 2  | Pull a **specific version** of an image | `docker pull <image_name>:<image_version>` |
| 3  | List **all local** images | `docker images` |
| 4  | Remove **a local image** (requires its containers to have been stopped in prior) | `docker image rm <image_name>` |
| 5  | Remove **all unused images** | `docker image prune -a` |
