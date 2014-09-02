import os.path

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
    if os.path.exists(config_path):
        print("Config file exists. Grabbing values.")
    ctx.obj = kw
    ctx.obj['config_path'] = config_path

cli.add_command(setup)

def main():
    """This starts the client...
    """

    cli(obj={})
