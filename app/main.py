import os
import csv


class GestionCSV:
    def __init__(self):
        self.fichiers = {}

    def ajouter_fichier(self, chemin: str):
        """Ajoute un fichier CSV à la gestion."""
        if os.path.exists(chemin):
            with open(chemin, mode="r", encoding="utf-8") as fichier:
                contenu = list(csv.reader(fichier))
                if contenu:
                    self.fichiers[chemin] = contenu
                    return True
        return False

    def recuperer_donnees(self, chemin: str):
        """Retourne les données d'un fichier donné."""
        if chemin in self.fichiers:
            return self.fichiers[chemin]
        return []

    def sauver_fichier(self, chemin: str, donnees: list):
        """Sauvegarde les données dans un fichier CSV."""
        with open(chemin, mode="w", newline="", encoding="utf-8") as fichier:
            ecrivain = csv.writer(fichier)
            ecrivain.writerows(donnees)

    def fusionner_fichiers(self, fichiers: list):
        """Fusionne plusieurs fichiers CSV dans une seule liste."""
        donnees_fusionnees = []
        en_tete = None
        for fichier in fichiers:
            if fichier in self.fichiers:
                contenu = self.fichiers[fichier]
                if en_tete is None:
                    en_tete = contenu[0]
                donnees_fusionnees.extend(contenu[1:])
        return [en_tete] + donnees_fusionnees if en_tete else []

    def trier_par_colonne(self, chemin: str, numero_colonne: int):
        """Trie les données d'un fichier selon une colonne spécifiée."""
        donnees = self.recuperer_donnees(chemin)
        if donnees:
            try:
                # Trier les données en fonction de la colonne
                # (en excluant l'en-tête)
                return [donnees[0]] + sorted(
                    donnees[1:], key=lambda x: x[numero_colonne]
                )
            except IndexError:
                print(f"Colonne {numero_colonne} invalide.")
                return []
        return []


class Affichage:
    def afficher_tableau(donnees: list):
        """Affiche un tableau à partir des données
        avec ':' comme séparateur et colonnes alignées."""
        if not donnees:
            return

        # Calculer la largeur maximale de chaque colonne
        colonnes_largeur = [
            max(len(str(item)) for item in colonne) for colonne in zip(
                *donnees)
        ]

        # Afficher les données ligne par ligne avec les colonnes alignées
        for ligne in donnees:
            print(
                " | ".join(
                    f"{str(cellule).ljust(colonnes_largeur[i])}"
                    for i, cellule in enumerate(ligne)
                )
            )
            print(
                "-" * (sum(colonnes_largeur) + len(colonnes_largeur) - 1)
            )  # Ligne de séparation


