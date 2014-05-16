node default {
  include akobi

  akobi::user { '<username>':
    ingroups => ['<group1>', '<group2>']
  }
}
