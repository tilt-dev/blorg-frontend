#!/usr/bin/env python

import deploy_utils as utils

import argparse
import textwrap
import getpass


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        Deploy the `blorg` app to Kubernetes development cluster (i.e. NOT PROD).
        
        Deploy consists of the following steps:
        1. (re)build Docker image
        2. push docker image to gcr.io
        3. generate k8s config file (by populating template)
        4. create/update k8s from config file
        
        If this is your first time deploying to the dev cluster, run with flag --first-deploy.
        (Actually jk this isn't implemented yet, it's here as a TODO o_0 )
        """))
    parser.add_argument('--config_template', '-c', type=str,
                        help=('path to config template file (default: %s)' %
                              utils.DEFAULT_TEMPLATE),
                        default=utils.DEFAULT_TEMPLATE)
    return parser.parse_args()


def main():
    # setup
    args = parse_args()
    owner = getpass.getuser()

    # 1. (re)build Docker image
    # 2. push docker image to gcr.io
    # 3. generate k8s config file (by populating template)
    # 4. create/update k8s from config file




if __name__ == '__main__':
    main()
