# gene.py
# -*- coding: utf-8 -*-

"""
This script is a simple command-line interface for parsing and querying a GEDCOM file.
It allows users to list individuals, search by surname or name, and track birth places."
"""

import os

from gedcom.element.individual import IndividualElement
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
    else:
        msg.error("No birth places found.")

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
    "Places": "Track Birth Places",
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
        track_birth_places()
