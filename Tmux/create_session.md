# 1. Start a new named session

Naming a tmux session makes it easier to find later. The next command opens a fresh shell inside tmux.
It looks like a normal terminal, but it can run in the background.
It even survives SSH session dropping, in case we are connected to a VM and we want to log out, but leave the task progressing.
```bash
tmux new -s my_bg_task
```

# 2. Activate the `venv` and run the script

```bash
cd /home/user/my_project
source venv/bin/activate
python3 my_script.py
```
Let it start printing progress lines as usual, to ensure all is OK.

# 3. Detach

To leave the script running in the background, press `Ctrl+B`, release and then press `D`.
We will drop back to our normal shell, so we are ready to terminate the SSH connection, if we want.
The script will keep running safe inside tmux on the connected VM.
We should just make sure that the VM will be on power.

# 4. Reattach anytime later

After reconnecting to the VM via a new SSH session, we can track the progress of the live script running through:
```bash
tmux attach -t my_bg_task
```
Again, to detach, press `Ctrl+B`, release and then press `D`.

# 5. Check progress without attaching

If we just want a quick peek on the status of the task, without reattaching, just run:
```bash
tmux capture-pane -t my_bg_task -p | tail -10
```

# 6. Save the output to a `.log` file after the task finishes

```bash
tmux capture-pane -t my_bg_task -p -S - > /home/user/my_project/output-$(date +%F).log
cat /home/user/my_project/output-*.log
grep -iE 'skip|warn|error' /home/user/my_project/output-*.log | head -50
```

# 7. Useful commands

To list all sessions an confirm that our task is indeed running (still alive):
```bash
tmux ls
```
If we want to deliberately want to stop the task, run:
```bash
tmux kill-session -t my_bg_task
```
The script is resumable, so this action is not destructive. It just means we need to re-run the script again later.
