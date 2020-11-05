import git_autoupdate

print("startup.py erne pyrevit auto updater..")

git_autoupdate.pull_repo("pyrevit")
git_autoupdate.pull_repo("pyRevit_erne")
