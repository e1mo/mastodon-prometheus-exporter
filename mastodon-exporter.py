#!/usr/bin/python3

from urllib import request
import prometheus_client as pc
import configparser as cp
from datetime import datetime
import os
import wsgiref
import json
import time
import argparse

args = argparse.ArgumentParser(description='Export prometheus metrics about a mastodon instance by em1o. Released under the BSD-3-Clause LICENSE, see LICENSE for the full text.')
args.add_argument('instance', metavar='instance', type=str, help='Mastodon instance to query')
args.add_argument('--address', '-a', type=str, help='Host to bind the webserver to. Defaults to 127.0.0.1')
args.add_argument('--port', '-p', type=int, help='The port to listen and serve the metrics on. Defaults to 38171')
args.add_argument('--protocol', type=str, help='Protocol to use. Defaults to https', choices=['http', 'https'])
args.add_argument('--interval', '-i', type=int, help='Time betwen calls to the API in seconds, be aware of mastodons rate limit. Defaults to 60s')
args.add_argument('--config', '-c', type=str, help='Absolute Path to the configuration ini. Will get overwritten bei other arguments.')

defaultConf = {
    'address': '127.0.0.1',
    'port': '38171',
    'interval': 60,
    'protocol': 'https'
}

args = args.parse_args()

localConf = defaultConf

localConf['instance'] = args.instance

configpath = args.config

localConf = defaultConf
if configpath is not None and os.path.isfile(configpath):
    print('[{}] Load config from {}'.format(datetime.now().strftime('%FT%H:%M%Z%z'), configpath))
    config = cp.ConfigParser()
    config.read(configpath)
    if localConf['instance'] in config:
        for key in config[localConf['instance']]:
            localConf[key.lower()] = config[localConf['instance']][key]

elif configpath is not None:
    print('[{}] {} not found or is not accesible'.format(datetime.now().strftime('%FT%H:%M%Z%z'), configpath))
    exit(1)

if args.protocol is not None:
    localConf['protocol'] = args.protocol

if args.address is not None:
    localConf['address'] = args.address

if args.port is not None:
    localConf['port'] = args.port

if args.interval is not None:
    localConf['interval'] = args.interval

print('[{}] Running width {}'.format(datetime.now().strftime('%FT%H:%M%Z%z'), localConf))

instance_url = localConf['protocol'] + '://' + localConf['instance']

host = localConf['address']
port = int(localConf['port'])

interval = localConf['interval']

last_query = pc.Info('mastodon_last_query', 'Unix timestamp of the last query of the api')
version = pc.Info('mastodon_version', 'Version of the mastodon instance')
title = pc.Info('mastodon_title', 'Title of the mastodon instance')
uri = pc.Info('mastodon_uri', 'Uri of the mastodon instance')
short_description = pc.Info('mastodon_short_description', 'Short description of the mastodon instance')
description = pc.Info('mastodon_description', 'Description of the mastodon instance')
email = pc.Info('mastodon_email', 'Email of the mastodon instance')

user_count = pc.Gauge('mastodon_user_count', 'Count of the users on this instance')
status_count = pc.Gauge('mastodon_status_count', 'Count of the statuses on this instance')
domain_count = pc.Gauge('mastodon_domain_count', 'Count of the connected domains to this instance')
custom_emoji_count = pc.Gauge('mastodon_custom_emoji_count', 'Count of the custom emojis on this instance')

trends = pc.Info('mastodon_trends', 'Trends on this mastodon instance')

def collectMetrics ():
    metrics = {}
    metrics['instance'] = json.loads(request.urlopen('{}/api/v1/instance'.format(instance_url)).read().decode('UTF-8'))
    metrics['custom_emojis'] = json.loads(request.urlopen('{}/api/v1/custom_emojis'.format(instance_url)).read().decode('UTF-8'))
    metrics['trends'] = json.loads(request.urlopen('{}/api/v1/trends'.format(instance_url)).read().decode('UTF-8'))

    last_query.info({'timestamp': str(round(time.time()))})
    version.info({'version': metrics['instance']['version']})

    uri.info({'title': metrics['instance']['title']})
    title.info({'uri': metrics['instance']['title']})
    short_description.info({'short_description': metrics['instance']['short_description']})
    description.info({'short_description': metrics['instance']['description']})
    email.info({'email': metrics['instance']['email']})
    user_count.set(metrics['instance']['stats']['user_count'])
    status_count.set(metrics['instance']['stats']['status_count'])
    domain_count.set(metrics['instance']['stats']['domain_count'])
    custom_emoji_count.set(len(metrics['custom_emojis']))

    _trends = {}
    for trend in metrics['trends']:
        _trends[trend['name']] = trend['history'][0]['uses']

    trends.info(_trends)

print('[{}] start exporting Stats about {}'.format(datetime.now().strftime('%FT%H:%M%Z%z'), instance_url))
print('[{}] listening on {}:{}. Point your Prometheus installation at this address and port'.format(datetime.now().strftime('%FT%H:%M%Z%z'), host, port))
pc.start_wsgi_server(port, addr=host)

while True:
    collectMetrics()
    time.sleep(interval)

