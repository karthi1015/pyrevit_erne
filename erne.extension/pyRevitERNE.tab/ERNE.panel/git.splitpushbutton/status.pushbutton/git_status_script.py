import os
import clr
clr.AddReference("LibGit2Sharp")
from LibGit2Sharp import Repository, Commands
from LibGit2Sharp import StatusOptions


def status_repo(name):
    print("INFO: git status: {}".format(name))
    target_path = os.path.join(PROG_DATA, name)
    repo = Repository(str(target_path))
    status = repo.RetrieveStatus(StatusOptions())
    if status.IsDirty:
        print("repo not clean - please contact your pyRevit admin!")
        return
    print("repo is clean: {}".format(not status.IsDirty))


PROG_DATA = "C:\\ProgramData"
status_repo("pyRevit_erne")
