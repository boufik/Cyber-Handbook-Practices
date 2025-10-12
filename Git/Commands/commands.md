# 1. Basic Git commands

| No | Action | Command | Example |
| :---- | :---- | :---- | :---- |
| 1 | Initialize a new Git repo | `git init` | `git init` will create a new `.git/` folder and **"convert" the directory into a Git repo**. |
| 2 | Clone an existing remote repo with **HTTPS** | `git clone <repo_url>` | `git clone https://github.com/<user>/<project_name>.git)` |
| 3 | Clone an existing remote repo with **SSH** | `git clone <repo_url>` | `git clone git@github.com:<user>/<project_name>.git` |
| 4 | Track/Stage a file for the first time | `git add <file>` | `git add main.py` adds the file `main.py` in the staging area, before committing |
| 5 | Track/Stage **all files** for the first time | `git add .` | Adds every file in the staging area, before committing |
| 6 | Check the current repo status | `git status` | Shows untracked, modified, and staged files. |
| | | | |
|  **6** | Commit staged changes with a message               | `git commit -m "<message>"`                     | `git commit -m "Fix: corrected login bug"` |
|  **7** | View your commit history                           | `git log`                                       | Press `q` to exit the history view. |
|  **8** | View compact commit history                        | `git log --oneline --graph --decorate`          | Great for visualizing branch history. |
|  **9** | See what changed since the last commit             | `git diff`                                      | Shows unstaged changes. |
| **10** | See what was staged (ready to commit)              | `git diff --staged`                             | Shows staged differences. |
| **11** | Check what branch you are on                       | `git branch`                                    | Lists local branches and highlights the current one. |
| **12** | Create a new branch                                | `git branch <branch_name>`                      | `git branch feature/login-ui` |
| **13** | Switch to another branch                           | `git checkout <branch_name>`                    | `git checkout main` |
| **14** | Create **and** switch to a new branch              | `git checkout -b <branch_name>`                 | `git checkout -b feature/api-endpoint` |
| **15** | Delete a local branch (safe only if merged)        | `git branch -d <branch_name>`                   | `git branch -d feature/old-branch` |
| **16** | Force delete a local branch                        | `git branch -D <branch_name>`                   | Use with caution — removes without merge check. |
| **17** | Push a local branch to the remote repo             | `git push -u origin <branch_name>`              | `git push -u origin feature1`                                                 |
| **18** | Pull the latest remote changes                     | `git pull origin <branch_name>`                 | `git pull origin main` — always do before pushing.                            |
| **19** | Push committed changes to remote                   | `git push`                                      | Sends all local commits on current branch.                                    |
| **20** | View configured remotes                            | `git remote -v`                                 | Lists fetch/push URLs for the repo.                                           |
| **21** | Add a new remote repo                              | `git remote add origin <repo_url>`              | `git remote add origin git@github.com:user/project.git`                       |
| **22** | Rename a remote                                    | `git remote rename origin upstream`             | Useful when forking projects.                                                 |
| **23** | Remove a remote                                    | `git remote remove <name>`                      | `git remote remove upstream`                                                  |
| **24** | Undo local unstaged changes                        | `git restore <file>`                            | Restores last committed version of that file.                                 |
| **25** | Unstage a file (keep working changes)              | `git restore --staged <file>`                   | Opposite of `git add`.                                                        |
| **26** | Show current configuration                         | `git config --list`                             | Shows name, email, merge editor, etc.                                         |
| **27** | Set your Git username                              | `git config --global user.name "<your_name>"`   | `git config --global user.name "John Doe"`                                    |
| **28** | Set your Git email                                 | `git config --global user.email "<your_email>"` | Must match your GitHub email for proper linking.                              |
| **29** | Show branch tracking info                          | `git branch -vv`                                | Indicates which remote branch each local branch tracks.                       |
| **30** | View remote-tracked branches                       | `git fetch --all` + `git branch -r`             | Fetches all remote changes for viewing.                                       |

