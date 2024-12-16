import os
import csv
import argparse
import cmd


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
        return self.fichiers.get(chemin, [])

    def afficher_tableau(self, donnees: list):
        """Affiche un tableau des données."""
        if not donnees:
            print("Aucune donnée à afficher.")
            return

        colonnes_largeur = [
            max(len(str(cell)) for cell in col) for col in zip(*donnees)
        ]
        for ligne in donnees:
            print(
                " | ".join(
                    f"{cell.ljust(colonnes_largeur[i])}"
                    for i, cell in enumerate(ligne)
                )
            )

    def trier_par_colonne(self, chemin: str, numero_colonne: int):
        """Trie les données d'un fichier CSV par une colonne donnée."""
        donnees = self.recuperer_donnees(chemin)
        if not donnees:
            print(f"Aucune donnée trouvée pour le fichier {chemin}")
            return []
        try:
            return [donnees[0]] + sorted(
                donnees[1:], key=lambda x: x[numero_colonne]
            )
        except IndexError:
            print("Numéro de colonne invalide.")
            return []


class InterfaceInteractif(cmd.Cmd):
    intro = (
        "Bienvenue dans le gestionnaire CSV interactif. Tapez 'help' pour "
        "voir les commandes disponibles.\n"
    )
    prompt = "(csv) "

    def __init__(self, gestion_csv):
        super().__init__()
        self.gestion_csv = gestion_csv
        self.fichier_actuel = None

    def do_importer(self, chemin):
        """Importer un fichier CSV. Exemple: importer fichier.csv"""
        if self.gestion_csv.ajouter_fichier(chemin):
            print(f"Fichier {chemin} importé avec succès.")
            self.fichier_actuel = chemin
        else:
            print(f"Erreur : impossible d'importer {chemin}.")

    def do_afficher(self, arg):
        """Afficher le contenu d'un fichier CSV importé."""
        if self.fichier_actuel:
            donnees = self.gestion_csv.recuperer_donnees(self.fichier_actuel)
            self.gestion_csv.afficher_tableau(donnees)
        else:
            print("Aucun fichier sélectionné. "
                  "Importez un fichier avec 'importer'.")

    def do_trier(self, numero_colonne):
        """Trier les données par une colonne. Exemple: trier 1"""
        if self.fichier_actuel:
            try:
                numero_colonne = int(numero_colonne)
                donnees_tries = self.gestion_csv.trier_par_colonne(
                    self.fichier_actuel, numero_colonne
                )
                self.gestion_csv.afficher_tableau(donnees_tries)
            except ValueError:
                print("Veuillez entrer un numéro de colonne valide.")
        else:
            print("Aucun fichier sélectionné. Importez un "
                  "fichier avec 'importer'.")

    def do_lister(self, arg):
        """Lister les fichiers CSV disponibles dans le répertoire courant."""
        fichiers = [f for f in os.listdir() if f.endswith(".csv")]
        if fichiers:
            print("Fichiers CSV disponibles :")
            for fichier in fichiers:
                print(f"- {fichier}")
        else:
            print("Aucun fichier CSV trouvé dans le répertoire courant.")

    def do_quitter(self, arg):
        """Quitter le programme."""
        print("Au revoir !")
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Gestionnaire CSV interactif."
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Lancer le programme en mode interactif.",
    )

    args = parser.parse_args()

    gestion_csv = GestionCSV()

    if args.interactive:
        InterfaceInteractif(gestion_csv).cmdloop()
    else:
        print("Utilisez --interactive pour démarrer le programme.")


if __name__ == "__main__":
    main()
