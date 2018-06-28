# CONSTANTS
DEFAULT_TEMPLATE = 'k8s-conf.template.yaml'

ENV_DEVEL = 'devel'
ENV_PROD = 'prod'

ENV_TO_PROJ = {
    ENV_DEVEL: 'blorg-dev',
    ENV_PROD: 'blorg-prod'  # probably? idk!
}


def docker_tag(owner, env):
    return '%s-%s' % (env, owner)


def image_name(owner, env):
    """Generate the canonical name of the docker image for this server+env+user."""
    # TODO: will need to templatize server name to use this script across repos.
    server = 'blorg-frontend'
    gcloud_proj = ENV_TO_PROJ[env]
    tag = docker_tag(owner, env)

    return 'gcr.io/%(gcloud_proj)s/%(server)s:%(tag)s' % {
        'gcloud_proj': gcloud_proj,
        'server': server,
        'tag': tag,
     }

