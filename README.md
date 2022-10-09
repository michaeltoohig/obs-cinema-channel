# cinema-playout

Cinema channel playout with OBS

Strictly a playout server via OBS taking advantage of some of OBS built in dynamic features such as updating text elements from the contents of text files.
This project has other components that handle video transcoding, data fetching and playlist building which is not seen here.

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
