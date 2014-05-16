class akobi::packages::python {
  package { 'python-pip':
    ensure => present
  }

  package { 'virtualenv':
    ensure   => present,
    provider => pip
  }

  package { 'tornado':
    ensure   => present,
    provider => pip
  }
}
