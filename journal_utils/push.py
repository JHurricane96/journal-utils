import git


def push(args, cfg):
    """
    Use git to push all new entries to the remote repository.
    """
    repo = git.Repo(cfg["journal_path"])
    repo.git.add(".")
    repo.git.commit("-m", "Updates")
    repo.git.push()
    print("Journal updated and pushed to remote repository.")
