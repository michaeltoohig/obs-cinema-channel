# cinema-playout

Cinema channel playout with OBS

Strictly a playout server via OBS taking advantage of some of OBS built in dynamic features such as updating text elements from the contents of text files.
This project has other components that handle video transcoding, data fetching and playlist building which is not seen here.

## Setup

Be sure to configure the `.env` file before using and that the library paths are correct and if they are network storage paths then they must be attached also.

Before starting you will need to run the `cinema-playout library copy` command to copy media content from the remote storage to the local storage as defined in `.env`.

Once the media is copied locally you can begin playout to the OBS instance via `cinema-playout obs run` which handles the OBS instance as well as schedules a daily task to copy library content from remote to local storage so you don't have to setup a recurring task manually.

## Usage

Activate the local environment (gives access to installed packages required for this tool to work)

    poetry shell

For help, run:

    poetry run cinema-playout --help

For crontab usage example:

    */5 * * * cd /path/to/cinema-playout && . /path/to/pypoetry/virtualenv/bin/activate && cinema-playout --strict [COMMAND] >> logs/`date +\%Y-\%m-\%d`.log 2>&1
    0 0 * * * /usr/bin/find /path/to/cinema-playout/logs -name "*.log" -type f -mtime +7 -exec rm -f {} \;

Note the use of the `--strict` option for production use so logs are rendered to JSON and without color.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd cinema-playout
    poetry shell
    poetry install

To run the tests:

    pytest

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [michaeltoohig/click-cli-boilerplate](https://github.com/michaeltoohig/click-cli-boilerplate) project template.
