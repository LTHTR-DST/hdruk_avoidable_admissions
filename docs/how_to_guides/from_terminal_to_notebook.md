## Start Point

By this point in the tutorial you should have a terminal up on your screen which looks something like this:

![Terminal](https://github.com/MattStammers/hdruk_avoidable_admissions_collaboration_docs/blob/southampton/docs/images/terminal.JPG?raw=true)

If so you are good to move to the next stage.

## Get to Root Folder

You now need to navigate to the root folder where the collaboration repository is sitting. to get there type

- `cd {PATH_TO_REPOSITORY}`

This should work in both Windows and Linux.

## Installing Mamba

To install mamba you need to call:

`conda install mamba -n base -c conda-forge`

In the base directory of your minicondas installation. This is the best and most reliable way to install it. Seems like extra work installing all these things (and it is) but the end result will be worthwhile in terms of having a robust environment to work in. You can install it with pip but conda-forge is a better option if available to you.

Important: :no_entry: This has typically been the slowest step when I have run it so be patient while it is running. It only needs to be done once.

## Creating The Virtual Environment

Now you are in the root folder with minicondas activated you are ready to create the virtual environment. A virtual environment is just a seperate computing environment which is controlled and won't interfere with the base or other environments. They are disposable and indispensible when programming as they allow you to customise things for particular projects and avoid dependencies conflits.

To set it up do the following:

 Execute `./init.bat` - or .sh if in linux

This will take a short while to run but when it is finished you will have a fully functional python environment to run all the commands to come. This is called hdruk_aa presently but you can rename it in the yaml file if you want to. The only bit you need to change to create a new but similar environment is this line in the `environment.yaml` file. (YAML files are typically just configuration files.)

change the line `name: hdruk_aa` to create a different environment with a different name. Only edit the rest if you know what you are doing or you might break the environment setup but it is there for those that need to change it.

When I was experimenting with this I tried various different environments and python versions tagging '_py3_11' etc onto the end to try them out. At the end you can delete all the ones you don't want. However, if you are new try to just create one and work with that to reduce complexity.

## Activating the environment

Activate the environment with `conda activate hdruk_aa` or whatever you have called it. As long as you are in base this should work.

## Launching the Notebook

You are now ready to launch the notebook or lab. Notebooks are simpler but juptyer-lab has more functionality. Feel free to experiment with whatever you prefer.

- To launch a simple notebook call: `python -m notebook`

- Or to start JupyterLab call `jupyter-lab`

These should open up a browser window in your root directory and you are then ready to start coding.
