define akobi::user(
    $ingroups = ['ssh-allow']
  ) {

  $homedir = "/home/$name"

  user { $name:
    name     => $name,
    ensure   => present,
    groups   => $ingroups,
    home     => $homedir,
    shell    => "/bin/bash",
  }

  file { $homedir:
    ensure  => directory,
    owner   => $name,
    group   => $name,
    mode    => 0750,
    require => User[$name]
  }
}
