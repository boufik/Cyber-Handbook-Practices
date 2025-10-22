# Current state

Imagine, you have created a local project in your host machine or inside a VM. You want to push it as it is right now to create a remote GitHub repo with the exact same name and the exact same content/files. To do this, we need to follow these steps.

# 1. Ensure that the current device is authorized

In order to push any local content/files to a remote repo, we need to have configured an SSH key for our current device/VM in prior. If you do not know how to do so, check the `device_authorization.md`.

# 2. Initialize Git locally

Let's call `streamapp` the local folder, inside which you have stored your code.

```
cd /..../streamapp
git init
```

# 3. About `.gitignore`

If the code inside our `streamapp` folder is written in Python, a `venv` folder may also be present inside the folder `streamapp`. You activate and deactivate this `venv` in order to `pip install` and run your code with the command `python`. But, we do NOT want such **files** to be pushed in our remote repo. An example of a **folder** we would NOT like to push remotely as well is the folder `__pycache__`. Thus, we need to configure our local repo in a way that does NOT care about these files and their corresponding changes. We need to create a `.gitignore` file by typing the command `touch .gitignore` under the directory of our project (`/.../streamapp`).

```
# Virtualenvs
venv/
.venv/

# Python caches
__pycache__/
*.py[cod]

# Env / secrets
.env

# IDE
.vscode/
.idea/
```

Then, we need to stage and commit **ONLY** the `.gitignore` file. So, the first time we use the command `git add` will refer to this file. The following command ensures ignored files will stay ignored when you add everything else!

```
git add .gitignore
git commit -m "First CLI commit - Added the file .gitignore to exclude venv and IDE files"
```

# 4. Commit the local folder code changes

By typing `git status`, we can see that the **other code changes** are still not tracked. The only file that has been committed so far is the `.gitignore` file. So:

```
git add .
git status
```

And then, commit the changes with a helping message:

```
git commit -m "Second CLI commit - Added the local folder's initial code changes"
```

At this point, ANY local change has been tracked locally!

# 5. Create a GitHub repo with the same name

Supposing that the name of the code folder is `streamapp`, we need to navigate to GitHub and create **manually** a new repository with the **exact same name** as the local folder. In the online platform of GitHub, while creating this repote repository, be careful NOT to include:
* a `README.md` file
* a `.gitignore` file
* any license

This way, a remote repo with the same name has been successfully created and it does NOT contain anything so far. After creating the remote repo, scroll down to see the final commands that GitHub prompts you to use in your local machine. Focus on the SSH-related commands:

```
git remote add origin git@github.com:<username>/<project_name>.git
git branch -M main
git push -u origin main
```

1. The first command copies the SSH URL from the GitHub page
2. The next one ensures consistency with GitHub defaults, as it renames the base branch to `main` (somteimes the base branch is named `master`)
3. The last command pushes everything (any committed local change) up to the remote repo with the exact same name

# 6. Verification

There are two ways that everything worked as expected:
* Navigate to your GitHub repositories tab and notice that the manually-created remote repo now contains the fodlers and files of your local changes.
* In your local machine, you can type `git pull origin main` and then a message like this will be shown:

```
From github.com:<username>/<project_name>
 * branch            main       -> FETCH_HEAD
Already up to date.
```
