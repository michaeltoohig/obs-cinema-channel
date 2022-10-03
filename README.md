# cinema-playout


[![pypi](https://img.shields.io/pypi/v/cinema-playout.svg)](https://pypi.org/project/cinema-playout/)
[![python](https://img.shields.io/pypi/pyversions/cinema-playout.svg)](https://pypi.org/project/cinema-playout/)
[![Build Status](https://github.com/michaeltoohig/cinema-playout/actions/workflows/dev.yml/badge.svg)](https://github.com/michaeltoohig/cinema-playout/actions/workflows/dev.yml)
[![codecov](https://codecov.io/gh/michaeltoohig/cinema-playout/branch/main/graphs/badge.svg)](https://codecov.io/github/michaeltoohig/cinema-playout)



Cinema channel playout with OBS


* Documentation: <https://michaeltoohig.github.io/cinema-playout>
* GitHub: <https://github.com/michaeltoohig/cinema-playout>
* PyPI: <https://pypi.org/project/cinema-playout/>
* Free software: MIT


## Features

* TODO

## TODO

* Use VLC Media Source to play a feature - websockets can set start time for when we are restarting the server
* Create filler / standby scene for with feature ends until next feature begins

NOTE: using OBS-websockets protocol version 4.9. Version 5.0 is not fully developed and is missing key functionality but should be used in the future.

https://github.com/obsproject/obs-websocket/blob/4.x-compat/docs/generated/protocol.md

## Usage

Activate the local environment (gives access to installed packages required for this tool to work)

    poetry shell

For help, run:

    poetry run cinema-playout --help

For crontab usage example:

    */5 * * * cd /path/to/cinema-playout && . /path/to/pypoetry/virtualenv/bin/activate && cinema-playout [COMMAND] >> logs/`date +\%Y-\%m-\%d`.log 2>&1
    0 0 * * * /usr/bin/find /path/to/cinema-playout/logs -name "*.log" -type f -mtime +7 -exec rm -f {} \;

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd cinema-playout
    poetry shell
    poetry install

To run the tests:

    pytest

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [michaeltoohig/click-cli-boilerplate](https://github.com/michaeltoohig/click-cli-boilerplate) project template.
