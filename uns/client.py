import os.path

try:
    from ConfigParser import (
            SafeConfigParser,
            NoOptionError,
            )
except ImportError:
    # Name changed in Python 3.x to configparser
    from configparser import (
            SafeConfigParser,
            NoOptionError,
            )

import click

from .setup import setup
from .vendor.appdirs import AppDirs

dirs = AppDirs("usingnamespace.client", "Using Namespace", version="0.0")

config_dir = dirs.user_data_dir

@click.group()
@click.option('--config-dir', default=config_dir, help='Configuration file location', type=click.Path())
@click.pass_context
def cli(ctx, **kw):
    config_path = os.path.join(kw['config_dir'], 'config.ini')
    config_defaults = {}
    config = SafeConfigParser(config_defaults)

    if os.path.exists(config_path):
        config.readfp(open(config_path))

    ctx.obj = kw
    ctx.obj['config_path'] = config_path
    ctx.obj['config'] = config

cli.add_command(setup)

def main():
    """This starts the client...
    """

    cli(obj={})
