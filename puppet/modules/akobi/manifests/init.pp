class akobi {
  # Setup users and groups
  include akobi::users
  include akobi::groups

  # Install required global packages
  include akobi::packages::general
  include akobi::packages::python

  include akobi::web
}
