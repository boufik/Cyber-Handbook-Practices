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

# 2. About `.gitignore`

If the code inside our `streamapp` folder is written in Python, a `venv` folder may also be present inside the folder `streamapp`. You activate and deactivate this `venv` in order to `pip install` and run your code with the command `python`. But, we do NOT want such **files** to be pushed in our remote repo. An example of a **folder** we would NOT like to push remotely as well is the folder `__pycache__`. Thus, we need to configure our local repo in a way that does NOT care about these files and their corresponding changes. We need to create a `.gitignore` file by typing the command `touch .gitignore` under the directory of our project (`/.../streamapp`).
