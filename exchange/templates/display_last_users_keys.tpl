
{% extends "base.tpl" %}

{% block content %}

{% for user_key in last_users_keys %}
<div id='user_data' >

</div>

{{user_key.user}} posté le {{user_key.date}} </br>

</p>
Type de clef:{{user_key.key_type}} ({{user_key.name}}) </br>
{{user_key.content}} </br>
</br>
</br>


{# Mise en forme de la pagination ici #}
{% if is_paginated %}
    <div class="pagination">
           {% if page_obj.has_previous %}
               <a href="?page={{ page_obj.previous_page_number }}">Précédente</a> —
           {% endif %}
           Page {{ page_obj.number }} sur {{ page_obj.paginator.num_pages }}
           {% if page_obj.has_next %}
              — <a href="?page={{ page_obj.next_page_number }}">Suivante</a>
           {% endif %}
    </div>
{% endif %}
{% endfor %}
{% endblock %}
