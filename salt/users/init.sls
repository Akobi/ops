{% for user, args in pillar.get('users', {}).items() %}
{{user}}:
    group.present:
        - gid: {{ args['id'] }}

    user.present:
        - password: {{ args['password'] }}
        - shell: /bin/bash
        - home: /home/{{user}}
        - createhome: True
        - uid: {{ args['id'] }}
        - gid: {{ args['id'] }}
        - groups: {{ args['groups'] }}
{% endfor %}
