from flask import Blueprint, jsonify
import json
import os
import psycopg2
import psycopg2.extras
from pathlib import Path
from datetime import date
from app.controllers.Config import Config
from dotenv import load_dotenv


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/get/config/serveur')
def get_config_serveur():
    load_dotenv()
    # recupere le serveur
    statut = "failure"
    host = os.environ.get('HOST_SERVEUR')
    if host :
        statut = "success"

    return jsonify({"statut": statut, "result": host})

@api.route('/get/dalle')
def get_dalle():
    # récuparation chemin du json
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, "../static/json/grille_dalle.json")
    # list qui contiendra les dalles
    data = []
    try:
        print("ouverture du json")
        with open(file_path) as json_file:
            data = json.load(json_file)
        statut = "success"
    except:
        print("erreur dans la récuperation du json")
        statut = "failure"

    return jsonify({"statut": statut, "result": data})

@api.route('/get/chantiers/<float(signed=True):x_min>/<float(signed=True):y_min>/<float(signed=True):x_max>/<float(signed=True):y_max>', methods=['GET', 'POST'])
def get_chantier(x_min=None, y_min=None, x_max=None, y_max=None):
    load_dotenv()
    bdd = get_connexion_bdd()
    # si il n'y a aucun probleme avec la connexion à la base
    if bdd :
        #  on recupere les dalles qui sont dans la bbox envoyer
        bdd.execute(f"SELECT bloc, ST_AsGeoJson(st_transform(st_setsrid(geom_chantier, 2154),4326)) as polygon FROM {os.environ.get('SCHEMA_CHANTIER')} WHERE geom_chantier && ST_MakeEnvelope({x_min}, {y_min}, {x_max}, {y_max})")
        chantiers = bdd.fetchall()
        statut = "success"
        bdd.close()
        bdd.close() 
    else :
        statut = "erreur"
    return jsonify({"statut": statut, "result": chantiers})

@api.route('/get/dalles/<float(signed=True):x_min>/<float(signed=True):y_min>/<float(signed=True):x_max>/<float(signed=True):y_max>', methods=['GET', 'POST'])
def get_dalles(x_min=None, y_min=None, x_max=None, y_max=None):
    load_dotenv()
    bdd = get_connexion_bdd()
    # si il n'y a aucun probleme avec la connexion à la base
    if bdd :
        #  on recupere les dalles qui sont dans la bbox envoyer
        bdd.execute(f"SELECT id, nom, ST_AsGeoJson(st_setsrid(geom, 2154)) as polygon FROM {os.environ.get('SCHEMA_DALLE')} WHERE geom && ST_MakeEnvelope({x_min}, {y_min}, {x_max}, {y_max})")
        dalles = bdd.fetchall()
        dalles = get_coordonees(dalles)
        dalles = new_format_dalle(dalles)
        statut = "success"
        bdd.close()
        bdd.close() 
    else :
        statut = "erreur"
    return jsonify({"statut": statut, "result": dalles})



def get_connexion_bdd():
    """ Connexion à la base de données pour accéder aux dalles pcrs

    Returns:
        cursor: curseur pour executer des requetes à la base
    """
    try :
        load_dotenv()

        conn = psycopg2.connect(database=os.environ.get('PGDATABASE'), user=os.environ.get('PGUSER'), host=os.environ.get('PGHOST'), password=os.environ.get('PGPASSWORD'), port=os.environ.get('PGPORT'))
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    except psycopg2.OperationalError as e:
        return False
    return cur


def get_coordonees(dalles):
    """recupere les coordonnées des dalles dans le bon format

    Args:
        dalles (List): Liste des dalles avec leurs différentes infos en récuperer en base

    Returns:
        List: Liste des coordonnées des dalles 
    """
    SIZE = 1000
    coordonnées = []
    for dalle in dalles:
        # on recupere le x et le y
        polygon = json.loads(dalle["polygon"])["coordinates"][0][0]

        x = int(polygon[0])
        y = int(polygon[1])

        coordonnées.append({
            "id": dalle["id"],
            "x_min": x, 
            "x_max": x + SIZE, 
            "y_min": y - SIZE, 
            "y_max": y,
            "nom": dalle["nom"]
        })
    return coordonnées

def new_format_dalle(dalles):
    # creation du dictionnaire qui sera envoyer par l'api
    new_format_dalles = {
                            "date": str(date.today()),
                            "len_dalles": len(dalles),
                            "dalles": []
                            }
    # on insere le format que l'on veut des dalles dans le dictionnaire
    for dalle in dalles:
        new_format_dalles["dalles"].append(dalle)
    return dalles





