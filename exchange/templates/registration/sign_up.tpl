{% extends "base.tpl" %}

{% block content %}


<form  class="pure-form pure-form-stacked"  method="post"  action="{% url "sign_up" invitation_url %}">

   {% csrf_token %}
 	   {{ form.as_p }}

    <input  class="pure-button pure-button-primary nobutton"  type="submit"/>
</form>

{% endblock %}
