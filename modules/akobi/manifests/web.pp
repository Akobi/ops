class akobi::web {
  file { ['/var/www', '/var/www/dev', '/var/www/publish']:
    ensure => directory,
    owner  => root,
    group  => root,
    mode   => 0750,
  }

  service { 'nginx':
    ensure => running
  }
}
