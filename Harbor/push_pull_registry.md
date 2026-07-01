# Harbor Container Registry

Harbor is a **self-hosted, private container registry**.
We can imagine it like a private DockerHub.
It supports private projects, access control, vulnerability scanning and works with the standard `docker push` and `docker pull` commands.




## 1. Prerequisites

- A Harbor instance accessible at `https://<harbor-domain>`
- A Harbor user account (created by the admin)
- A local Docker image ready to push to Harbor




## 2. Robot Accounts

Many organizations prefer robot accounts over personal credentials even for individual interactive use, since they are scoped, revocable, and don't tie pushes to a personal account that might have broader permissions elsewhere.

> **⚠️ DISCLAIMER: Robot accounts are intended exclusively for CLI and API operations (`docker login`, `docker push`, `docker pull`).
> They cannot be used to log into the Harbor web UI. Attempting to use robot account credentials on the browser login page will always fail. This is expected behavior, not a bug.**

### 2a. Create a Robot Account

1. Navigate to your project → click the **Robot Accounts** tab.
2. Click the button **`+ NEW ROBOT ACCOUNT`*.*
3. Fill in the form:
   - **Name**: Since robot accounts are project-specific, put something descriptive such as `<username>-<project>`. Harbor will automatically prefix it as `robot$<project_name>+<robot_account_name>`
   - **Description**: An example could be `"Push and pull permissions for the development of <project>"`.
   - **Expiration**: Set a reasonable expiry like `90 days`s or `Never` (often depending on the organization's policy).
4. Set **Permissions**, only scoped to this project:
   - ✅ Pull Repository: required for consumers and integrators
   - ✅ Push Repository: required for developers pushing images
   - ✅ Read Repository: required for basic access
   - ⬜ Delete: only if explicitly needed, not recommended
5. Click **Add**.
6. **CRITICAL ⚠️**: Harbor shows the robot account token **only once** at creation time, so copy it immediately and store it securely via a password manager for example. It can not be retrieved again, only regenerated.

### 2b. Robot Account Naming Convention

Harbor automatically formats robot account usernames as:
```
robot$<project_name>+<robot_account_name>
```
Example: `robot$wifiproject+thomas-wifitool`

For the `docker login` command, use this exact string, including the `robot$` prefix and `+` separator.

### 2c. Separate Accounts per Role

Regarding robot account permissions, a useful tip is this:
- **Developers** → push + pull + read repository
- **Consumers / Integrators** → pull + read (optionally) repository




## 3. Push an Image to Harbor

### Step 1: Login
```bash
docker login <harbor-domain> -u 'robot$<project_name>+<robot_account_name>'
# Enter the robot account token as the password when prompted
```

After filling in the Harbor-copied password, a warning may appear, but this is normal. The warning will say:
```
Password:

WARNING! Your credentials are stored unencrypted in '/home/<user>/.docker/config.json'.
Configure a credential helper to remove this warning. See
https://docs.docker.com/go/credential-store

Login Succeeded
```

### Step 2: Tag your local image
```bash
docker tag <image-name>:<tag> <harbor-domain>/<project_name>/<image-name>:<tag>
```
After `docker tag`, the image will appear in the listed `docker images` of the local machine.

### Step 3: Push the image to Harbor
```bash
docker push <harbor-domain>/<project_name>/<image-name>:<tag>
```

### Step 4: Verify
In Harbor web UI, refresh the **Repositories** tab. The image should appear with an **artifact** count of 1.




## 4. Pull an Image from Harbor
In the consumer/integrator side:
```bash
docker login <harbor-domain> -u 'robot$<project_name>+<robot_account_name>'
docker pull <harbor-domain>/<project_name>/<image-name>:<tag>
```




## 5. Image Signing (Optional)

By default, pushed images are **NOT signed**, so Harbor shows a red X under the `"Signed"` column.
This is normal for internal/private workflows where Harbor's access control (private project + login) is sufficient.

To enable signing via Docker Content Trust:
```bash
export DOCKER_CONTENT_TRUST=1
docker push <harbor-domain>/<project_name>/<image-name>:<tag>
```
*This generates signing keys on first use. It is only required if an organization enforces supply-chain security policies.*




## 6. Quick Guide

| Action | Command |
|---|---|
| Login | `docker login <harbor-domain> -u 'robot$<project_name>+<robot_account_name>'` |
| Tag image | `docker tag <image_name>:<tag> <harbor-domain>/<project_name>/<image_name>:<tag>` |
| Push image | `docker push <harbor-domain>/<project_name>/<image_name>:<tag>` |
| Pull image | `docker pull <harbor-domain>/<project_name>/<image_name>:<tag>` |
| Logout | `docker logout <harbor-domain>` |
