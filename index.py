import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
workbook = load_workbook(filename = 'annuaire_avocats.xlsx')
sheet = workbook.active
# Envoyer une requête GET à la page principale de l'annuaire
# sheet.append(["nom", "telephone", "adresse", "code_postale", "ville", "site_web", "activités dominantes"])

for i in range(32):
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
        nom = ""
        adresse = ""
        code_postale = ""
        ville = ""
        site_web = ""
        tags = ""
        if contact_tag:
            if contact_tag.find("div").find("h3"):
                nom = contact_tag.find("div").find("h3").text.strip()
            if contact_tag.find("div").find(class_="addr"):
                adresse = contact_tag.find("div").find(class_="addr").text.strip()
            if contact_tag.find("div").find(class_="localite"):
                code_postale = contact_tag.find("div").find(class_="localite").text.strip()
            if contact_tag.find("div").find(class_="ville"):
                ville = contact_tag.find("div").find(class_="ville").text.strip()
            if contact_tag.find("div").find(class_="www"):
                site_web = contact_tag.find("div").find(class_="www").text.strip()
        if new_soup.find(class_="tag"):
            for tag in new_soup.find_all(class_="tag"):
                tags += tag.text.strip()
                tags += " - "
            # print(nom)
            # print(adresse)
            # print(code_postale)
            # print(ville)
            telephone = tel_tag.text.strip()
            sheet.append([nom, telephone, adresse, code_postale, ville, site_web, tags])
            # Extraire le numéro de téléphone

            # Faire quelque chose avec le numéro de téléphone (l'afficher, le sauvegarder, etc.)
            # print(telephone)
            # print("---")
        

workbook.save("annuaire_avocats.xlsx")
