QIIME-Galaxy
============

A Python application to automatically integrate QIIME on Galaxy.

## Getting started

To run _QIIME-Galaxy_, you will first need to get [QIIME](http://qiime.org/) and [Galaxy](http://wiki.galaxyproject.org/) successfully installed in your machine. Refer to their pages for installation details.

__Note:__ _QIIME-Galaxy_ requires Python 2.7.3 to work correctly, the same version as QIIME.

## Installation procedure

__Note:__ The commands in this page assume you are in your home directory. You can change the installation paths as you like, but you will need to modify the commands we provide to use the new paths.

To install _QIIME-Galaxy_ in your system, you can follow these instructions:

1. Get the _QIIME-Galaxy_ code by cloning the repository:

        git clone git://github.com/qiime/qiime-galaxy.git

Alternatively, you can download the source code in a zipped archive using this [link](https://github.com/qiime/qiime-galaxy/archive/master.zip).

2. Add the ```scripts``` folder to your path and the ```lib``` folder to your python path.

        echo "export PATH=$HOME/qiime-galaxy/scripts:$PATH" >> $HOME/.bashrc
        echo "export PYTHONPATH=$HOME/qiime-galaxy/lib:$PYTHONPATH" >> $HOME/.bashrc
        source $HOME/.bashrc

## Usage examples

### Integrate QIIME on a dedicated Galaxy instance

To integrate QIIME on a Galaxy instance that will only host the QIIME tools, run the following command. This command assumes that the Galaxy installation directory ```galaxy-dist``` and the QIIME installation directory ```qiime``` are located in your home folder. Change these paths in order to meet your system configuration.

    integrate_on_galaxy.py -i $HOME/qiime/scripts -g $HOME/galaxy-dist -c $HOME/qiime-galaxy/config_file.txt

### Integrate QIIME on a Galaxy instance with other tools

To integrate QIIME on a Galaxy instance that hosts other tools, run the following command. This command will allow to maintain the current Galaxy tools configuration while adding QIIME as a new available tool.

    integrate_on_galaxy.py -i $HOME/qiime/scripts -g $HOME/galaxy-dist -c $HOME/qiime-galaxy/config_file.txt --update_tool_conf