define akobi::user(
    $ingroups = ['ssh-allow']
  ) {

  $homedir         = "/home/$name"
  $sshdir          = "$homedir/.ssh"
  $authorized_keys = "$sshdir/authorized_keys"

  user { $name:
    name     => $name,
    ensure   => present,
    groups   => $ingroups,
    home     => $homedir,
    shell    => "/bin/bash",
    # password => sha1($name)
  }

  file { [$homedir, $sshdir]:
    ensure  => directory,
    owner   => $name,
    group   => $name,
    mode    => 0750,
    require => User[$name]
  }

  file { $authorized_keys:
    ensure  => present,
    owner   => $name,
    group   => $name,
    mode    => 0644,
    require => File[$sshdir]
  }
}
