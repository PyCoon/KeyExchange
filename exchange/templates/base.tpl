<!doctype html>
<html class="no-js" lang="FR">

    <head>

        <meta charset="utf-8">
        <title>Smala Key Exchange</title>
        <meta name="description" content="Site de partage de clefs autour de Retroshare.">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        {% load staticfiles %}

<link rel="shortcut icon" type="image/png" href="{% static "img/favicon.ico" %}"/>
                <link rel="stylesheet" type="text/css" href="{% static "css/pure.css" %}" />
                <link rel="stylesheet" type="text/css" href="{% static "css/style_sheet.css" %}" />
                <script type="text/javascript" src="{% static "js/jquery-2.1.4.js" %}" ></script>
                
    </head>

    <body>

        <header>

      
</br>
            <div class="pure-g">
                <div class="pure-u-1-4">
                </div>
                <div class="pure-u-1-2">
                                             <aside id="connect_with">
  Bonjour {{ request.user.username|default:"étranger" }}</aside> 
                     <a href="{% url 'front_page' %}" class=" nomenu pure-menu-link">   <img id="logo" src="{% static "img/logo.png" %}" class="pure-img" alt="SmalaKey" /> </a>
                         </div> 
                          </div>  
                           
                           
           
            <div class="pure-g main-navbar">   
 <div class="pure-u-1-4">
                </div>     
    
        <div class="pure-u-1-2">

                    <nav class="pure-menu pure-menu-horizontal">
                        <ul class="pure-menu-list nomenu">

                            <li class="pure-menu-item pure-menu-selected"><a href="{% url 'all_users_list' %}" class=" nomenu pure-menu-link">LISTE DES UTILISATEURS</a></li>
                            
    <li class="pure-menu-item pure-menu-selected"><a href="{% url 'create_invitation' %}" class=" nomenu pure-menu-link">INVITER UN AMI</a></li>
    
 <li class="pure-menu-item"><a href="{% url 'upload_key' %}" class="nomenu pure-menu-link">VERSER UNE CLEF</a></li>

                                <li class="pure-menu-item pure-menu-has-children pure-menu-allow-hover">
                                <a href="{% url 'tutoriels' %}"  class="nomenu pure-menu-link">TUTOS</a>
                                <ul class="pure-menu-children">
                                <li class="pure-menu-item"><a href="{% url 'installation' %}" class="nomenu pure-menu-link">1. INSTALLER</a></li>
                                    <li class="pure-menu-item"><a href="{% url 'ajouter_ami' %}" class="nomenu pure-menu-link">2. AJOUTER DES AMIS</a></li>
                                    <li class="pure-menu-item"><a href="{% url 'partager' %}" class="nomenu pure-menu-link">3. PARTAGER</a></li>

                                </ul>
                            </li>
                            
                  </li>


                  <li class="pure-menu-item pure-menu-has-children pure-menu-allow-hover account_logo"  >
                 <a href="{% url 'account_detail' %}"  class="nomenu pure-menu-link"> <img  class="pure-img" id="account_logo" src="{% static "img/my account_key2.png" %}" alt="TABLEAU DE BORD"><div id="notif" >DASHBOARD{% if request.session.notifications > 0 %}{{request.session.notifications}} Notifications !{% endif %} </a> </div> </a>
                   <ul class="pure-menu-children">
                                    
                                    <li class="pure-menu-item"><a href="{% url 'account_detail' %}" class="nomenu pure-menu-link">MON COMPTE</a></li>
                                    <li class="pure-menu-item"><a href="{% url 'change_pass_view' %}" class="nomenu pure-menu-link">CHANGER MON MOT DE PASSE</a></li>
                                    <li class="pure-menu-item"><a href="{% url 'login_user' %}" class="nomenu pure-menu-link">CONNEXION AVEC UN AUTRE COMPTE</a></li>
                                    <li class="pure-menu-item"><a href="{% url 'logout_view' %}" class="nomenu pure-menu-link">DECONNEXION</a></li></ul>
                  </li>
                       </ul> 
                         </nav>


   </div>                
</div>

            <div class="hr"></div>
        </header>

        <div class="pure-g">
           <div class="pure-u-1-4">
            </div>


            <div class="pure-u-1-2">
            
            <section>
                                        <div class="login_session">

            </div>
{% block content %}
{% endblock %}


            </section>
<footer> Nono copyright, tout droits réservés. </footer>
        </div>

            <div class="pure-g">
                <div class="pure-u-1-4">
                
                </div>
                
                <div class="pure-u-1-2">
                                            
                         </div> 
                          </div>  
                           
                           
           

    </body>

</html>
