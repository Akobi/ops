base:
    '*':
        - common
        - groups
        - users

    'roles:webserver':
        - match: grain
        - web.nginx

    'P@roles:(web|app)server':
        - match: compound
        - python.pkgs
