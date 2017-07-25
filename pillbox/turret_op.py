#!/usr/bin/python

import os
import click
import bcrypt
import pillbox
from tabulate import tabulate
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)

@click.group()
@click.option('--url', envvar='PILLBOXURL')
@click.option('--login', envvar='PILLBOXLOGIN')
@click.option('--password', envvar='PILLBOXPASSWORD')
@click.option('--token', envvar='PILLBOXADMINTOKEN')
def cli(token, url, login, password):
    global to
    to = pillbox.operators(url,login,password,token)


@cli.command()
def show():
    """ show list of operators """
    r = to.listOperators()

    if r.status_code == 401:
        print "Unauthorized!"
        return False

    results = r.json()

    data = []
    for row in results['_items']:
         data.append([row['name'], row['password'], row['role'], row['description']])

    click.echo(tabulate(data, headers=["Name","Password", "Role", "Description"], tablefmt="fancy_grid"))

@cli.command()
@click.option('-n', '--name', prompt=True, default=lambda: os.environ.get('USER', ''))
@click.option('--description', prompt=True)
@click.password_option()
@click.option('--role', prompt=True, type=click.Choice(['admin', 'user', 'viewer']), default='user')
def add(name,description, password, role):
    """ add new operator """
    data = {}
    data['name'] = name
    data['password'] = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt())
    data['description'] = description
    data['role'] = role

    print data['password']

    result = to.createOperator(data)

    if result.status_code == 201:
        click.echo('Succes!')
    else:
        click.echo('Error!')
        click.echo(result.status_code)
        click.echo(result.text)

@cli.command()
@click.option('-n', '--name', prompt=True, default=lambda: os.environ.get('USER', ''))
@click.password_option()
def chpwd(name, password):
    """ Change operator password """

    result = to.findOperator(name)
    r = result.json()

    aantal = r['_meta']['total']

    if aantal == 0:
        click.echo('Operator not found!')
        return False
    elif aantal == 1:
        etag = r['_items'][0]['_etag']
        opID = r['_items'][0]['_id']

        data = {}
        data['password'] = bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt())

        ru = to.updateOperator(opID, etag, data)
        
        if ru.status_code == 200:
            click.echo('Succes!')
        else:
            click.echo('Error!')
            click.echo(ru.status_code)
            click.echo(ru.json())
    elif aantal > 1:
        click.echo('Huh, multiple operators with this name?')
        return False

@cli.command()
@click.option('-n', '--name', prompt=True, default=lambda: os.environ.get('USER', ''))
@click.option('-t', '--token')
@click.option('-a', '--action', type=click.Choice(['add', 'del', 'show']), prompt='Action [add|del|show]')
def token(name, token, action):
    """ Change operator token """

    result = to.findOperator(name)
    r = result.json()

    aantal = r['_meta']['total']
    
    if aantal == 0:
        click.echo('Operator not found!')
        return False
    elif aantal == 1:
        etag = r['_items'][0]['_etag']
        opID = r['_items'][0]['_id']

        if action == 'show':
            if 'tokens' in r['_items'][0]:
                data = [ [n] for n in r['_items'][0]['tokens']] 
                click.echo(tabulate(data, headers=["tokens {}".format(name)], tablefmt="fancy_grid"))
            else:
                click.echo("No tokens!")
        elif token:
            data = {}
            if 'tokens' in r['_items'][0] and action == 'add':
                tokens = r['_items'][0]['tokens']  
                tokens.append(token)
                data['tokens'] = list(set(tokens))
            elif 'tokens' in r['_items'][0] and token in r['_items'][0]['tokens'] and action == 'del':
                tokens = r['_items'][0]['tokens']  
                tokens.remove(token)
                data['tokens'] = tokens
            elif action == 'del':
                click.echo("No such token")
                return False
            elif action == 'add':
                data['tokens'] = [token]

            ru = to.updateOperator(opID, etag, data)
            
            if ru.status_code == 200:
                click.echo('Success!')
            else:
                click.echo('Error!')
                click.echo(ru.status_code)
                click.echo(ru.json())
    elif aantal > 1:
        click.echo('Huh, multiple operators with this name?')
        return False

@cli.command()
@click.option('-n', '--name', prompt=True, default=lambda: os.environ.get('USER', ''))
@click.confirmation_option(help='Are you sure you want to delete the operator?')
def delete(name):
    """ del operator """
    result = to.findOperator(name)
    r = result.json()

    aantal = r['_meta']['total']

    if aantal == 0:
        print 'Operator not found'
        return False
    elif aantal == 1:
        etag = r['_items'][0]['_etag']
        opID = r['_items'][0]['_id']

        ru = to.deleteOperator(opID, etag) 
        if ru.status_code == 204:
            click.echo('Success!')
        else:
            click.echo('Error!')
            click.echo(ru.status_code)
            click.echo(ru.text)
    elif aantal > 1:
        click.echo('Huh, multiple operators with this name?')
        return False


if __name__ == "__main__":
    cli()
