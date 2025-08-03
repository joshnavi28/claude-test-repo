import subprocess

def main(commit_message: str):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        return f"Changes pushed with commit message: '{commit_message}'"
    except subprocess.CalledProcessError as e:
        return f"Git command failed: {e}"
