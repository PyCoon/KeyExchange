{% extends "base.tpl" %}

{% block content %}
{% load staticfiles %}

L'ajout d'amis ne se fait pas par "demande d'invitation", mais par l'échange de clefs publiques. Le site Samlakey fonctionne sur invitation, c'est à dire que les clefs publiques ont été postées par des utilisateurs vérifiés. 

<h2>Ajouter la clef sur Smalakey</h2>
Si vous ne l'avez déjà fait, je vous invite à ajouter votre clefs sur le site afin que d'autres puissent la télécharger (cela n'engage en rien, si un inconnu quelconque s'empare de la clef, vous ne pourrez communquer que si vous avez ajouté la sienne.) Vous pouvez ajouter votre clef au site dès aujourd'hui <a href="{% url "upload_key" %}" > en cliquant ici. </a>

<h2>Ajouter un ami</h2>
Vous pouvez télécharger les clefs des autres utilisateurs sur le site "{% url "all_users_list" %}"

Une fois que vous avez une clef, cliquons sur "ajouter un ami"

</p>
<img src="{% static "tuto_images/ajouter_ami.png" %}" class="pure-img img_tuto" alt="ajouter_amis"/>
<p>
Puis faites entrer manuellement le certificat et cliquez sur suivant.

Il va falloir entrer la clef de votre ami dans le champ du bas.


</p>


<img src="{% static "tuto_images/certif_version_texte_rempli.png" %}" class="pure-img img_tuto" alt="certificat"/>

Validez et rock'n roll.


<p>
</p>

{% endblock %}
