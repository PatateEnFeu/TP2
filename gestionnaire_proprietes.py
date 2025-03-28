"""
Ce module est responsable de la gestion des propriétés dans l'application IFT-1004 Solo Immo,
incluant l'ajout de nouvelles propriétés, la liste et le filtrage des propriétés disponibles.

Fonctions:
- `lister_proprietes()`: Liste toutes les propriétés disponibles.
- `filtrer_proprietes()`: Filtre les propriétés en fonction des critères de l'utilisateur.
- `ajouter_propriete()`: Ajoute une nouvelle propriété si l'utilisateur est connecté.

Dépendances:
- `gestionnaire_donnees`: Pour lire et écrire dans le fichier des propriétés.
- `gestionnaire_utilisateurs`: Pour vérifier si un utilisateur est connecté.
- `utilitaires`: Pour des fonctions auxiliaires comme l'affichage de tableaux formatés,
et le formatage de montants en dollars.
"""

from gestionnaire_donnees import charger_proprietes, sauvegarder_propriete
from gestionnaire_utilisateurs import utilisateur_est_connecte
from utilitaires import afficher_tableau, formater_argent


TYPES_DE_PROPRIETE = ["Maison", "Appartement", "Condo", "Loft"]
VILLES = ["Québec", "Montréal", "Toronto", "Ottawa"]


def lister_proprietes():
    """Affiche la liste de toutes les propriétés disponibles sous forme de tableau.

    Cette fonction suit les étapes suivantes :
      1. Charge les propriétés à partir du fichier de données via la fonction `charger_proprietes`.
      2. Si aucune propriété n'est disponible, affiche un message indiquant "Aucune propriété disponible".
      3. Si des propriétés sont disponibles, formate chaque propriété en une ligne de tableau avec les colonnes suivantes :
         - Prix : formaté en devise grâce à `formater_argent`.
         - Ville : ville où se situe la propriété.
         - Type de propriété : type (par exemple, Maison, Condo).
         - Chambres : nombre de chambres.
         - Salles de bains : nombre de salles de bains.

    Les informations sont ensuite affichées dans un tableau formaté avec une ligne d'en-tête descriptive.

    Affiche un message approprié si aucune propriété n'est disponible.
    """
    # TODO
    list_of_list = []
    sous_liste = []
    list_prop = charger_proprietes()

    for valeur in list_prop:
        sous_liste = [
            formater_argent(valeur["prix"]),
            valeur["ville"],
            valeur["type"],
            valeur["chambres"],
            valeur["salles_de_bains"]
        ]

        list_of_list.append(sous_liste)

    if list_prop :
        afficher_tableau(list_of_list,["Prix","Ville","Type de propriété","Chambres","Salles de bains"])

    else :
        print("Aucune propriété disponible")



