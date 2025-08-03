from skills import create_repo, push_code

def main(repo_name: str, description: str = "Repo created by Claude GitOps Assistant", private: bool = True, local_path: str = "."):
    # Step 1: Create the repo
    create_response = create_repo.main(repo_name=repo_name, private=private, description=description)

    if create_response.get("status") != "success":
        return {"status": "error", "message": "Repo creation failed", "details": create_response}

    repo_url = create_response.get("repo_url")

    # Step 2: Push code
    push_response = push_code.main(repo_url=repo_url, local_path=local_path, commit_message="Initial commit from Claude GitOps Assistant")

    if push_response.get("status") != "success":
        return {"status": "error", "message": "Code push failed", "details": push_response}

    return {"status": "success", "message": "Repo created and code pushed successfully!", "repo_url": repo_url}
