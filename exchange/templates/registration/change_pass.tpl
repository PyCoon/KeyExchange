{% extends "base.tpl" %}

{% block content %}
<h2> Changer le mot de passe. </h2>



<form  class="pure-form pure-form-stacked"  method="post"  action="{% url "change_pass_view" %}">
 	   {% csrf_token %}
 	   {{ form.as_p }}

    <input  class="pure-button pure-button-primary nobutton"  type="submit"/>
</form>

{% endblock %}