def filtrer_proprietes():
    """Filtre les propriétés disponibles selon les critères définis par l'utilisateur.

    Cette fonction permet de rechercher des propriétés en appliquant des filtres basés sur les critères suivants :
      1. Prix (minimum et maximum)
      2. Ville
      3. Type de propriété (ex. Maison, Condo)
      4. Nombre de chambres
      5. Nombre de salles de bains
      6. Combinaison de plusieurs de ces critères

    Processus de filtrage :
      - Affiche un menu permettant à l'utilisateur de sélectionner un critère de filtrage unique
        ou une combinaison de critères.
      - En fonction de l'option choisie, invite l'utilisateur à entrer les valeurs de filtrage.
      - Applique les critères pour trouver les propriétés correspondantes.

    Affichage :
      - Si des propriétés correspondant aux critères sont trouvées, elles sont affichées sous forme de tableau
        avec les colonnes : Prix, Ville, Type de propriété, Chambres, et Salles de bains.
      - Si aucune propriété ne correspond, un message indique qu'aucune propriété n'est disponible.
    """
    # TODO
    continuer = True 
    list_prop = charger_proprietes()
    list_of_list = []
    sous_liste = []
    list_of_list_spec = []


    for valeur in list_prop:
        sous_liste = [
            valeur["prix"],
            valeur["ville"],
            valeur["type"],
            valeur["chambres"],
            valeur["salles_de_bains"]
        ]

        list_of_list.append(sous_liste)

    while continuer:
        print("1. Filtrer par prix")
        print("2. Filtrer par ville")
        print("3. Filtrer par type de propriété")
        print("4. Filtrer par nombre de chambres")
        print("5. Filtrer par salles de bains")
        print("6. Filtrer par une combinaison des options")

        
        try:
            choix = int(input('Choisissez une option de filtrage: '))

            if 1 <= choix <= 6:
                
                if choix == 1 :
                    list_of_list_spec = []

                    prix = demander_plage_de_prix()

                    if prix[0] == None and prix[1] == None : # Cas aucun prix défini
                        list_of_list_spec = list_of_list.copy()

                    elif prix[0] == None and prix[1] >= 0 : # Cas du prix maximum seulement
                        for sous_liste_spec in list_of_list :
                            if sous_liste_spec[0] <= prix[1] :
                                list_of_list_spec.append(sous_liste_spec)

                    elif prix[0] >= 0 and prix[1] == None : # Cas du prix minimum seulement
                        for sous_liste_spec in list_of_list :
                            if sous_liste_spec[0] >= prix[0] :
                                list_of_list_spec.append(sous_liste_spec)

                
                elif choix == 2 :

                    ville = demander_ville()
                    for sous_liste_spec in list_of_list :
                        if sous_liste_spec[1] == ville :
                            list_of_list_spec.append(sous_liste_spec)


                elif choix == 3 :

                    prop = demander_type_de_propriete()
                    for sous_liste_spec in list_of_list :
                        if sous_liste_spec[2] == prop :
                            list_of_list_spec.append(sous_liste_spec)
                
                
                elif choix == 4 :
                    continuer_chamb = True
                    while continuer_chamb :
                        try:
                            nbr_chambres = int(input("Nombres de chambres: "))
                            for sous_liste_spec in list_of_list :
                                if sous_liste_spec[3] == nbr_chambres:
                                    list_of_list_spec.append(sous_liste_spec)
                            
                            if not list_of_list_spec:
                                print("Il n'y a aucune propriété avec ce nombre de chambres")

                            continuer_chamb = False

                        except ValueError :
                            print("Entrez un nombre valide")
                        


                elif choix == 5 :

                    continuer_sdb = True
                    while continuer_sdb:
                        try:
                            nbr_sdb = int(input("Nombres de salles de bains: "))
                            for sous_liste_spec in list_of_list :
                                if sous_liste_spec[4] == nbr_sdb:
                                    list_of_list_spec.append(sous_liste_spec)
                            if not list_of_list_spec:
                                print("Il n'y a aucune propriété avec ce nombre de salles de bains ")

                            continuer_sdb = False

                        except ValueError:
                            print("Entrez un nombre valide")

   
                
                elif choix == 6 :

                    prix = demander_plage_de_prix()
                    if prix[0] == None and prix[1] == None : # Cas aucun prix défini
                        list_of_list_spec = list_of_list.copy()

                    elif prix[0] == None and prix[1] >= 0 : # Cas du prix maximum seulement
                        for sous_liste_spec in list_of_list :
                            if sous_liste_spec[0] <= prix[1] :
                                list_of_list_spec.append(sous_liste_spec)

                    elif prix[0] >= 0 and prix[1] == None : # Cas du prix minimum seulement
                        for sous_liste_spec in list_of_list :
                            if sous_liste_spec[0] >= prix[0] :
                                list_of_list_spec.append(sous_liste_spec)



                    ville = input("Choisissez une ville parmi les suivantes: Québec, Montréal, Toronto, Vancouver, Ottawa:")
                    for sous_liste_spec in list_of_list :
                        if sous_liste_spec[1] == ville :
                            list_of_list_spec.append(sous_liste_spec)
                    

                    prop = input("Choisissez un type de propriété parmi les suivants: Maison, Appartement, Condo, Loft:")
                    for sous_liste_spec in list_of_list :
                        if sous_liste_spec[2] == prop :
                            list_of_list_spec.append(sous_liste_spec)

                    
                    nbr_chambres = input("Nombres de chambres: ")
                    for sous_liste_spec in list_of_list :
                        if sous_liste_spec[3] == nbr_chambres:
                            list_of_list_spec.append(sous_liste_spec)


                    nbr_sdb = input("Nombres de salles de bains: ")
                    for sous_liste_spec in list_of_list :
                        if sous_liste_spec[4] == nbr_sdb:
                            list_of_list_spec.append(sous_liste_spec)


                continuer = False

            else :
                print("Choix invalide. Entrez une option parmi celles proposées")

        except ValueError :
            print("Entrez une nombre entre 1 et 6")

    for valeur in list_of_list_spec:
        valeur[0] = formater_argent(valeur[0])
        
    afficher_tableau(list_of_list_spec,["Prix","Ville","Type de propriété","Chambres","Salles de bains"])
        

    

    

