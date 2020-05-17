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
```

### Venv installation

```bash
$ git clone https://github.com/e1mo/mastodon-prometheus-exporter.git
$ cd mastodon-prometheus-exporter
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

### Systemd
TODO

## Usage

```bash
usage: mastodon-exporter.py [-h] [--address ADDRESS] [--port PORT]
               [--protocol {http,https}] [--interval INTERVAL]
               instance

Export prometheus metrics about a mastodon instance

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

$ ./mastodon-exporter.py mastodon.social
[2020-05-17T03:32] start exporting Stats about https://mastodon.social
[2020-05-17T03:32] listening on 127.0.0.1:38171. Point your Prometheus at this address and port

$ ./mastodon-exporter.py chaos.social --address 0.0.0.0 --port 8081 --protocol http --interval 120
[2020-05-17T03:33] start exporting Stats about http://chaos.social
[2020-05-17T03:33] listening on 0.0.0.0:8081. Point your Prometheus at this address and port
```

## LICENSE

This Software is released under the BSD-3-Clause license. See [LICENSE](LICENSE) for the full license.