class Commandes:
    def __init__(self):
        self.gestionnaire_csv = GestionCSV()

    def lister_fichiers_csv(self):
        """Retourne une liste des fichiers CSV importés."""
        return list(self.gestionnaire_csv.fichiers.keys())

    def executer_importer(self):
        """Exécute l'importation d'un fichier
        CSV depuis le répertoire courant."""
        fichiers_disponibles = [f for f in os.listdir() if f.endswith(".csv")]
        if not fichiers_disponibles:
            print("Aucun fichier CSV trouvé dans le répertoire courant.")
            return False

        print("Fichiers CSV disponibles dans le répertoire courant :")
        for idx, fichier in enumerate(fichiers_disponibles, 1):
            print(f"{idx}. {fichier}")

        choix = input("Choisissez un fichier à importer (par numéro) : ")
        try:
            fichier_choisi = fichiers_disponibles[int(choix) - 1]
            if self.gestionnaire_csv.ajouter_fichier(fichier_choisi):
                print(f"Fichier {fichier_choisi} importé avec succès.")
                return True
            else:
                print(f"Erreur : fichier {fichier_choisi} non importé.")
                return False
        except (ValueError, IndexError):
            print("Choix invalide.")
            return False

    def executer_afficher(self):
        """Affiche les fichiers CSV déjà importés."""
        fichiers_importes = self.lister_fichiers_csv()
        if not fichiers_importes:
            print("Aucun fichier importé.")
            return

        print("Fichiers CSV importés :")
        for idx, chemin in enumerate(fichiers_importes, 1):
            print(f"{idx}. {chemin}")

        choix = input("Choisissez un fichier à afficher (par numéro) : ")
        try:
            fichier_choisi = fichiers_importes[int(choix) - 1]
            donnees = self.gestionnaire_csv.recuperer_donnees(fichier_choisi)
            Affichage.afficher_tableau(donnees)
        except (ValueError, IndexError):
            print("Choix invalide.")

    def executer_fusionner(self):
        """Fusionne plusieurs fichiers CSV importés."""
        fichiers_importes = self.lister_fichiers_csv()
        if not fichiers_importes:
            print("Aucun fichier importé.")
            return

        print("Fichiers CSV importés :")
        for idx, fichier in enumerate(fichiers_importes, 1):
            print(f"{idx}. {fichier}")

        choix = input(
            "Choisissez les fichiers à fusionner"
            "(séparés par des espaces, par numéro) : "
        )
        try:
            fichiers_choisis = [
                fichiers_importes[int(i) - 1] for i in choix.split()
            ]
            donnees_fusionnees = self.gestionnaire_csv.fusionner_fichiers(
                fichiers_choisis
            )
            if donnees_fusionnees:
                Affichage.afficher_tableau(donnees_fusionnees)

                # Demander si l'utilisateur veut enregistrer
                enregistrer = (
                    input(
                        "Voulez-vous enregistrer ce fichier fusionné ?"
                        "(oui/non) : "
                    )
                    .strip()
                    .lower()
                )

                if enregistrer == "oui":
                    # Demander un nom pour le fichier fusionné
                    nom_fichier = input(
                        "Entrez le nom du fichier fusionné (sans extension) : "
                    )
                    chemin_fusionne = f"{nom_fichier}.csv"
                    self.gestionnaire_csv.sauver_fichier(
                        chemin_fusionne, donnees_fusionnees
                    )
                    print(f"Fichier sauvegardé sous {chemin_fusionne}.")
                else:
                    print("Le fichier fusionné n'a pas été sauvegardé.")
            else:
                print("Erreur lors de la fusion des fichiers.")
        except (ValueError, IndexError):
            print("Choix invalide.")

    def executer_trier(self):
        """Trie les données d'un fichier CSV importé selon une colonne."""
        fichiers_importes = self.lister_fichiers_csv()
        if not fichiers_importes:
            print("Aucun fichier importé.")
            return

        print("Fichiers CSV importés :")
        for idx, fichier in enumerate(fichiers_importes, 1):
            print(f"{idx}. {fichier}")

        choix = input("Choisissez un fichier à trier (par numéro) : ")
        try:
            fichier_choisi = fichiers_importes[int(choix) - 1]
            chemin = fichier_choisi
            donnees = self.gestionnaire_csv.recuperer_donnees(chemin)
            en_tete = donnees[0]  # En-tête du fichier
            print("Colonnes disponibles :")
            for i, colonne in enumerate(en_tete):
                print(f"{i + 1}. {colonne}")
            # Demander à l'utilisateur de choisir la colonne par numéro
            numero_colonne = (
                int(input("Entrez le numéro de la colonne pour trier : ")) - 1
            )
            donnees_triees = self.gestionnaire_csv.trier_par_colonne(
                chemin, numero_colonne
            )
            if donnees_triees:
                Affichage.afficher_tableau(donnees_triees)
            else:
                print(
                    f"Erreur lors du tri de la colonne {numero_colonne + 1}."
                )
        except (ValueError, IndexError):
            print("Choix invalide.")


class InterfaceUtilisateur:
    def __init__(self):
        self.commandes = Commandes()

    def menu(self):
        """Affiche le menu de l'interface utilisateur."""
        while True:
            print("\nMenu :")
            print("1. Importer un fichier CSV")
            print("2. Afficher un fichier CSV")
            print("3. Fusionner des fichiers CSV")
            print("4. Trier un fichier CSV")
            print("5. Quitter")
            choix = input("Choisissez une option : ")

            if choix == "1":
                self.commandes.executer_importer()
            elif choix == "2":
                self.commandes.executer_afficher()
            elif choix == "3":
                self.commandes.executer_fusionner()
            elif choix == "4":
                self.commandes.executer_trier()
            elif choix == "5":
                print("Au revoir !")
                break
            else:
                print("Choix invalide. Essayez à nouveau.")


if __name__ == "__main__":
    interface = InterfaceUtilisateur()
    interface.menu()
