# gene.py
# -*- coding: utf-8 -*-

"""
This script is a simple command-line interface for parsing and querying a GEDCOM file.
It allows users to list individuals, search by surname or name, and track birth places."
"""

import os

from gedcom.element.individual import IndividualElement

from geopy.geocoders import Nominatim
import folium
import time

from gedcom.parser import Parser
from dotenv import load_dotenv, dotenv_values 
from classes import myMenu, msg

"""
Funtions to interact with the GEDCOM file.
These functions allow users to list all individuals, find individuals by surname or name,
and track birth places.
"""
def list_all():
    """Function to list all individuals in the GEDCOM file."""
    msg.info("Listing all individuals:")
    count = 0
    # Iterate through all root child elements
    for element in root_child_elements:
        # Is the `element` an actual `IndividualElement`? (Allows usage of extra functions such as `surname_match` and `get_name`.)
        if isinstance(element, IndividualElement):
            # Unpack the name tuple
            (first, last) = element.get_name()
            # Print the first and last name of the individual
            print("({}) {} {}".format(count, first, last))
            count += 1

def find_individuals_by_surname():
    """Function to find individuals by surname in the GEDCOM file."""
    msg.info("Finding individuals by surname:")
    # Prompt the user for a surname
    surname = input("Enter the surname to search for: ").strip()
    if not surname:
        msg.error("No surname provided.")
        exit()
    # Iterate through all root child elements
    for element in root_child_elements:

        # Is the `element` an actual `IndividualElement`? (Allows usage of extra functions such as `surname_match` and `get_name`.)
        if isinstance(element, IndividualElement):
            if element.surname_match(surname):

                # Unpack the name tuple
                (first, last) = element.get_name()

                # Print the first and last name of the found individual
                print(first + " " + last)

def find_individuals_by_name():
    msg.info("Finding individuals by name:")
    # Prompt the user for a name
    name = input("Enter the name to search for: ").strip()
    if not name:
        msg.error("No name provided.")
        exit()
    # Iterate through all root child elements
    for element in root_child_elements:

        # Is the `element` an actual `IndividualElement`? (Allows usage of extra functions such as `surname_match` and `get_name`.)
        if isinstance(element, IndividualElement):
            if element.given_name_match(name):

                # Unpack the name tuple
                (first, last) = element.get_name()

                # Print the first and last name of the found individual
                print(first + " " + last)

def track_birth_places():
    # Track unique birth places
    msg.info("Tracking unique birth places:")
    # Get all unique birth places from the root child elements
    birth_places = set()
    # Iterate through all root child elements
    for element in root_child_elements:
        # Is the `element` an actual `IndividualElement`? (Allows usage of extra functions such as `surname_match` and `get_name`.)
        if isinstance(element, IndividualElement):
            # Get the birth place of the individual
            date,birth_place, source = element.get_birth_data()
            if birth_place:
                birth_place = birth_place.split(",")[0].strip().title()  # Take the first part of the birth place
                birth_places.add(birth_place)
    # Print all unique birth places
    if birth_places:
        print("Unique Birth Places:")
        for place in sorted(birth_places):
            print(place)
        return sorted(birth_places)
    else:
        msg.error("No birth places found.")
        return None

def geocoder_villes(lieux):
    geoloc = Nominatim(user_agent="gedcom_mapper")
    coords = {}

    for lieu in lieux:
        try:
            location = geoloc.geocode(lieu)
            if location:
                coords[lieu] = (location.latitude, location.longitude)
            else:
                print(f"⚠️ Lieu introuvable : {lieu}")
        except Exception as e:
            print(f"Erreur pour {lieu} : {e}")
        time.sleep(1)  # éviter de surcharger le service

    return coords

def creer_carte(coords, nom_fichier="carte_ancetres.html"):
    # Centrer la carte sur la France par défaut
    carte = folium.Map(location=[46.5, 2.5], zoom_start=5)

    for ville, (lat, lon) in coords.items():
        folium.Marker(location=[lat, lon], popup=ville).add_to(carte)

    carte.save(nom_fichier)
    print(f"✅ Carte enregistrée : {nom_fichier}")


def extraire_evenements(individus):

    data = []

    for elem in individus:
        if isinstance(elem, IndividualElement):
            nom = elem.get_name() or "Nom inconnu"
            parcours = []

            for child in elem.get_child_elements():
                tag = child.get_tag()
                if tag in ['BIRT', 'DEAT', 'MARR']:
                    date = None
                    lieu = None

                    for sub in child.get_child_elements():
                        if sub.get_tag() == 'DATE':
                            date = sub.get_value()
                        elif sub.get_tag() == 'PLAC':
                            lieu = sub.get_value()

                    if lieu:
                        parcours.append((tag, date, lieu.strip()))

            if parcours:
                data.append((nom, parcours))

    return data

