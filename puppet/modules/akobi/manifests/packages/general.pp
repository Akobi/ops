class akobi::packages::general {
  package { 'git-core':
    ensure => latest
  }

  package { 'nginx':
    ensure => latest
  }
}
