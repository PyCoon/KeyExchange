{% extends "base.tpl" %}
{% block title %}Reinitialiser son mot de passe{% endblock %}

{% block content %}
<form  class="pure-form pure-form-stacked"  method="post"  action="{% url "do_reset_password_now" reset_url %}">
 	   {% csrf_token %}
 	   {{ form.as_p }}

    <input  class="pure-button pure-button-primary nobutton"  type="submit"/>
</form>
{% endblock %}
