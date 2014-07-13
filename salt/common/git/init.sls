git:
    pkg:
        - installed

{% for user, args in pillar.get('users', {}).items() %}
/home/{{ user }}/.gitconfig:
    file.managed:
        - source: salt://common/git/gitconfig
        - mode: 644
        - user: {{ user }}
        - group: {{ user }}
{% endfor %}
