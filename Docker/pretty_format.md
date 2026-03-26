# 1. `docker ps`

View important fields with:
```
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Status}}"
```

Output:
```
CONTAINER ID   IMAGE                             NAMES                                 STATUS
17e8b7d9a88b   multi-container-app-todo-app      multi-container-app-todo-app-1        Up 2 minutes
01cdff972b0e   mongo:6                           multi-container-app-todo-database-1   Up 3 minutes
75c471086af8   vulnerables/web-dvwa:latest       vuln-web                              Up 3 minutes
619fc483665f   welcome2:latest                   welcome2                              Up 3 minutes
6cfa9d43a603   docker/welcome-to-docker:latest   welcome-to-docker                     Up 3 minutes
```

# 2. `docker inspect`

View IP per container:
```
docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q)
```

Output:
```
/multi-container-app-todo-app-1 - 172.18.0.3
/multi-container-app-todo-database-1 - 172.18.0.2
/vuln-web - 172.17.0.3
/welcome2 - 172.17.0.4
/welcome-to-docker - 172.17.0.2
```
