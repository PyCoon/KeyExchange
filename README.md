KeyExchange
===================

KeyExchange est un projet d'application Web de partage de clefs publiques mais pas seulement. Il est destiné à encourager les utilisateurs novices à utiliser GPG et les logiciels l'utilisant.

----------

Retroshare
-------------

Initialement, le projet à été codé pour répondre à la problématique du partage de clefs Rétroshare par les nouveaux arrivant n'ayant jamais utilisé GPG. Un tutoriel est disponible détaillant l'installation et la configuration de Retroshare au sein du projet.

Invitation d'amis
-------------
Avec KeyExchange vous pouvez inviter vos amis à créer un compte et partager à leurs tour leurs clefs. Le serveur se charge d'envoyer le mail d'invitation pour peu que vous l'ayez configuré.

Déploiement
-------------

Le déploiement d'un projet Django peut se faire de diverses manières, je vous conseille les composants suivants:

 - Nginx pour servir les fichiers statiques.
 - Gunicorn est l'interface WSGI entre Python et Nginx qui lui envoi les requêtes qu’il ne peut traiter.
 - Supervisor pour gérer les services, et notamment les redémarrer automatiquement si besoin.
