
# Manage Apps

this is a simple script to add, delete, check, list and launch from a configuration script
`apps.csv` this was done for linux, if you want to work on windows,  you have to do some
adjustments to the paths.

The default position of this directory should be in `$HOME/.local/share/apps`.

## Getting started

- firstly clone this repository: `git clone https://github.com/fractal27/m-apps ~/.local/share/apps`
- install the script, you can install it locally and globally;
```sh
$ #sudo make global-install
$ make local-install
Successfully installed `m-apps` locally into `~/.local/bin`
```
- modify the apps, you first should remove all apps in the configuration.
