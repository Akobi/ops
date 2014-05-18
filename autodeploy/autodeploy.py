import json
import logging
import os
import subprocess
import sys

import tornado.web
import tornado.ioloop

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
        config_repos = self.configs['repos']
        logging.info("Got POST for repo: %s" % repo['url'])

        try:
            repo = config_repos[repo['url']]
        except KeyError:
            logging.debug("Repo %s not in config. Ignoring..." % repo['url'])
            return

        path = None
        deploy_cmds = None
        for deploy_info in repo:
            if deploy_info['ref'] == body['ref']:
                path = deploy_info['path']
                deploy_cmds = deploy_info['deploy']

        if path is None or deploy_cmds is None:
            logging.debug("Wasn't expecting post-receive from ref: %s"
                            % body['ref'])
            return

        cmd_str = " && ".join(deploy_cmds)
        cmd = "cd %s && %s" % (path, cmd_str)
        logging.info(cmd)
        subprocess.call(cmd, shell=True)
        logging.info("Finished deploying")
        self.write("ACK")
        self.finish()

def main():
    app = tornado.web.Application([
        (r'/', GithubPostReceiveHandler)
    ])
    app.listen(80)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    user_id = os.getuid()
    if not user_id == 0:
        print "Script must be run as root!"
        sys.exit(1)

    main()
