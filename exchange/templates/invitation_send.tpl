{% extends "base.tpl" %}

{% block content %}
{% load staticfiles %}
{%if form%}

{%if name%}
Votre invitation à {{name}} a bien été envoyée !!!
{%endif%}


{{message}}
<form  class="pure-form pure-form-stacked"  method="post"  action="{% url "create_invitation" %}">
 	   {% csrf_token %}
 	   {{form}}


    <input  class="pure-button pure-button-primary nobutton"  type="submit"/>
</form>
{%endif%}
{%endblock%}
