python-pip:
    pkg.installed

{% for provider, pkgs in pillar.get('python-packages').items() %}
    {% if provider == 'pip' %}
        {% for pkg, args in pkgs.items() %}
{{ pkg }}:
    pip.installed:
        - name: {{ pkg }} {{ args['version'] }}
        - requires:
            - pkg: python-pip
        {% endfor %}
    {% elif provider == 'apt-get' %}
        {% for pkg in pkgs %}
{{ pkg }}:
    pkg.installed
        {% endfor %}
    {% endif %}
{% endfor %}
