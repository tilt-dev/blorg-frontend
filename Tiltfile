# -*- mode: Python -*-

def blorg_frontend():
  env = 'devel'
  entrypoint = '/app/server'
  image = build_docker_image('Dockerfile.base', 'gcr.io/blorg-dev/blorg-frontend:devel-' + local('whoami').rstrip('\n'), entrypoint)
  src_dir = '/go/src/github.com/windmilleng/blorg-frontend'
  image.add(local_git_repo('.'), src_dir)
  image.run('cd ' + src_dir + '; mkdir -p /app; go build -o server; cp index.html /app/; cp -r public /app/; cp server /app/')

  # print(image)
  yaml = local('python populate_config_template.py ' + env + ' 1>&2 && cat k8s-conf.generated.yaml')

  # this api might be cleaner than stderr stuff above
  # run('python populate_config_template.py ' + env')
  # yaml = read('k8s-conf.generated.yaml')

  # print(yaml)
  return k8s_service(yaml, image)
