{% extends "base.tpl" %}

{% block content %}
{% load staticfiles %}

<input type='button' id='button' value="Afficher l'aide" >
<div id='content' >
  Pour trouver votre clef retroshare, cliquez d'abord sur " Ajouter un ami".

  <img src="{% static "tuto_images/menu_ajout_ami.png" %}" class="pure-img img_tuto" alt="Aide_ajout_ami"/>

Cliquez sur suivant jusqu'à trouver la fenêtre suivante:

  <img src="{% static "tuto_images/entrez_certificat_version_texte.png" %}" class="pure-img img_tuto" alt="Aide_entrer_certificat"/>


Votre clef retroshare est ici. Cet amas de chiffres et de lettres dans son ensemble.
Il ne vous reste plus qu'à copier le tout et à la poster dans ce formulaire.
Enjoy.


</div>



<form  class="pure-form pure-form-stacked"  method="post"  action="{% url "upload_key" %}">
 	   {% csrf_token %}
 	   {{form}}


    <input  class="pure-button pure-button-primary nobutton"  type="submit"/>
</form>




<script type="text/javascript">
var button = document.getElementById('button'); // Assumes element with id='button'

var div = document.getElementById('content');
div.style.display='none';

button.onclick = function() {
    var div = document.getElementById('content');
    if (div.style.display !== 'none') {
        div.style.display = 'none';
    }
    else {
        div.style.display = 'block';
        button.value = "Masquer l'aide";
    }
};
</script>

{% endblock %}
