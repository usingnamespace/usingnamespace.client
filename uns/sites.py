import requests
import click

@click.group()
@click.pass_context
def sites(ctx):
    pass

@click.command(name='list')
@click.pass_context
def sites_list(ctx):
    click.echo('Listing all sites...')

    try:
        import requests

        headers = {
                'x-api-ticket': ctx.obj['config'].get('DEFAULT', 'api_ticket')
                }

        r = requests.get(ctx.obj['config'].get('DEFAULT', 'api_url'), headers=headers)

        if r.status_code == 200:
            sites = r.json()['sites']

            for site in sites:
                outlines = '{id}: {title}\r\n\t{tagline}'.format(**site)
                click.echo(outlines)
        else:
            click.echo('Failed to fetch list of sites.')
    except:
        click.echo('Failed to connect to server to get list of sites')


sites.add_command(sites_list)
