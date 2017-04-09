{% extends "base.tpl" %}

{% block content %}
{% load staticfiles %}

<h2>Tutoriels</h2>

<h3>Installation et configuration de Rétroshare</h3>

<ul>
<li><a href="{% url "installation" %}">Installer le logiciel</a></li>
<li><a href="{% url "partager" %}">Partager des fichiers</a></li>
<li><a href="{% url "ajouter_ami" %}">Ajouter des amis</a></li>
</ul>

      {% endblock %}


