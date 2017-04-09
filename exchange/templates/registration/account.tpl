{% extends "base.tpl" %}

{% block content %}




<h2> Mon Profil </h2>

<div id="user_data" >

<dl>
    <dt>Nom d'utilisateur: </dt>
    <dd>{{request.user.username}}</dd>
    <dt>Email:</dt>
    <dd>{{user.email}}</dd>
        <dt>Nombre de clefs actives: </dt>
    <dd>{{user.profil.key_nb}}</dd>
    <dt>Dernière connexion:</dt>
    <dd>{{user.last_login}}</dd>
        <dt>Date d'inscription: </dt>
    <dd>{{request.user.username}}</dd>
    <dt>{{user.date_joined}}</dt>


</dl>
<h2>Notification</h2>
{% if friend_requests %}
<a href="{% url "note_notif_as_read" %}" > Noter les notifications comme lues </a>
{% for request in friend_requests %}
<ul class="data-list" >
<li><a href="{% url "detail_user_key" request.sender_user.pk %}"> {{request.sender_user.username}} </a></li>
<li>{{request.message}}</li>
<li>{{request.date}}</li>
</ul>


{%endfor%}


<div class="pagination">
    <span class="step-links">
        {% if friend_requests.has_previous %}
            <a href="?page={{ friend_requests.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ friend_requests.number }} sur {{ friend_requests.paginator.num_pages }}.
        </span>

        {% if friend_requests.has_next %}
            <a href="?page={{ friend_requests.next_page_number }}">Suivante</a>
        {% endif %}
    </span>
</div>

{%else%}
<p><i>Pas de notifications pour le moment. </i></p>

{% endif %}
<div id="info" >
{{message}}

</div>
</br>
{%if form_ %}
<form action="{% url "exchange.views.account_detail" %}" method="post" class="pure-form pure-form-stacked"  >

{% csrf_token %}

{{form_.as_p}}
</form >

{% endif %}
<h2>Mes clefs Uploadées</h2>

{%if forms_and_keys %}
</br>
{%else%}
Pas de clefs uploadées.
{% endif %}



{% for key, form  in forms_and_keys %}
Type de clef: {{key.key_type}} Nom de la clef:  {{key.name}} </br>


<form action="{% url "exchange.views.account_detail" %}" method="post" class="pure-form pure-form-stacked"  >

{% csrf_token %}

{{ form.as_p }}  <input class="pure-button pure-button-primary nobutton"  type="submit" value="Supprimer" />
</form >

{% endfor%}



{% endblock %}
