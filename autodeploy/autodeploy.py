import json
import os
import subprocess
import sys

import tornado.web
import tornado.ioloop

CONFIG_FILE = "configs.json"

class GithubPostReceiveHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(GithubPostReceiveHandler, self).__init__(*args, **kwargs)
        self.configs = self.load_configs()

    def load_configs(self):
        with open(CONFIG_FILE) as configs:
            json_configs = json.loads(configs.read())
            return json_configs

    @tornado.web.asynchronous
    def post(self, *args, **kwargs):
        event = self.request.headers['X-Github-Event']
        if event == "ping":
            print "Got ping.."
            self.write("ACK")
            self.finish()
            return

        payload = self.request.body
        body = json.loads(payload)
        repo = body['repository']
        config_repos = self.configs['repos']

        try:
            repo = config_repos[repo['url']]
        except KeyError:
            print "Repo %s not in config. Ignoring..." % repo['url']
            return

        path = None
        deploy_cmds = None
        for deploy_info in repo:
            if deploy_info['ref'] == body['ref']:
                path = deploy_info['path']
                deploy_cmds = deploy_info['deploy']

        if path is None or deploy_cmds is None:
            print "Wasn't expecting post-receive from ref: %s" % body['ref']
            return

        cmd_str = " && ".join(deploy_cmds)
        cmd = "cd %s && %s" % (path, cmd_str)
        print cmd
        subprocess.call(cmd, shell=True)
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
