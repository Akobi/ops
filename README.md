puppet
======

Puppet modules and configs for Akobi.

We run masterless puppet as of now, so to use the modules all you have to do is run:

```shell
$ sudo puppet apply manifests/site.pp --modulepath ./modules
```
