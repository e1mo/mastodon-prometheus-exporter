# mastodon-prometheus-exporter

Export public information about a mastodon instance to prometheus using [the official python prometheus_client](https://github.com/prometheus/client_python/).

## Requirements

- Python3
- Pip
- Git (if you want to clone from GitHub, otherwise download the ZIP file from the GitHub repo)

## Installation

### Barebones installation

This is the most barebones installation possible.

```bash
$ git clone https://github.com/e1mo/mastodon-prometheus-exporter.git
$ cd mastodon-prometheus-exporter
$ pip3 install -r requirements.txt
$ cp instances.ini.example instances.ini # Optional
```

### Venv installation

```bash
$ git clone https://github.com/e1mo/mastodon-prometheus-exporter.git
$ cd mastodon-prometheus-exporter
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ cp instances.ini.example instances.ini # Optional
```

### Systemd
TODO

<!--
```bash
# adduser --home /opt/mastodon-exporter/ --shell /bin/bash --disabled-password --disabled-login mastodon-exporter
# su - mastodon-exporter
$ git clone https://github.com/e1mo/mastodon-prometheus-exporter.git
$ cd mastodon-prometheus-exporter
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
-->

## Usage

```bash
usage: mastodon-exporter.py [-h] [--address ADDRESS] [--port PORT]
                            [--protocol {http,https}] [--interval INTERVAL]
                            [--config CONFIG]
                            instance

Export prometheus metrics about a mastodon instance by em1o. Released under
the BSD-3-Clause LICENSE, see LICENSE for the full text.

positional arguments:
  instance              Mastodon instance to query

optional arguments:
  -h, --help            show this help message and exit
  --address ADDRESS, -a ADDRESS
                        Host to bind the webserver to. Defaults to 127.0.0.1
  --port PORT, -p PORT  The port to listen and serve the metrics on. Defaults
                        to 38171
  --protocol {http,https}
                        Protocol to use. Defaults to https
  --interval INTERVAL, -i INTERVAL
                        Time betwen calls to the API in seconds, be aware of
                        mastodons rate limit. Defaults to 60s
  --config CONFIG, -c CONFIG
                        Absolute Path to the configuration ini. Will get
                        overwritten bei other arguments.

$ ./mastodon-exporter.py mastodon.social
[2020-05-17T06:19] Running width {'address': '127.0.0.1', 'port': '38171', 'interval': 60, 'protocol': 'https', 'instance': 'mastodon.social'}
[2020-05-17T06:19] start exporting Stats about https://mastodon.social
[2020-05-17T06:19] listening on 127.0.0.1:38171. Point your Prometheus installation at this address and port

$ ./mastodon-exporter.py chaos.social --address 0.0.0.0 --port 8081 --protocol http --interval 120
[2020-05-17T06:19] Running width {'address': '0.0.0.0', 'port': 8081, 'interval': 120, 'protocol': 'http', 'instance': 'chaos.social'}
[2020-05-17T06:19] start exporting Stats about http://chaos.social
[2020-05-17T06:19] listening on 0.0.0.0:8081. Point your Prometheus installation at this address and port

$ ./mastodon-exporter.py chaos.social --config instances.ini
[2020-05-17T06:20] Load config from instances.ini.example
[2020-05-17T06:20] Running width {'address': '127.0.0.1', 'port': '38171', 'interval': 60, 'protocol': 'https', 'instance': 'chaos.social'}
[2020-05-17T06:20] start exporting Stats about https://chaos.social
[2020-05-17T06:20] listening on 127.0.0.1:38171. Point your Prometheus installation at this address and port
```

## Configuration

In the `instances.ini` you can define the same settings you can pass as arguments. The syntax is as follows, all entries are optional. The section with the matching instance name is chosen, this is extremely useful if you want to run multiple exporters  without being able to modify the arguments passed every time.

```ini

[mastodon.social]
port=1336
# equals to
# ./mastodon-exporter.py chaos.social --port 1336

[chaos.social]
address=0.0.0.0
port=1337
interval=300
protocol=https
# equals to
# ./mastodon-exporter.py chaos.social --port 1336 --address 0.0.0.0 --interval 300 --protocol https

```

## LICENSE

This Software is released under the BSD-3-Clause license. See [LICENSE](LICENSE) for the full license.

