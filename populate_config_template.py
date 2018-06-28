#!/usr/bin/env python

import argparse
import getpass

DEFAULT_TEMPLATE = 'k8s-conf.template.yaml'

ENV_DEVEL = 'devel'
ENV_PROD = 'prod'

KEY_ENVIRONMENT = 'environment'
KEY_OWNER = 'owner'
KEY_GCLOUD_PROJ = 'gcloud_proj'

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


def main():
    # setup
    args = parse_args()
    user = getpass.getuser()

    print('user:', user)
    print('env:', args.environment)
    print('file:', args.file)

    temp_vals = {
        KEY_ENVIRONMENT: args.environment,
        KEY_OWNER: user,
        KEY_GCLOUD_PROJ: ENV_TO_PROJ[args.environment]
    }
    template = get_file(args.file)

    outfile = "%s.%s" % (args.file, 'generated')
    if 'template' in args.file:
        outfile = args.file.replace('template', 'generated')
    populated = template % temp_vals

    write_file(outfile, populated)


if __name__ == '__main__':
    main()
