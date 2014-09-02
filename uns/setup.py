import os.path

import requests

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
@click.option('--interactive/--no-interactive', default=True, help="Run this script interactively")
@click.option('--test/--no-test', default=True, help="Test the new configuration (non-interactive only)")
@click.option('--save/--no-save', default=False, help="Save the new configuration (non-interactive only)")
@click.option('--api-url', default=default_api_url, help="The API URL")
@click.option('--api-ticket', help="The API ticket")
@click.pass_context
def setup(ctx, **kw):
    config_path = ctx.obj['config_path']
    config_defaults = {}
    config = SafeConfigParser(config_defaults)

    interactive = kw['interactive']
    test = kw['test']
    save = kw['save']

    if os.path.exists(config_path):
        config.readfp(open(config_path))
        
        try:
            if kw['api_url'] == default_api_url and interactive:
                kw['api_url'] = config.get('DEFAULT', 'api_url')

            if kw['api_ticket'] is None:
                kw['api_ticket'] = config.get('DEFAULT', 'api_ticket')
        except NoOptionError:
            pass

    api_url_prompt = 'What API URL would you like to use'

    if kw['api_url'] != default_api_url:
        api_url_prompt = api_url_prompt + ' (Default: {})'.format(default_api_url)
    
    api_url = kw['api_url'] if not interactive else click.prompt(api_url_prompt, default=kw['api_url'])
    api_ticket = kw['api_ticket'] if not interactive else click.prompt('API ticket for your account', default=kw['api_ticket'])

    if not interactive and api_ticket is None:
        click.echo('Unable to continue without API ticket')
        exit(-1)

    config.set('DEFAULT', 'api_url', api_url)
    config.set('DEFAULT', 'api_ticket', api_ticket)

    if (not interactive and test) or (interactive and click.confirm('Test new configuration')):
        click.echo('Testing configuration...')

        headers = {
                'x-api-ticket': api_ticket,
                }

        try:
            r = requests.get(api_url, headers=headers)

            if r.status_code != 200:
                click.echo('API ticket or API url are wrong. Do not save file.')
                save = False
            else:
                click.echo('Everything checks out.')
                if interactive:
                    save = True

        except:
            click.echo('Provided API URL is invalid.')
            save = False

    if (not interactive and save) or (interactive and click.confirm('Save the new configuration file?', abort=True, default=save)):
        try:
            os.makedirs(os.path.abspath(ctx.obj['config_dir']), 0o700)
        except os.error:
            pass

        with open(config_path, 'w') as f:
            config.write(f)

