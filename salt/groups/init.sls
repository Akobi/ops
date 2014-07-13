{% for group, args in pillar.get('groups', {}).items() %}
{{ group }}:
    group.present:
        - name: {{ group }}
        - gid: {{ args['gid'] }}
{% endfor %}
