# git-learning
Learning a model of Git using AALpy.

## Setup
This section describes how to setup Git, in order to be learnable with AALpy. Instead of using a remote connection/repository, such as on GitHub or GitLab, we will create a bare repository locally.
Experiments are performed locally for efficienty, and would need to be slighlty adapted to learn directly with the remote git server.

Prerequisites: installation of Git and following Python dependencies:
```python
pip install aalpy gitpython
```

### Bare Repository
First, the bare repository has to be created.
```
git init --bare /path/to/bare.git
```

### Working Repository
There are two possibilities to connect the working repository with the bare repository. Either one will work fine. They both have to be typed in the directory where the working repository should be.
```
git init
git remote add origin /path/to/bare.git
```
```
git clone /path/to/bare.git
```

### Usage

`python3 git_learning.py` creates two repos (one bare, one normal) in the `/tmp` directory.

Furthermore, the files `git-model.pdf` and `git-model.log` containing the model's graph and a textual representation will be created.


### Useful Links
[Blog entry by Jon Saints](https://www.saintsjd.com/2011/01/what-is-a-bare-git-repository/)  
[StackOverflow Post](https://stackoverflow.com/questions/10603671/how-to-add-a-local-repo-and-treat-it-as-a-remote-repo)
