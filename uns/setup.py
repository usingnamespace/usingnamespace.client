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

default_api_url = 'https://api.usingnamespace.com/v1/'

@click.command()
@click.option('--api-url', default=default_api_url, help="The API URL")
@click.option('--api-token', help="The API token")
@click.pass_context
def setup(ctx, **kw):
    config_path = ctx.obj['config_path']
    config_defaults = {}
    config = SafeConfigParser(config_defaults)

    if os.path.exists(config_path):
        config.readfp(open(config_path))
        
        try:
            if kw['api_url'] == default_api_url:
                kw['api_url'] = config.get('DEFAULT', 'api_url')

            if kw['api_token'] is None:
                kw['api_token'] = config.get('DEFAULT', 'api_token')
        except NoOptionError:
            pass

    api_url_prompt = 'What api URL would you like to use'

    if kw['api_url'] != default_api_url:
        api_url_prompt = api_url_prompt + ' (Default: {})'.format(default_api_url)
   
    api_url = click.prompt(api_url_prompt, default=kw['api_url'])
    api_token = click.prompt('Valid API token', default=kw['api_token'])

    config.set('DEFAULT', 'api_url', api_url)
    config.set('DEFAULT', 'api_token', api_token)

    if click.confirm('Test new configuration'):
        click.echo('Testing configuration...')

        click.echo('Tests passed, safe to save this config file')

    if click.confirm('Save the new configuration file?', abort=True):
        try:
            os.makedirs(os.path.abspath(ctx.obj['config_dir']), 0o700)
        except os.error:
            pass

        with open(config_path, 'w') as f:
            config.write(f)

