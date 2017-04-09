{% extends "base.tpl" %}

{% block content %}
{% load staticfiles %}
<article>
    <h2>Installation</h2>
<p>
    Téléchargez d'abord l'installateur correspondant au système d'exploitation que vous utilisez:</br>
    <h3>Téléchargement</h3>
    <ul>
    Windows: 
    <li><a href="http://sourceforge.net/projects/retroshare/files/RetroShare/0.6.0-rc2/RetroShare_0.6.0_8551_rc2_setup.exe/download" > Retroshare Windows amd64/i386 </a></li> 


    Mac:
    <li><a href="https://github.com/RetroShare/RetroShare/releases/download/v0.6.0-RC2/RetroShare06-RC2.dmg.zip" > Retroshare Mac </a></li>


    Sources:
    <li><a href="http://sourceforge.net/projects/retroshare/files/RetroShare/0.6.0-rc2/retroshare_0.6.0.RC2~8551_src.tgz/download" >Sources à compiler sois même </a></li>


    </ul>

    L'installation ne devrait pas poser de problème, vous pouvez cliquer sur suivant sans craindre d'installer un pourriciel par mégarde.
    
    <h3>Configuration de l'installation</h3>

    Nous vous conseillons de laisser l'installation standard (et non la portable) et de garder cochée la case démarrage automatique.

    Créez ensuite un compte : le nom du nœud importe peu, « Maison » est un bon nom pour un nœud. Cette opération permet de s'y retrouver dans le cas d'une installation sur plusieurs machines. 

</p>

    <h2>Configuration</h2>


    <p>
    <h3>Première connection</h3>
      Vous voilà devant l'écran de connexion de Retroshare, il est important de cocher la case "se rappeller du mot de passe" ou Retroshare ne pourra pas démarrer tout seul et donc partager les fichiers.
    </p>

<img src="{% static "tuto_images/se_connecter.png" %}" class="pure-img img_tuto" alt="se_connecter"/>

      <p>
<h3>Dossier de réception</h3>

      D'abord configurez le dossier destiné à recevoir les fichiers téléchargés.

      Pour cela cliquez sur l’icône "Option" en forme d'écrou.
  </p>
      <img src="{% static "tuto_images/retroshare_option(option).png" %}" class="pure-img img_tuto" alt="Menu_d_option"/>
<p>

      Rendez-vous ensuite dans l'onglet « Dossiers » puis cliquez sur la petite loupe. Choisissez le dossier dans lequel les fichiers que vous téléchargerez  atterriront. Je vous conseille de créer un dossier dédié sur le bureau.
</p>
      <img src="{% static "tuto_images/option_dossier_cible(parcourir).png" %}" class="pure-img img_tuto" alt="dossier_cible"/>
<p>

</article>

      {% endblock %}