def geocoder_lieux(liste_lieux):
    geoloc = Nominatim(user_agent="gedcom_migration_mapper")
    coords = {}
    for lieu in liste_lieux:
        try:
            if lieu not in coords:
                location = geoloc.geocode(lieu)
                if location:
                    coords[lieu] = (location.latitude, location.longitude)
                else:
                    print(f"⚠️ Lieu introuvable : {lieu}")
        except Exception as e:
            print(f"Erreur pour {lieu} : {e}")
        time.sleep(1)
    return coords

def creer_carte_migrations(data, coords, nom_fichier="migrations.html"):
    carte = folium.Map(location=[46.5, 2.5], zoom_start=5)

    for nom, parcours in data:
        points = []
        tooltip = f"<b>{nom}</b><br>"

        # Trier les événements par date si disponible
        parcours = sorted(parcours, key=lambda x: x[1] if x[1] else "")

        for evt_type, date, lieu in parcours:
            if lieu in coords:
                lat, lon = coords[lieu]
                points.append((lat, lon))
                tooltip += f"{evt_type} – {date or '?'} – {lieu}<br>"

        if len(points) >= 2:
            folium.PolyLine(points, color="blue", weight=2, opacity=0.7,
                            popup=folium.Popup(tooltip, max_width=300)).add_to(carte)

    carte.save(nom_fichier)
    print(f"✅ Carte de migration enregistrée : {nom_fichier}")


# loading variables from .env file
load_dotenv() 

# Path to your `.ged` file
file_path = os.getenv("GEDCOM_PATH")
if not file_path:
    raise ValueError("GEDCOM_PATH environment variable is not set.")
# Ensure the file exists
if not os.path.isfile(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

msg.title("Genepy: Genealogical Data Parsing")
msg.info(f"Parsing GEDCOM file: {file_path}")
# Initialize the parser
gedcom_parser = Parser()

# Parse your file
gedcom_parser.parse_file(file_path)

root_child_elements = gedcom_parser.get_root_child_elements()

choices = {
    "List all individuals": "List all individuals",
    "Find individuals by surname": "Find individuals by surname",
    "Find individuals by name": "Find individuals by name",
    "Find individuals by birth place": "Find individuals by birth place",
    "Create map of birth places": "Create a map of birth places",
    "Migration": "Track migration of individuals",
    "Exit": "Exit the program"
}

"""
For future developements (not implemented yet):
    "Find individuals by death place": "Find individuals by death place",
    "Find individuals by birth date": "Find individuals by birth date",
    "Find individuals by death date": "Find individuals by death date",
    "Find individuals by marriage date": "Find individuals by marriage date",
    "Find individuals by marriage place": "Find individuals by marriage place",
    "Find individuals by age": "Find individuals by age",
    "Find individuals by gender": "Find individuals by gender",
"""
while True:
    menu = myMenu("Main Menu", choices)
    rep = menu.show()
    # Check if the user wants to exit
    if rep == 0:
        msg.info("Exiting the program.")
        exit()
    # Check if the user wants to list all individuals
    if rep == 1:
        list_all()
    # Check if the user wants to find individuals by surname
    if rep == 2:
        find_individuals_by_surname()
    # Check if the user wants to find individuals by name
    if rep == 3:
        find_individuals_by_name()

    # Check if the user wants to find individuals by birth place
    if rep == 4:
        msg.info("Finding individuals by birth place:")
        # Prompt the user for a birth place
        birth_place = input("Enter the birth place to search for: ").strip()
        if not birth_place:
            msg.error("No birth place provided.")
            exit()
    if rep == 5:
        towns = track_birth_places()
        if towns:
            coords = geocoder_villes(towns)
            if coords:
                creer_carte(coords)
    # Check if the user wants to track migration of individuals
    if rep == 6:
        msg.info("Tracking migration of individuals:")
        # Extract events from the GEDCOM file
        data = extraire_evenements(root_child_elements)
        if not data:
            msg.error("No migration data found.")
            continue
        # Get unique places from the data
        lieux = set(lieu for _, parcours in data for _, _, lieu in parcours)
        coords = geocoder_lieux(lieux)
        if coords:
            creer_carte_migrations(data, coords)
