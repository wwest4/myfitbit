from datetime import date, timedelta
import argparse
import configparser
import getpass
import logging
import json

logging.basicConfig(level=logging.DEBUG)

import requests
from . import Fitbit, FitbitAuth
from .export import FitbitExport


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    fa = FitbitAuth(
        client_id=config['fitbit_auth']['client_id'],
        client_secret=config['fitbit_auth']['client_secret'],
    )
    fa.ensure_access_token()

    try:
        f = Fitbit(access_token=fa.access_token['access_token'])
        print(json.dumps(f.profile, indent=2))
    except requests.exceptions.HTTPError as e:
        print(e.response.status_code)
        if e.response.status_code == 429:
            print(e.response.headers)
        raise

    export = FitbitExport('.', f)

    export.sync_sleep()
    export.sync_heartrate_intraday()
    return


if __name__ == '__main__':
    main()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--username', required=True)
    # parser.add_argument('--ask-password', required=True, action='store_true')
    # args = parser.parse_args()
