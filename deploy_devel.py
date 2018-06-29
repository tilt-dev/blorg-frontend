#!/usr/bin/env python

import deploy_utils as utils
from populate_config_template import populate_config_template

import argparse
import getpass
import subprocess
import textwrap

def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        Deploy the `blorg frontend` app to Kubernetes development cluster (i.e. NOT PROD).
        
        Deploy consists of the following steps:
        1. (re)build Docker image
        2. push docker image to gcr.io
        3. generate k8s config file (by populating template)
        4. create/update k8s from config file
        
        # TODO(maia): actually implement this
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
    imgname = utils.image_name(utils.ENV_DEVEL, owner)

    # 1. (re)build Docker image
    print('+ (Re)building Docker image...')
    out = subprocess.check_output(['docker', 'build', '-t', imgname, '.'])
    print('~~~ Built Docker image "%s" with output:\n%s' % (imgname, utils.tab_lines(out.decode("utf-8"))))

    # 2. push docker image to gcr.io
    print('+ Pushing Docker image...')
    out = subprocess.check_output(['docker', 'push', imgname])
    print('~~~ Pushed Docker image with output:\n%s' % utils.tab_lines(out.decode("utf-8")))

    # 3. generate k8s config file (by populating template)
    print('+ Generating k8s file from template "%s"...' % args.config_template)
    config = populate_config_template(args.config_template, utils.ENV_DEVEL, owner)
    print('~~~ Generated config file: "%s"\n' % config)

    # 4. create/update k8s from config file
    print('+ Deleting existing pods for this app+owner+env...')
    # TODO: template these keys/vals in conf file so everything is controlled by Python
    labels = {
        'app': 'blorg',
        'environment': utils.ENV_DEVEL,
        'owner': owner,
        'tier': 'frontend'
    }
    selectors = []
    for selector in ['%s=%s' % (k, v) for k, v in labels.iteritems()]:
        selectors.append('-l')
        selectors.append(selector)
    out = subprocess.check_output(['kubectl', 'delete', 'pods'] + selectors)
    print('~~~ Deleted existing pods (if any) with output:\n%s' % utils.tab_lines(out.decode("utf-8")))

    print('+ Applying generated k8s config...')
    out = subprocess.check_output(['kubectl', 'apply', '-f', config])
    print('~~~ Successfully applied config with output:\n%s' % utils.tab_lines(out.decode("utf-8")))


if __name__ == '__main__':
    main()
