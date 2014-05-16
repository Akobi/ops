## Akobi Ops

Base repo for all of Akobi's ops-related code. This includes puppet modules, shell scripts etc.

- ```puppet/``` - All puppet modules and manifests

#### puppet

Contains all our puppet modules and manifests. Currently we only use masterless puppet, so to run the manifests:

- Edit ```manifests/site.pp``` to modify the placeholder strings
- Run ```$ sudo puppet apply manifests/site.pp --modulepath ./modules```
