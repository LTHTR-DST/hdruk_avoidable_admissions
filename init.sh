# Project initialisation Script.
# This runs a series of commands to setup the entire project environment
# Depends on a version of anaconda or miniconda installed with mamba and pip on PATH
# If using this on Windows, run in an Anaconda Powershell Prompt

mamba env update -f ./environment.yml --prune
mamba activate hdruk_aa
