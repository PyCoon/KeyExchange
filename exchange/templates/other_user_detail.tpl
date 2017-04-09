{% extends "base.tpl" %}
{% load key_format %}


{% block content %}


{% if form %}


<b>Vous souhaitez que un de vos amis télécharge votre clef ? Laissez lui un message, il sera informé que vous avez téléchargé la sienne en <a href='#' id="showit">cliquant ici</a></b>

<form {%if form.errors%} style="display: auto;" {%else%} style="display: none;" {%endif%} class="pure-form pure-form-stacked"  method="post"  action=""{% url "detail_user_key" user.id %}">
 	   {% csrf_token %}
 	   {{ form.as_p }}

    <input   class="pure-button pure-button-primary nobutton"  type="submit"/>
</form>


<p>

<a   href="{% url "detail_user_key" user.id %}">{{user.username}}</a> dernière connexion le <i>{{user.last_login}}</i> </br>
Inscrit depuis le <i>{{user.date_joined}}</i></br></p>

{%for  key in keys %}
{{key.name}} ajoutée le
{{key.date}}

  <div id="key{{key.pk}}" class="key"  >
  
  {{key.content}}
  </div>


{% endfor %}

{% endif %}
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
{%if sended%}
<script type="text/javascript" > 

alert("Votre message a été envoyé à {{user.username}}.");

</script>
{%endif%}

<script type="text/javascript" > 

$(document).ready(function() {
    $('#showit').click(function() {
            $('.pure-form').slideToggle("slow");
    });
});

</script>

{% endblock %}
