import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
workbook = Workbook()
sheet = workbook.active
# Envoyer une requête GET à la page principale de l'annuaire
for i in range(31):
    url = "https://www.barreaudeladrome.fr/annuaire-des-avocats/page/{}/".format(i)
    print(url)
    response = requests.get(url)

    # Analyser le contenu HTML de la page
    soup = BeautifulSoup(response.content, "html.parser")

    # Trouver toutes les balises avec la classe "more"
    more_tags = soup.find_all(class_="more")

    

    # Parcourir chaque balise "more" pour extraire les numéros de téléphone
    for tag in more_tags:
        # Extraire le lien href de l'élément enfant <a>
        href = tag.find("a")["href"]

        # Visiter la nouvelle page en utilisant le lien href
        new_response = requests.get(href)
        new_soup = BeautifulSoup(new_response.content, "html.parser")

        # Trouver la balise avec la classe "tel"
        tel_tag = new_soup.find(class_="tel")
        contact_tag = new_soup.find(class_="contact")

        if contact_tag:
            nom = contact_tag.find("div").find("h3").text.strip()
            adresse = contact_tag.find("div").find(class_="addr").text.strip()
            code_postale = contact_tag.find("div").find(class_="localite").text.strip()
            ville = contact_tag.find("div").find(class_="ville").text.strip()
            # print(nom)
            # print(adresse)
            # print(code_postale)
            # print(ville)
            telephone = tel_tag.text.strip()
            sheet.append([nom, telephone, adresse, code_postale, ville])
            # Extraire le numéro de téléphone

            # Faire quelque chose avec le numéro de téléphone (l'afficher, le sauvegarder, etc.)
            # print(telephone)
            # print("---")
        

workbook.save("annuaire_avocats.xlsx")
