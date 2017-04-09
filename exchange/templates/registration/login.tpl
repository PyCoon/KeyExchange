{% extends "base.tpl" %}

{% block content %}
<h2> Login </h2>



<form  class="pure-form pure-form-stacked" method="post"  action="{% url "login_user" %}">
 	   {% csrf_token %}
 	   {{ form.as_p }}

      <div id="message" >{{message}}</div>
      
        <input  class="pure-button pure-button-primary nobutton" type="submit"/>
</form>

{% endblock %}
