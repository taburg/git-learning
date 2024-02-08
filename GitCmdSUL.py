import subprocess

from aalpy.base import SUL

from utils import clean_up, create_file, change_file, delete_file


def execute_git_command(command, cwd):
    try:
        result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True
        else:
            return False
    except Exception:
        return False


class GitCmdSUL(SUL):
    def __init__(self, repo_path, bare_repo_path, verbose=True):
        super().__init__()
        self.repo_path = repo_path
        self.bare_repo_path = bare_repo_path
        self.path_to_bare_repo_from_repo = self.bare_repo_path.replace('tmp', '..')

        # helper variables
        self.filenames: list[str] = ['file0.txt', 'file1.txt']
        self.branches = ['master', 'other_branch']
        self.tag_number = 0
        self.commit_number = 0

        self.verbose = verbose

    def pre(self):
        # Initialize a bare repository as a local remote
        subprocess.run(['git', 'init', '--bare', self.bare_repo_path], stdout=subprocess.DEVNULL)
        # Initialize a new repository if it doesn't exist
        subprocess.run(['git', 'init', self.repo_path], stdout=subprocess.DEVNULL)
        # Add the remote
        subprocess.run(['git', 'remote', 'add', 'origin', self.path_to_bare_repo_from_repo], cwd=self.repo_path)

    def post(self):
        self.tag_number = 0
        self.commit_number = 0
        clean_up(None, self.repo_path, self.bare_repo_path)

    def query(self, word: tuple) -> list:
        outputs = super(GitCmdSUL, self).query(word)
        if self.verbose:
            print(f'Current query and outputs: {list(zip(word, outputs))}')
        return outputs

    def step(self, letter):
        file_command_status = None
        # File operations
        if letter == 'create_f0':
            file_command_status = create_file(self.repo_path + '/' + self.filenames[0])
        elif letter == 'create_f1':
            file_command_status = create_file(self.repo_path + '/' + self.filenames[1])
        elif letter == 'change_f0':
            file_command_status = change_file(self.repo_path + '/' + self.filenames[0])
        elif letter == 'change_f1':
            file_command_status = change_file(self.repo_path + '/' + self.filenames[1])
        elif letter == 'delete_f0':
            file_command_status = delete_file(self.repo_path + '/' + self.filenames[0])
        elif letter == 'delete_f1':
            file_command_status = delete_file(self.repo_path + '/' + self.filenames[1])

        if file_command_status is not None:
            return 'PASS' if file_command_status else 'FAIL'

        # Git commands
        git_command = None
        if letter == 'add_all':
            git_command = ['git', 'add', '.']
        elif letter == 'add_f0':
            git_command = ['git', 'add', self.filenames[0]]
        elif letter == 'add_f1':
            git_command = ['git', 'add', self.filenames[1]]
        elif letter == 'commit':
            git_command = ['git', 'commit', '-m', f'Commit Number: {self.commit_number}']
            self.commit_number += 1
        elif letter == 'tag':
            git_command = ['git', 'tag', '-a', f'v.{self.tag_number}', '-m', 'Tag Message']
            self.tag_number += 1
        elif letter == 'fetch':
            git_command = ['git', 'fetch', 'all']
        elif letter == 'pull':
            git_command = ['git', 'pull', ]
        elif letter == 'push':
            git_command = ['git', 'push', '-u', 'origin', 'HEAD']
        elif letter == 'create_branch':
            git_command = ['git', 'branch', self.branches[1]]
        elif letter == 'checkout_branch':
            git_command = ['git', 'checkout', self.branches[1]]
        elif letter == 'checkout_master':
            git_command = ['git', 'checkout', self.branches[0]]
        else:
            raise ValueError(f'This letter is not part of the alphabet! Letter: {letter}')

        git_command_status = execute_git_command(git_command, cwd=self.repo_path)
        return 'PASS' if git_command_status else 'FAIL'
