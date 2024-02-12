![Learned Git Model](https://github.com/taburg/git-learning/blob/main/models/learned_model.PNG)

# git-learning
Learning a model of Git using AALpy.

## Setup
This section describes how to setup Git, in order to be learnable with AALpy. Instead of using a remote connection/repository, such as on GitHub or GitLab, we will create a bare repository locally.
Experiments are performed locally for efficienty, and would need to be slightly adapted to learn directly with the remote git server.

Prerequisites: installation of Git and following Python dependencies (AALpy and GitPython):
```python
pip install -r requirements.txt
```

### Usage

`python3 git_learning.py` creates two repos (one bare, one normal) in the `/tmp` directory.

That script can be parametarized to learn certain configuration of Git, and learned model will be displayed and saved to a file.

You can either learn models of GitCLI or GitPython, with or without `--allow-empty` flag, and with any input alphabet found in appropriate file.

#### Experiment runner

To execute all experiments, run:
```python
python experiment_runner.py
```

All learned models and experiment statistics can be found in the models/ folder. 

### Differences between learned models

Following are some of the found differences with the interface_comparison script:
```
Inputs        : ('create_f0', 'add_f0', 'delete_f0', 'add_f0')
CLI           : ['PASS', 'PASS', 'PASS', 'PASS']
GitPython     : ['PASS', 'PASS', 'PASS', 'FAIL']

Inputs        : ('checkout_master')
CLI           : ['FAIL']
GitPython     :  ['PASS']

Inputs    : ('create_f0', 'add_f0', 'delete_f0', 'commit', 'create_branch', 'checkout_branch', 'delete_f0')
CLI       : ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'FAIL']
GitPython :['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS']

Inputs    : ('create_f0', 'commit', 'add_f0', 'create_branch', 'commit', 'checkout_branch', 'create_f0', 'checkout_master')
CLI       : ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'FAIL']
GitPython : ['PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS', 'PASS']
```