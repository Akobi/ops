base:
    '*':
        - common
        - groups
        - users

    'roles:webserver':
        - match: grain
        - web.nginx
