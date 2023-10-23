# git-learning
Learning a model of Git using AALpy.

## Setup
This section describes how to setup Git, in order to be learnable with AALpy. Instead of using a proper remote repository, such as on GitHub or GitLab, we will create a so-called bare repository locally. There is no need for a remote connection, it would only slow things down.

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

### Links
[Blog entry by Jon Saints](https://www.saintsjd.com/2011/01/what-is-a-bare-git-repository/)  
[StackOverflow Post](https://stackoverflow.com/questions/10603671/how-to-add-a-local-repo-and-treat-it-as-a-remote-repo)

### TODO
- SUL implementation
Desired functions:
- Init (reset) - Total clean
- Add
- Commit
- Push
- Pull
- Tag
- Stash
- Branching
- Fetch
- Reset
- Restore
- Maybe some more interesting ones

- Files operations (change/delete/add/...)

Use subsets of learning the alphabet, and/or everything.

How to deal with files:
- Have 2 .txt files and some method to change them, with completely random stuff in them
- For example: function add() can map to : add_all, add_file_1, add_file_2

General:
- Use RandomWord and/or RandomWEqOracle
- run_Lstar or run_KV

Future:
- Once it is set up, try with remote repo
- Same stuff with SVN
- Write a function that compares models with known differences (push == commit, push)
