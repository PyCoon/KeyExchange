
<p>Please specify your email address to receive instructions for resetting it.</p>


{{message}}
<form  class="pure-form pure-form-stacked"  method="post"  action="{% url "password_reset" %}">
 	   {% csrf_token %}
 	   {{ form.as_p }}

    <input  class="pure-button pure-button-primary nobutton"  type="submit"/>
</form>
