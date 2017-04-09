{% extends "base.tpl" %}

{% block content %}
{% load staticfiles %}

    <h2>Partage</h2>
Le logiciel qui permet de partager une grande quantité de fichiers et de les mettre à disposition de vos amis. Vous pouvez aussi leur suggerer de télécharger tel ou tel fichier que vous avez sur votre disque. 

<h3>Mettre un répertoire en partage</h3>


Nous allons voir ici comment partager un répéertoire contenant les vidéos de nos dernières vacances. 

D'abors allez sur l'onglet "Partage de fichier"

<p>

Ensuite "Ajouter un partage"
</p>

<img src="{% static "tuto_images/ajouter_un_partage.png" %}" class="pure-img img_tuto" alt="gestionnaire_de_partage"/>
<p>
Ensuite sur "ajouter"

</p>
<img src="{% static "tuto_images/ajouyer_partage_fenetre.png" %}" class="pure-img img_tuto" alt="Modifier_les_dossiers_partagés"/>
<p>
Cliquez sur "Parcourir"

</p>
<h3>Gérer les permission</h3>

<img src="{% static "tuto_images/modif_dossier_partager(parcourir).png" %}" class="pure-img img_tuto" alt="parcourir"/>
<p>
Puis pour permettre a vos amis de télécharger le contenu directement cliquez sur le dossier bleu. (La petite bouille anonymous signifie que le fichiers n'est accessible que par un tunnel chiffré: vos amis peuvent le télécharger mais seuement en passant au travers d'un tunnel chiffré).

</p>
<img src="{% static "tuto_images/modif_dossier_partager(DROITS).png" %}" class="pure-img img_tuto" alt="modifier_les_droits"/>
<p>
Renouvelez autant de fois que vous avez de dossiers à partager (et de vidéos de vacances intéressantes). 


{% endblock %}
