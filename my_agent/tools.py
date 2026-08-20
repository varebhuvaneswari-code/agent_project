
import os
import shutil
import subprocess

def calculate_average(marks: list[float]) -> float:
    """Calculate the average of a list of marks."""
    if not marks:
        return 0.0
    return sum(marks) / len(marks)


def create_file(filename: str, content: str) -> str:
    """Creates a file with a given filename and writes the provided content into it.

    Args:
        filename: The name or path of the file to create (e.g., 'notes.txt').
        content: The text content to write inside the file.
    
    Returns:
        A confirmation or error message.
    """
    try:
        # Create missing folders if the path includes directories
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
            
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Success: File '{filename}' was created."
    except Exception as e:
        return f"Error: Could not create file '{filename}'. Details: {str(e)}"

def generate_linkedin_post(topic: str, audience: str = "professionals", tone: str = "engaging") -> str:
    """Generates structured content suitable for a LinkedIn post.

    Args:
        topic: The primary subject or subject matter of the post.
        audience: The target audience (e.g., 'software engineers', 'recruiters', 'entrepreneurs').
        tone: The desired style/tone (e.g., 'thought leadership', 'storytelling', 'actionable advice').

    Returns:
        A structured string containing the proposed LinkedIn post draft.
    """
    # This function acts as a template or generator logic tool.
    # In an agent setup, an LLM can either call this to draft content or use it as a standard function.
    post_template = (
        f"🚀 **LinkedIn Post Draft**\n"
        f"**Target Audience:** {audience}\n"
        f"**Tone:** {tone}\n\n"
        f"--- Draft Start ---\n\n"
        f"Here's something every {audience} should keep in mind about {topic}:\n\n"
        f"1. Key Insight: Focus on the core problem and solution.\n"
        f"2. Practical Tip: Share a clear, actionable takeaway.\n\n"
        f"What are your thoughts on this? Let me know below! 👇\n\n"
        f"#Networking #{topic.replace(' ', '')} #CareerGrowth"
    )
    return post_template


def _find_git_executable() -> str:
    """Locates the git executable on the system if available."""
    git_path = shutil.which("git")
    if git_path:
        return git_path

    common_paths = [
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files\Git\bin\git.exe",
        r"C:\Program Files (x86)\Git\cmd\git.exe",
        r"C:\Program Files (x86)\Git\bin\git.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\cmd\git.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\bin\git.exe"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Programs\Git\cmd\git.exe"),
        os.path.expandvars(r"%ProgramW6432%\Git\cmd\git.exe"),
        r"C:\Git\cmd\git.exe",
        r"C:\tools\git\cmd\git.exe",
    ]
    for path in common_paths:
        if os.path.isfile(path):
            return path

    return ""


