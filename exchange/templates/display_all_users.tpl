
{% extends "base.tpl" %}

{% block content %}
Voici les derniers utilisateurs enregistrés sur le site. 
Cliquez sur un nom d'utilisateur pour voir ses clefs. 

<table class="pure-table pure-table-horizontal">
    <thead>
        <tr>

            <th>Nom d'utilisateur</th>
            <th>Dernière connexion</th>
            <th>Nombre de clefs actives</th>
        </tr>
    </thead>

{% for user in users %}


    <tbody>
        <tr>
            <td><a href="{% url "detail_user_key" user.id %}">{{user.username}}</a></td>
            <td>{{user.last_login}}</td>
            <td>{{user.profil.key_nb}}</td>
        </tr>




{% endfor %}
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

{% endblock %}

    </tbody>
</table>
