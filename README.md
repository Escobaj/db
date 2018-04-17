# Rendu de l'equipe 10 pour le cours GLO-2005

vous trouverez dans ce depot :
- Les sources du projet de cours
- Un dump de la base de donnée finale, avec ses données
- Le rapport

## Instruction (sous windows)

1 - Pour lancer le projet vous devez créer une base de données <br>

`mysql -u root -p -e "create database 'db'"`

2 - Importer le fichier `dump.sql` <br>

`mysql -u root -p db < dump.sql`

3 - Mettre a jour les informations de connection

`pymysql.connect(host='localhost',
	                       user='root',
	                       password='password',
	                       db='db')`

4 - Le projet contient un executable python pour le lancer si vous ne l'avez pas sur le systeme<br>

>`>venv\Scripts\python.exe db.py`

Si tout s'est déroulé correctement vous devriez voir :  `* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)` <br>
Vous pouvez alors accéder au site [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Architecture
logique affaire : **app/controllers/*** <br>
logique base de donnée : **app/models/*** <br>
logique client : **templates/*** <br>
fichier racine: **db.py**

## Contact 
En cas de problème pour lancer le projet, vous pouvez contacter Joffrey Escobar, qui s’est occupé du fonctionnel du site à l’adresse : joffrey.escobar.1@ulaval.ca