def push_to_github(
    repo_url: str = "",
    commit_message: str = "Update agent codebase",
    branch: str = "main",
    token: str = "",
) -> str:
    """Initializes git (if needed), stages files, commits, and pushes the agent project to GitHub.

    Args:
        repo_url: The GitHub repository URL (e.g. 'https://github.com/username/my-agent.git' or 'username/my-agent').
                  If omitted, will attempt to push to the already configured 'origin' remote.
        commit_message: Commit message describing the changes.
        branch: The Git branch to push to (defaults to 'main').
        token: Optional GitHub Personal Access Token for HTTPS authentication. Can also be set via GITHUB_TOKEN environment variable.

    Returns:
        A status message indicating success or details of any error encountered.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)

        # 1. Ensure .gitignore exists to prevent leaking secrets (.env) or virtual environment
        gitignore_path = os.path.join(project_root, ".gitignore")
        if not os.path.exists(gitignore_path):
            default_gitignore = (
                "# Environment variables & secrets\n.env\n\n"
                "# Virtual environments\n.venv/\nenv/\nvenv/\n\n"
                "# Python cache\n__pycache__/\n*.py[cod]\n\n"
                "# IDEs & Tooling\n.gemini/\n.vscode/\n.idea/\n"
            )
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write(default_gitignore)

        # 2. Clean and format the repository URL
        if not repo_url:
            repo_url = "https://github.com/varebhuvaneswari-code/agent_project.git"

        cleaned_url = repo_url.strip()
        if not cleaned_url.startswith("http://") and not cleaned_url.startswith("https://") and not cleaned_url.startswith("git@"):
            cleaned_url = f"https://github.com/{cleaned_url}.git"
        elif not cleaned_url.endswith(".git") and "github.com" in cleaned_url:
            cleaned_url = f"{cleaned_url}.git"

        auth_token = token.strip() or os.getenv("GITHUB_TOKEN", "").strip()

        # Build authenticated URL if token is present
        if auth_token and cleaned_url.startswith("https://github.com/"):
            target_push_url = cleaned_url.replace("https://github.com/", f"https://{auth_token}@github.com/")
        else:
            target_push_url = cleaned_url

        # 3. If token is provided, prioritize direct GitHub REST API sync for 100% reliable HTTPS push
        if auth_token and "github.com" in cleaned_url:
            # Extract owner and repo from URL (e.g. https://github.com/owner/repo.git)
            parts = cleaned_url.rstrip("/").removesuffix(".git").split("/")
            if len(parts) >= 2:
                owner, repo_name = parts[-2], parts[-1]
                return _push_via_github_api(
                    owner=owner,
                    repo=repo_name,
                    token=auth_token,
                    project_root=project_root,
                    branch=branch,
                    commit_message=commit_message,
                )

        # Check if native git CLI is available
        git_bin = _find_git_executable()

        if git_bin:
            def run_git(args: list[str]) -> tuple[int, str, str]:
                res = subprocess.run(
                    [git_bin] + args,
                    cwd=project_root,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                return res.returncode, res.stdout.strip(), res.stderr.strip()

            git_dir = os.path.join(project_root, ".git")
            if not os.path.exists(git_dir):
                code, _, err = run_git(["init", "-b", branch])
                if code != 0:
                    run_git(["init"])
                    run_git(["branch", "-M", branch])

            # Ensure user info
            code, user_name, _ = run_git(["config", "user.name"])
            if not user_name:
                run_git(["config", "user.name", "Agent Assistant"])
            code, user_email, _ = run_git(["config", "user.email"])
            if not user_email:
                run_git(["config", "user.email", "agent@assistant.local"])

            # Set remote
            code, _, _ = run_git(["remote", "get-url", "origin"])
            if code == 0:
                run_git(["remote", "set-url", "origin", target_push_url])
            else:
                run_git(["remote", "add", "origin", target_push_url])

            run_git(["branch", "-M", branch])
            run_git(["add", "-A"])

            code, status_out, _ = run_git(["status", "--porcelain"])
            if status_out:
                run_git(["commit", "-m", commit_message])

            code, push_out, push_err = run_git(["push", "-u", "origin", branch])
            if code != 0:
                safe_err = push_err.replace(auth_token, "********") if auth_token else push_err
                if "Authentication failed" in safe_err or "could not read Username" in safe_err or "Invalid username or password" in safe_err:
                    return (
                        f"Authentication required: GitHub requires a Personal Access Token to push.\n"
                        f"Please provide your GitHub Personal Access Token (or set GITHUB_TOKEN in your environment)."
                    )
                return f"Error pushing with git CLI to branch '{branch}': {safe_err}"

            return f"Success: Pushed agent project to GitHub ({cleaned_url}) on branch '{branch}'."

        # Fallback to pure Python dulwich git implementation
        try:
            import dulwich.porcelain as porcelain
            from dulwich.repo import Repo

            git_dir = os.path.join(project_root, ".git")
            if not os.path.exists(git_dir):
                repo = porcelain.init(project_root)
            else:
                repo = Repo(project_root)

            # Stage unignored files
            tracked_items = [".gitignore", "README.md", "requirements.txt", "buna", "my_agent"]
            valid_paths = [p for p in tracked_items if os.path.exists(os.path.join(project_root, p))]
            porcelain.add(project_root, paths=valid_paths)

            # Commit
            try:
                porcelain.commit(
                    project_root,
                    message=commit_message.encode("utf-8"),
                    author=b"Agent Assistant <agent@assistant.local>",
                    committer=b"Agent Assistant <agent@assistant.local>",
                )
            except Exception:
                pass  # Nothing new to commit

            # Push
            refspec = f"refs/heads/master:refs/heads/{branch}".encode("utf-8")
            porcelain.push(
                project_root,
                target_push_url,
                refspecs=refspec,
            )
            return f"Success: Pushed agent project to GitHub repository ({cleaned_url}) on branch '{branch}'."

        except Exception as dulwich_err:
            err_str = str(dulwich_err)
            if "HTTPUnauthorized" in err_str or "No valid credentials" in err_str:
                return (
                    f"Authentication required: GitHub requires a Personal Access Token (PAT) to push.\n\n"
                    f"To push to your repo ({cleaned_url}):\n"
                    f"1. Generate a token on GitHub: https://github.com/settings/tokens (classic -> check 'repo' scope)\n"
                    f"2. Provide the token here (e.g. push_to_github(token='ghp_...')) or set GITHUB_TOKEN in your .env"
                )
            return f"Error pushing to GitHub: {err_str}"

    except Exception as e:
        return f"Unexpected error while pushing to GitHub: {str(e)}"


def _push_via_github_api(
    owner: str,
    repo: str,
    token: str,
    project_root: str,
    branch: str = "main",
    commit_message: str = "Update agent codebase",
) -> str:
    """Directly synchronizes and commits repository files to GitHub using the REST API."""
    import base64
    import requests

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Agent-Assistant",
    }

    # 1. Verify credentials with GitHub
    user_res = requests.get("https://api.github.com/user", headers=headers)
    if user_res.status_code == 401:
        return (
            "Authentication Error: GitHub returned '401 Bad credentials'.\n\n"
            "Please verify that the Personal Access Token is active and was copied completely from:\n"
            "https://github.com/settings/tokens (Tokens classic -> check 'repo' scope)."
        )
    elif user_res.status_code != 200:
        return f"Authentication Error: {user_res.status_code} {user_res.text}"

    # 2. Check repository access
    repo_res = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)
    if repo_res.status_code == 404:
        return f"Error: Repository '{owner}/{repo}' was not found. Please ensure the repository is created under your GitHub account."
    elif repo_res.status_code != 200:
        return f"Error accessing repository '{owner}/{repo}': {repo_res.status_code} {repo_res.text}"

    # Collect project files to upload
    ignore_names = {".env", ".venv", ".git", ".gemini", "__pycache__", ".idea", ".vscode"}
    files_to_upload = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in ignore_names]
        for f in files:
            if f in ignore_names or f.endswith(".pyc"):
                continue
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, project_root).replace("\\", "/")
            files_to_upload.append((rel_path, full_path))

    # 3. Create blobs for each file
    tree_items = []
    for rel_path, full_path in files_to_upload:
        with open(full_path, "rb") as fp:
            content_bytes = fp.read()
        b64_content = base64.b64encode(content_bytes).decode("utf-8")
        blob_res = requests.post(
            f"https://api.github.com/repos/{owner}/{repo}/git/blobs",
            headers=headers,
            json={"content": b64_content, "encoding": "base64"},
        )
        if blob_res.status_code != 201:
            return f"Error uploading '{rel_path}': {blob_res.text}"
        blob_sha = blob_res.json()["sha"]
        tree_items.append({
            "path": rel_path,
            "mode": "100644",
            "type": "blob",
            "sha": blob_sha,
        })

    # 4. Check existing branch ref
    ref_res = requests.get(f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{branch}", headers=headers)
    parent_commits = []
    base_tree = None
    if ref_res.status_code == 200:
        parent_commit_sha = ref_res.json()["object"]["sha"]
        parent_commits = [parent_commit_sha]
        commit_info = requests.get(f"https://api.github.com/repos/{owner}/{repo}/git/commits/{parent_commit_sha}", headers=headers)
        if commit_info.status_code == 200:
            base_tree = commit_info.json()["tree"]["sha"]

    # 5. Create new Git tree
    tree_payload = {"tree": tree_items}
    if base_tree:
        tree_payload["base_tree"] = base_tree
    tree_res = requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/git/trees",
        headers=headers,
        json=tree_payload,
    )
    if tree_res.status_code != 201:
        return f"Error creating Git tree on GitHub: {tree_res.text}"
    new_tree_sha = tree_res.json()["sha"]

    # 6. Create Git commit
    commit_payload = {
        "message": commit_message,
        "tree": new_tree_sha,
        "parents": parent_commits,
    }
    commit_res = requests.post(
        f"https://api.github.com/repos/{owner}/{repo}/git/commits",
        headers=headers,
        json=commit_payload,
    )
    if commit_res.status_code != 201:
        return f"Error creating Git commit on GitHub: {commit_res.text}"
    new_commit_sha = commit_res.json()["sha"]

    # 7. Update branch reference (or create branch if initial commit)
    if parent_commits:
        update_res = requests.patch(
            f"https://api.github.com/repos/{owner}/{repo}/git/refs/heads/{branch}",
            headers=headers,
            json={"sha": new_commit_sha, "force": True},
        )
    else:
        update_res = requests.post(
            f"https://api.github.com/repos/{owner}/{repo}/git/refs",
            headers=headers,
            json={"ref": f"refs/heads/{branch}", "sha": new_commit_sha},
        )

    if update_res.status_code not in (200, 201):
        return f"Error updating branch '{branch}' on GitHub: {update_res.text}"

    return f"Success: Successfully pushed agent project to https://github.com/{owner}/{repo} (branch '{branch}')."