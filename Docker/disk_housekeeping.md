# 1. Disk space summary
Shows a summary of how much disk Docker is using, broken into Images, Containers, Local Volumes, and Build Cache. Each row gives the total size and how much is reclaimable. Running it first and last (as you've done) lets you see how much space the prune commands actually freed.
```
docker system df
```




# 2. Clear build cache
Clears the build cache — the intermediate layers BuildKit keeps to speed up rebuilds. By default it only removes dangling (unused) cache. The flag `-f` skips the "Are you sure?" confirmation prompt.
```
docker builder prune -f
```




# 3. Clear entire build cache
Same idea but `--all` removes the entire build cache, not just dangling entries, including cache that's still associated with existing images. Your next build will be slower since it has to redo everything from scratch. The previous line is essentially redundant once you run this one.
```
docker builder prune --all -f
```

# 4. Remove stopped containers
Removes all stopped containers. Running containers are untouched. This frees the thin writable layer each stopped container holds.
```
docker container prune -f
```




# 5. Remove images not currently used
```
docker image prune -a -f
```
Removes images. **Without the flag `-a` it only deletes dangling images (untagged layers). With `-a` it removes every image not currently referenced by a running or existing container, including tagged ones you pulled or built but aren't actively using.** This is usually where the big space savings come from, but it also means you'll need to re-pull and rebuild anything you need again.

> One thing worth flagging given a database setup: None of these touch volumes, so any database-stored data is safe here. **The data lives in named volumes, and volume pruning requires a separate `docker volume prune`**. That command is the one to be careful with, since it can wipe persisted database contents!




# Summary
The overall sequence is a fairly aggressive cleanup. It is fine for reclaiming space, just expect slower first builds and a round of image re-pulls afterward. One redundancy note: Since `docker builder prune --all -f` supersedes the plain docker builder prune -f right above it, you can drop the first of the two.