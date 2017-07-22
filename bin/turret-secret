#!/usr/bin/python

import os
import click
import pillbox
from ansible_vault import Vault
from tabulate import tabulate
from signal import signal, SIGPIPE, SIG_DFL
from distutils.util import strtobool

signal(SIGPIPE, SIG_DFL)

@click.group()
@click.option('--url', envvar='PILLBOXURL')
@click.option('--login', envvar='PILLBOXLOGIN')
@click.option('--password', envvar='PILLBOXPASSWORD')
@click.option('--token', envvar='PILLBOXTOKEN')
@click.option('--vaultpass', envvar='PILLBOXVAULTPASS')
def cli(token, url, login, password, vaultpass):
    """ Tool for storing secrets 
        
        Client side encryption using ansible vault.
    """
    global ts
    ts = pillbox.secrets(url,login,password,token)
    ts.vault = Vault(vaultpass)


@cli.command()
@click.option('--category','-c')
def show(category):
    """ show list of stored secrets """

    where = None
    if category:
        where='{{"category": "{}"}}'.format(category)

    r = ts.listSecretsStores(where)
    if r.status_code == 500:
        click.echo("500 Internal Server Error")
        return False

    results = r.json()
    if r.status_code != 200:
        click.echo("{} {}".format(r.status_code, results['_error']['message']))
        return False
    else:
        data = []
        for row in results['_items']:
             data.append([row['category'] if 'category' in row else 'default', row['name'], row['_created_by'] if '_created_by' in row else '-', row['_modified_by'] if '_modified_by' in row else '-', row['_remote_addr'] if '_remote_addr' in row else '-'])

        click.echo(tabulate(data, headers=["Category","StoreName", "Creator", "Modifier", "Modifier ip"], tablefmt="fancy_grid"))

@cli.command()
@click.option('--category','-c', prompt=True)
@click.option('--storename',prompt=True)
def new(category, storename):
    data = {}
    data['category'] = category
    data['name'] = storename
    data['store'] = ''
    result = ts.createSecretsStore(data)
    click.echo("Result: {}".format(result.status_code))

@cli.command()
@click.option('--category','-c', default=None)
@click.option('--storename',prompt=True)
def edit(category, storename):

    r = ts.findSecretsStore(storename).json()

    aantal = r['_meta']['total']

    if aantal == 0:
        print 'Niet gevonden'
        return False
    elif aantal == 1:
        etag = r['_items'][0]['_etag']
        passwordID = r['_items'][0]['_id']

        if r['_items'][0]['store']:
            content = ts.vault.load(r['_items'][0]['store'])
        else:
            content = ''

        content = click.edit(content)        

        data = {}
        data['store'] = ts.vault.dump(content)
        if category:
            data['category'] = category

        r2 = ts.updateSecretsStore(passwordID, etag, data)
        click.echo("Result: {}".format(r2.status_code))
        
        return True
    elif aantal > 1:
        click.echo("Huh, multiple secret stores with this name?")
        return False

@cli.command()
@click.option('--storename', prompt=True)
def display(storename, decrypt=True):
    result = ts.findSecretsStore(storename)

    r = result.json()

    aantal = r['_meta']['total']

    if aantal == 0:
        click.echo("Store not found")
        return False
    elif aantal == 1:
        passwordID = r['_items'][0]['_id']
        if r['_items'][0]['store']:
            if decrypt:
                content = ts.vault.load(r['_items'][0]['store'])
            else:
                content = r['_items'][0]['store']
        else:
            content = ''

        click.echo("ID: {}".format(passwordID))
        click.echo("Content:")
        click.echo("-" * 80)
        click.echo(content)
        click.echo("-" * 80)

    elif aantal > 1:
        click.echo("Huh, multiple secret stores with this name?")
        return False

@cli.command()
@click.option('--storename', prompt=True)
@click.confirmation_option(help='Are you sure you want to delete the secret store?')
def delete(store):
    r = ts.findSecretsStore(store).json()

    aantal = r['_meta']['total']

    if aantal == 0:
        click.echo("Store not found")
        return False
    elif aantal == 1:
        etag = r['_items'][0]['_etag']
        passwordID = r['_items'][0]['_id']

        r2 = deletePasswordStore(passwordID, etag) 
        click.echo("Result: {}".format(r2.status_code))
        return True
    elif aantal > 1:
        click.echo("Huh, multiple secret stores with this name?")
        return False

if __name__ == "__main__":
    cli()