VILLES = ["Québec", "Montréal", "Toronto", "Vancouver", "Ottawa"]
TYPES_DE_PROPRIETE = ["Maison", "Appartement", "Condo","Loft"]
def ajouter_propriete():
    """Ajoute une nouvelle propriété à la liste des propriétés, si l'utilisateur est connecté.

    Cette fonction suit les étapes suivantes :
      1. Vérifie si un utilisateur est connecté en appelant `utilisateur_est_connecte`.
         Si aucun utilisateur n'est connecté, affiche un message d'erreur et interrompt le processus.
      2. Demande les informations détaillées de la propriété à ajouter, en incluant :
         - Prix (valeur positive)
         - Ville
         - Type de propriété (par exemple, Maison, Condo)
         - Nombre de chambres (valeur positive)
         - Nombre de salles de bains (valeur positive)
      3. Enregistre les informations de la nouvelle propriété dans le fichier de propriétés via la fonction `sauvegarder_propriete`.

    Affiche un message de confirmation une fois la propriété ajoutée, ou un message d'erreur si l'utilisateur n'est pas connecté.
    """
    # TODO
    connected = utilisateur_est_connecte()
    info_prop = {}
    if connected:
        prix = demander_nombre_positif("Entrez le prix")
        ville = demander_ville()
        Type_prop = demander_type_de_propriete()
        nbr_chamb = demander_nombre_positif("Entrez le nombre de chambres")
        nbr_sdb = demander_nombre_positif("Entrez un nombre de salles de bains")
   
        info_prop = {
            "prix": prix,
            "ville": ville,
            "type" : Type_prop,
            "chambres": nbr_chamb,
            "salles_de_bains": nbr_sdb
        }
        sauvegarder_propriete(info_prop)

    else:
        print("L'utilisateur n'est pas connecté, vous ne pouvez pas ajouter de propriété")
    



def demander_plage_de_prix(optionnel=False):
    """Demande à l'utilisateur de saisir une plage de prix.

    Args:
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        tuple: (prix_minimum, prix_maximum)
    """
    while True:
        try:
            prix_minimum = input("Prix minimum: ")
            prix_maximum = input("Prix maximum: ")
            if optionnel and not prix_minimum and not prix_maximum:
                return None, None
            prix_minimum = int(prix_minimum) if prix_minimum else None
            prix_maximum = int(prix_maximum) if prix_maximum else None
            if (
                prix_minimum is not None
                and prix_maximum is not None
                and prix_minimum > prix_maximum
            ):
                raise ValueError(
                    "Le prix minimum doit être inférieur ou égal au prix maximum."
                )
            return prix_minimum, prix_maximum
        except ValueError as e:
            print(e)


def demander_ville(optionnel=False):
    """Demande à l'utilisateur de choisir une ville parmi les choix définis.

    Args:
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        str: La ville choisie.
    """
    print(f"Choisissez une ville parmi les suivantes: {', '.join(VILLES)}")
    while True:
        ville = input("Ville: ").capitalize()
        if optionnel and not ville:
            return None
        if ville in VILLES:
            return ville
        print(f"Ville invalide. Choisissez parmi: {', '.join(VILLES)}")


def demander_type_de_propriete(optionnel=False):
    """Demande à l'utilisateur de choisir un type de propriété parmi les choix définis.

    Args:
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        str: Le type de propriété choisi.
    """
    print(
        f"Choisissez un type de propriété parmi les suivants: {', '.join(TYPES_DE_PROPRIETE)}"
    )
    while True:
        type_de_propriete = input("Type de propriété: ").capitalize()
        if optionnel and not type_de_propriete:
            return None
        if type_de_propriete in TYPES_DE_PROPRIETE:
            return type_de_propriete
        print(
            f"Type de propriété invalide. Choisissez parmi: {', '.join(TYPES_DE_PROPRIETE)}"
        )


def demander_nombre_positif(prompt, optionnel=False):
    """Demande à l'utilisateur de saisir un nombre positif.

    Args:
        prompt (str): Le message à afficher pour la saisie.
        optionnel (bool): Indique si la saisie est facultative.

    Returns:
        int: Le nombre saisi, qui sera positif.
    """
    while True:
        nombre = input(f"{prompt}: ")
        if optionnel and not nombre:
            return None
        try:
            nombre = int(nombre)
            if nombre > 0:
                return nombre
            else:
                print("Veuillez saisir un nombre positif.")
        except ValueError:
            print("Valeur invalide. Veuillez saisir un nombre.")
