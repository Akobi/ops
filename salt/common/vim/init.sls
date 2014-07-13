vim:
  pkg.installed

/etc/vim/vimrc:
  file.managed:
    - source: salt://common/vim/vimrc
    - mode: 644
    - user: root
    - group: root
