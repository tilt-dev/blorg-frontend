#!/usr/bin/env python

import argparse
import getpass

DEFAULT_TEMPLATE = 'k8s-conf.template.yaml'

ENV_DEVEL = 'devel'
ENV_PROD = 'prod'

KEY_ENVIRONMENT = 'environment'
KEY_OWNER = 'owner'
KEY_GCLOUD_PROJ = 'gcloud_proj'
KEY_DOCKER_TAG = 'docker_tag'

ENV_TO_PROJ = {
    ENV_DEVEL: 'blorg-dev',
    ENV_PROD: 'blorg-prod'  # probably? idk!
}


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Populate k8s config file template with the appropriate values.')
    parser.add_argument('environment', type=str,
                        help='environment you\'re deploying to',
                        choices=[ENV_DEVEL, ENV_PROD])
    parser.add_argument('--file', type=str,
                        help=('path to template file (default: %s)' %
                              DEFAULT_TEMPLATE),
                        default=DEFAULT_TEMPLATE)
    return parser.parse_args()


def get_file(filename):
    with open(filename) as infile:
        body = infile.read()

    return body


def write_file(filename, contents):
    """Write the given contents to the given file. (If file exists, overwrite it.)"""
    with open(filename, 'w') as outfile:
        outfile.write(contents)


def outfile_name(infile):
    """Given infile (i.e. template file), generates outfile name."""
    outfile = '%s.%s' % (infile, 'generated')
    if 'template' in infile:
        outfile = infile.replace('template', 'generated')
    return outfile


def docker_tag(owner, env):
    return '%s-%s' % (env, owner)


def main():
    # setup
    args = parse_args()
    owner = getpass.getuser()

    temp_vals = {
        KEY_ENVIRONMENT: args.environment,
        KEY_OWNER: owner,
        KEY_GCLOUD_PROJ: ENV_TO_PROJ[args.environment],
        KEY_DOCKER_TAG: docker_tag(owner, args.environment)
    }
    template = get_file(args.file)

    outfile = outfile_name(args.file)

    populated = template % temp_vals

    write_file(outfile, populated)


if __name__ == '__main__':
    main()
