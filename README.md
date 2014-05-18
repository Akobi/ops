## Akobi Ops

Base repo for all of Akobi's ops-related code. This includes puppet modules, shell scripts etc.

- ```puppet/``` - All puppet modules and manifests
- ```autodeploy/``` - Script for autodeploying the website on a push

#### puppet

Contains all our puppet modules and manifests. Currently we only use masterless puppet, so to run the manifests:

- Edit ```manifests/site.pp``` to modify the placeholder strings
- Run ```$ sudo puppet apply manifests/site.pp --modulepath ./modules```

#### autodeploy

Contains a script to autodeploy a site upon push to a remote repo. The current version utilises a POST from Github's [Webhook Service](https://developer.github.com/webhooks/) to pull the new version of the code and optionally execute other deploy-related commands.

Repositories that POSTs are expected from go in the ```configs.json``` file along with a path to the Git repo on the machine, the branch the push is expected from, and all deploy-related commands that need to be run.