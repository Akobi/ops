import json
import logging
import os
import subprocess
import sys

import tornado.web
from tornado.ioloop import IOLoop

CONFIG_FILE = "configs.json"
LOG_FILE = "autodeploy.log"

logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt="%m/%d/%Y %I:%M:%S %p",
                    filename=LOG_FILE,
                    level=logging.DEBUG)

class GithubPostReceiveHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(GithubPostReceiveHandler, self).__init__(*args, **kwargs)
        self.configs = self.load_configs()

    def load_configs(self):
        with open(CONFIG_FILE) as configs:
            json_configs = json.loads(configs.read())
            return json_configs

    def get(self, *args, **kwargs):
        self.write("Hello")

    def _extract_configs(self, repo_url):
        all_configs = self.configs['repos']
        repo_configs = None

        try:
            repo_configs = all_configs[repo_url]
        except KeyError:
            logging.debug("Repo %s not in config. Ignoring" % repo_name)

        return repo_configs

    def _build_deploy_cmd(self, repo_configs, branch_name):
        path = None
        deploy_cmds = None

        for config in repo_configs:
            if config['ref'] == branch_name:
                path = config['path']
                deploy_cmds = config['deploy']

        if path is None or deploy_cmds is None:
            logging.debug("Wasn't expecting post-receive from ref: %s"
                            % branch_name)
            return None

        cmd_str = " && ".join(deploy_cmds)
        cmd = "cd %s && %s" % (path, cmd_str)
        logging.info(cmd)
        return cmd

    def do_deploy(self, repo, branch):
        repo_url = repo['url']
        repo_configs = self._extract_configs(repo_url)

        deploy_cmd = self._build_deploy_cmd(repo_configs, branch)
        if deploy_cmd is None:
            return

        subprocess.call(deploy_cmd, shell=True)
        logging.info("Finished deploying")
        return

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        event = self.request.headers['X-Github-Event']
        if event == "ping":
            logging.info("Got ping..")
            self.write("ACK")
            self.finish()
            return

        payload = self.request.body
        body = json.loads(payload)
        repo = body['repository']
        branch = body['ref']

        logging.info("Got POST for repo: %s" % repo['url'])

        IOLoop.instance().add_callback(self.do_deploy, repo, branch)

        self.write("ACK")
        self.finish()
        return

def main():
    app = tornado.web.Application([
        (r'/', GithubPostReceiveHandler)
    ])
    app.listen(8001)

    IOLoop.instance().start()

if __name__ == '__main__':
    user_id = os.getuid()
    if not user_id == 0:
        print "Script must be run as root!"
        sys.exit(1)

    main()
