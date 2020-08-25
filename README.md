# You can start the automatism by:
source venv/bin/activate
nohup python autoschedule.py &

#### Configurer un raspberry pi ####

1/ Copier autopython dans un dossier qu’on appellera "." (ou git pull)
2/ Créer un fichier ./RPD_ID. Ce sera l’identité du raspberry pi qui peut être "entry", "ring"
3/ virtualenv, activer, installer les requirements.txt
4/ Automatiser le lancement de ./AUTOPYTHON/run.py avec le virtualenv.