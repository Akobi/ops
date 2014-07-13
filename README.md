## Akobi Ops

Base repo for all of Akobi's ops-related code. This includes puppet modules, shell scripts etc.

- ```puppet/``` - All puppet modules and manifests
- ```autodeploy/``` - Script for autodeploying the website on a push
- ```nginx/``` - Nginx configurations for the website

#### puppet

[ OUTDATED ]
NOTE: We no longer use puppet and have since moved to [Salt](http://www.saltstack.com). This section is left here for posterity's sake

Contains all our puppet modules and manifests. Currently we only use masterless puppet, so to run the manifests:

- Edit ```manifests/site.pp``` to modify the placeholder strings
- Run ```$ sudo puppet apply manifests/site.pp --modulepath ./modules```

#### autodeploy

Contains a script to autodeploy a site upon push to a remote repo. The current version utilises a POST from Github's [Webhook Service](https://developer.github.com/webhooks/) to pull the new version of the code and optionally execute other deploy-related commands.

Repositories that POSTs are expected from go in the ```configs.json``` file along with a path to the Git repo on the machine, the branch the push is expected from, and all deploy-related commands that need to be run.

#### nginx

Contains Nginx configs for the website. As of now, there is nothing notable being served on the webserver. However, we are using Nginx as a reverse proxy to forward requests to the autodeploy script talked about above.

#### salt

Contains all our salt states for setting up new servers in the fleet. Makes use of pillar data which will, unfortunately, not be added to this repo.
