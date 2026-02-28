With the help of ChatGPT and in accordance with what is said in official GitHub documentation, we define these steps.

# Steps after a successful `git clone` or a successful PR

## 1. Start with the latest `main`

Every new task should start from a clean, updated `main` branch:

```
1a)  git checkout main
1b)  git pull origin main
```

✅ Why: Ensures you’re building on the latest code, avoids conflicts later.

## 2. Create a new branch for your task

```
2a)  git checkout -b feature_branch
```

✅ Why: Never work directly on `main`. Branches isolate your work and make PRs possible.

## 3. Work and commit changes

After editing files:

```
3a)  git add .
3b)  git commit -m "Add feature XYZ"
```

✅ Why: `add` stages changes, `commit` saves them locally. Good commit messages help teammates.

# 4. Push branch to GitHub

```
4a)  git push -u origin feature_branch
```

✅ Why: Publishes your work to GitHub and lets you open a Pull Request.

# 5. Open a Pull Request (PR) on GitHub

Target: merge your `branch → main`. Fill in description: what you changed, why, how to test. Request review if you’re on a team.

✅ Why: PRs are the professional way to merge changes — they allow review, discussion, and CI checks.

# 6. Keep your branch up to date

If `main` moved forward while you were coding:

```
6a)  git fetch origin
6b)  git merge origin/main   # or: git rebase origin/main (FOR cleaner history)
6c)  git push
```

✅ Why: Keeps your branch compatible with main. Prevents merge conflicts at the last moment. These changes may have no effect for solo projects, if no changes are made between the time of the PR and the current time of commands execution.

# 7. Merge your PR

Once approved and tests pass, merge via GitHub. Preferred strategy for beginners: `Squash and Merge` → keeps main clean with one commit per feature.

✅ Why: `main` stays tidy, history is easy to read.

# 8. Clean up

After merge:

```
8a)  git checkout main
8b)  git pull origin main
8c)  git branch -d feature_branch
8d)  git push origin --delete feature_branch        # optional but recommended
```

✅ Why: Keeps repo clean, avoids old stale branches.

# Best Practices

* Never push directly to branch `main`. Always use a branch + PR.
* One branch per feature/bug. Short-lived, focused.
* Commit often, but keep messages clear. Example: `Fix bug in login validation (#45)`
* Pull (or rebase) before you `push`. Stay in sync with the team.
* Use GitHub PRs to merge. It’s the professional standard.
* Delete merged branches. Keeps the repo clean.

# Steps Cheat-Sheet

```
# Start new branch
git checkout main
git pull origin main
git checkout -b feature_branch

# Modify files
git add .
git commit -m "Added this specific feature"

# Publish the branch into the remote repo
git push -u origin feature_branch

# Create the PR using GitHub GUI

# If main was updated in the meanwhile
git fetch origin
git merge origin/main
git push

# Merge the PR

# After PR is merged
git checkout main
git pull origin main
git branch -d feature_branch
git push origin --delete feature_branch
```

# Fix mistake with branches

Suppose that I have made a mistake, and after the `git clone` command (or `git checkout main` and `git pull origin main`), I accidentally forgot to create a new branch named `feature_branch`. 

## Executed Commands

```
git checkout main
git pull origin main
# I forgot to branch
# I made changes, staged them + committed directly on main (locally)
```

Now, I have local commits on main that are not yet pushed. I want to:

* keep my work,
* avoid pushing directly to `origin/main`,
* open a PR so others can review it.
  
## Safe recovery steps

### 1. Create a new branch from my current `main`

This captures my current (edited) state and “copies” it in the new branch:

```
git checkout -b feature_branch
```

Now, my new branch includes the local commits (the ones I accidentally made in the `main` branch).

### 2. Reset your local `main` branch back to the remote state!

I will move the `main` branch back, so that it can match the remote version. This ensures that I will NOT accidentally push those changes. Go back to main and then, reset it to match what’s on GitHub:

```
git checkout main
git fetch origin					           # Step to reset
git reset --hard origin/main		     # Step to reset
```

This removes the local commits from `main` (but they’re safe — they live on the new branch now).  Now, the local `main` is clean and synced again.

### 3. `Push` your new branch to GitHub

```
git checkout feature_branch
git push -u origin feature_branch
```

This publishes the changes to GitHub, without touching the `main`.

### 4. Create a Pull Request

Go to `GitHub → repo_name → GitHub` will automatically suggest: `Compare & pull request: feature → main`. Open the PR, describe the work, and submit it for review. That’s it — the code is now visible to teammates, safely.
 
### 5. Optional cleanup

Once the PR is merged and reviewed:

```
git checkout main
git pull origin main
git branch -d feature_branch
git push origin --delete feature_branch
```


# Sync local disk files with remote repo files

Suppose that I work in `main` branch locally and I did a mistake by modifying some files. If I want to "reset" all these local disk-located files into the state they are in the latest commit in the remote GitHub repo, I should do:

```
git fetch origin main
git restore <filename>
```
