import os
import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Git command failed: {cmd}\nstdout: {result.stdout}\nstderr: {result.stderr}")
    return result.stdout

def commit_changes(commit_message):
    # Check if there are changes to commit
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout.strip() == "":
        # No changes detected
        return "No changes to commit"
    else:
        # Commit the changes
        run_cmd(["git", "commit", "-m", commit_message])
        return "Changes committed"

def main(repo_url: str, commit_message: str = "Update from Claude GitOps", local_path: str = "."):
    try:
        os.chdir(local_path)

        if not os.path.exists(os.path.join(local_path, ".git")):
            run_cmd(["git", "init"])
            run_cmd(["git", "remote", "add", "origin", repo_url])
        else:
            remotes = run_cmd(["git", "remote"])
            if "origin" not in remotes:
                run_cmd(["git", "remote", "add", "origin", repo_url])

        run_cmd(["git", "add", "."])
        commit_message_status = commit_changes(commit_message)
        run_cmd(["git", "push", "-u", "origin", "main"])

        return {
            "status": "success",
            "message": f"Code pushed to {repo_url} successfully. {commit_message_status}"
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
