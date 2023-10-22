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
