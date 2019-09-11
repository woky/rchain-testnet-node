#!/usr/bin/env python3

import os
import time
import logging
import subprocess


logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
LOGGER = logging.getLogger()


def parse_conf(contents):
    result = {}
    for line in contents.splitlines():
        if line == '':
            continue
        key, value = line.split('=', maxsplit=1)
        value = value.strip('"')
        value = value.strip("'")
        result[key] = value
    return result


def parse_conf_file(file_name):
    with open(file_name) as file:
        contents = file.read()
        return parse_conf(contents)


def main():
    config = parse_conf_file('/var/lib/rnode-static/autopropose.conf')
    deploy_no_sooner_than_every = int(config.get('period', '60'))

    deploy_env = {}
    if 'contract' in config:
        deploy_env['contract'] = config['contract']
    elif 'RD_OPTION_CONTRACT' in os.environ:
        deploy_env['RD_OPTION_CONTRACT'] = os.environ['RD_OPTION_CONTRACT']

    for env_var in ('RD_OPTION_DEPLOY_KEY', 'RD_OPTION_RNODE_LAUNCHER_ARGS', 'RD_OPTION_RNODE_DEPLOY_ARGS'):
        if env_var in os.environ:
            deploy_env[env_var] = os.environ[env_var]

    LOGGER.info('Deploying contract %s every %d seconds', deploy_env.get('contract'), deploy_no_sooner_than_every)

    while True:
        while True:
            rnode_container_hash = subprocess.check_output(['docker', 'ps', '--quiet', '--filter=name=^rnode$'])
            if rnode_container_hash != '':
                break
            time.sleep(15)

        try:
            deploy_started_at = int(time.monotonic())
            LOGGER.info("Deploying %s", deploy_env.get('contract'))
            subprocess.check_output(['/opt/rchain-testnet-node/rundeck-scripts/deploy'], env=deploy_env)
        except subprocess.CalledProcessError:
            LOGGER.exception('deploy')

        deploy_finished_at = int(time.monotonic())
        deploy_took = deploy_finished_at - deploy_started_at
        if deploy_took < deploy_no_sooner_than_every:
            wait_duration = deploy_no_sooner_than_every - deploy_took
            time.sleep(wait_duration)

        try:
            LOGGER.info("Proposing...")
            subprocess.check_output(['/opt/rchain-testnet-node/rundeck-scripts/propose'])
        except subprocess.CalledProcessError:
            LOGGER.exception('propose')

if __name__ == '__main__':
    main()
