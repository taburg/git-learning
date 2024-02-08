import subprocess

# Paths to the repositories
from utils import clean_up

repo_path: str = 'tmp/repo'
bare_repo_path: str = 'tmp/barerepo.git'

clean_up(None, repo_path, bare_repo_path)

# Initialize a new repository if it doesn't exist
subprocess.run(["git", "init", repo_path])

# Initialize a bare repository as a local remote
subprocess.run(["git", "init", "--bare", bare_repo_path])

# Add the remote
subprocess.run(["git", "remote", "add", "master", bare_repo_path])


# Add a file to the repository
file_path = "example.txt"
with open(f"{repo_path}/{file_path}", "w") as f:
    f.write("Hello, world!")

# Add the file to the staging area
subprocess.run(["git", "add", file_path])

# Commit the changes
subprocess.run(["git", "commit", "-m", "Initial commit"])

# Push the changes to the local remote
subprocess.run(["git", "push", "-u", "origin", "master"],)