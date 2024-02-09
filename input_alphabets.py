
basic_functionality_alphabet: list = [
    # File operations
    'create_f0',  # Create a file
    'change_f0',  # Apply changes to a file
    'delete_f0',  # Delete a file

    # Git commands
    'add_f0',
    'commit',  # Make a commit
]

remotes_alphabet: list = [
    # File operations
    'create_f0',  # Create a file
    'change_f0',  # Apply changes to a file
    'delete_f0',  # Delete a file

    # Git commands
    'add_f0',
    'commit',  # Make a commit
    'pull',  # Pull from remote
    'push',  # Push to remote, implies --set-remote for new branches
]

remotes_branching_alphabet: list = [
    # File operations
    'create_f0',  # Create a file
    'change_f0',  # Apply changes to a file
    'delete_f0',  # Delete a file

    # Git commands
    'add_f0',
    'commit',  # Make a commit
    'pull',  # Pull from remote
    'push',  # Push to remote, implies --set-remote for new branches

    # Branching
    'create_branch',  # Create a new branch
    'checkout_branch',  # Checkout the newly created branch
    'checkout_master'  # Checkout master
]

extended_functionality: list = [
    # File operations
    'create_f0',  # Create a file
    'create_f1',
    'change_f0',  # Apply changes to a file
    'change_f1',
    'delete_f0',  # Delete a file
    'delete_f1',

    # Git status checks
    # They do not/should not change state
    # 'branch',  # Reveal the current branch
    # 'untracked',  # Reveal the number of untracked files
    # 'dirty',  # Reveal whether something was added, but not committed yet
    # 'modified',  # Reveal the modified files

    # Git commands
    'add_all',  # Add files
    'add_f0',
    'add_f1',
    'commit',  # Make a commit
    'fetch',  # Fetch from remote
    'pull',  # Pull from remote
    'push',  # Push to remote, implies --set-remote for new branches
    'tag',  # Create a tag
    'create_branch',  # Create a new branch
    'checkout_branch',  # Checkout the newly created branch
    'checkout_master'  # Checkout master
]

# Unused
# Comment these in/out to enable/disable them
complete_input_alphabet: list = [
    # File operations
    'create_f0',  # Create a file
    'create_f1',
    'change_f0',  # Apply changes to a file
    'change_f1',
    'delete_f0',  # Delete a file
    'delete_f1',

    # Git status checks
    # They do not/should not change state
    # 'branch',  # Reveal the current branch
    # 'untracked',  # Reveal the number of untracked files
    # 'dirty',  # Reveal whether something was added, but not committed yet
    # 'modified',  # Reveal the modified files

    # Git commands
    'add_all',  # Add files
    'add_f0',
    'add_f1',
    'commit',  # Make a commit
    'fetch',  # Fetch from remote
    'pull',  # Pull from remote
    'push',  # Push to remote, implies --set-remote for new branches
    'tag',  # Create a tag
    'create_branch',  # Create a new branch
    'checkout_branch',  # Checkout the newly created branch
    'checkout_master'  # Checkout master
]