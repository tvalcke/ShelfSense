# tests écrits avec chat gpt

import unittest
import os
from main import GestionCSV


class TestGestionCSV(unittest.TestCase):

    def setUp(self):
        """Crée des csv avant les tests"""
        self.file1 = "test1.csv"
        self.file2 = "test2.csv"
        self.gestion_csv = GestionCSV()

        with open(self.file1, "w", encoding="utf-8") as f1:
            f1.write("nom,quantité,prix,categorie\n")
            f1.write("ProduitA,10,5.5,Cat1\n")
            f1.write("ProduitB,20,10.0,Cat2\n")

        with open(self.file2, "w", encoding="utf-8") as f2:
            f2.write("nom,quantité,prix,categorie\n")
            f2.write("ProduitC,15,7.0,Cat1\n")
            f2.write("ProduitD,30,12.5,Cat3\n")

    def setDown(self):
        """Supprime les fichiers CSV après les tests."""
        if os.path.exists(self.file1):
            os.remove(self.file1)
        if os.path.exists(self.file2):
            os.remove(self.file2)

    def test_ajouter_fichier(self):
        """Teste l'ajout d'un fichier CSV."""
        # Test avec un fichier existant
        result = self.gestion_csv.ajouter_fichier(self.file1)
        self.assertTrue(result)
        self.assertIn(self.file1, self.gestion_csv.fichiers)

        # Test avec un fichier inexistant
        nonexistent_file = "fichier_inexistant.csv"
        result_nonexistent = self.gestion_csv.ajouter_fichier(nonexistent_file)
        self.assertFalse(result_nonexistent)
        self.assertNotIn(nonexistent_file, self.gestion_csv.fichiers)

    def test_recuperer_donnees(self):
        """Teste la récupération des données d'un fichier CSV."""
        # Test avec un fichier existant contenant des données
        self.gestion_csv.ajouter_fichier(self.file1)
        data = self.gestion_csv.recuperer_donnees(self.file1)
        self.assertEqual(len(data), 3)  # Inclut l'en-tête et deux lignes
        self.assertEqual(data[0], ["nom", "quantité", "prix", "categorie"])

        # Test avec un fichier totalement vide
        empty_file = "empty.csv"
        with open(empty_file, "w", encoding="utf-8") as f:
            f.write("")  # on écrit rien
        self.gestion_csv.ajouter_fichier(empty_file)
        empty_data = self.gestion_csv.recuperer_donnees(empty_file)
        # Le fichier vide doit renvoyer un tableau vide
        self.assertEqual(empty_data, [])
        os.remove(empty_file)

    def test_sauver_fichier(self):
        """Teste la sauvegarde de données dans un fichier CSV."""
        data = [
            ["nom", "quantité", "prix", "categorie"],
            ["ProduitX", "5", "2.5", "CatX"],
        ]
        output_file = "output.csv"
        self.gestion_csv.sauver_fichier(output_file, data)

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 2)  # Deux lignes de données
        os.remove(output_file)

    def test_fusionner_fichiers(self):
        """Teste la fusion de plusieurs fichiers CSV."""
        self.gestion_csv.ajouter_fichier(self.file1)
        self.gestion_csv.ajouter_fichier(self.file2)
        merged_data = self.gestion_csv.fusionner_fichiers(
            [self.file1, self.file2])

        self.assertEqual(len(merged_data), 5)  # 1 en-tête + 4 lignes
        self.assertEqual(
            merged_data[0], ["nom", "quantité", "prix", "categorie"])
        self.assertEqual(merged_data[-1], ["ProduitD", "30", "12.5", "Cat3"])

    def test_trier_par_colonne(self):
        """Teste le tri des données d'un fichier CSV par une colonne."""
        self.gestion_csv.ajouter_fichier(self.file1)

        # Trie par la colonne 1 (quantité)
        sorted_data = self.gestion_csv.trier_par_colonne(self.file1, 1)
        self.assertEqual(sorted_data[1], ["ProduitA", "10", "5.5", "Cat1"])
        self.assertEqual(sorted_data[2], ["ProduitB", "20", "10.0", "Cat2"])

        # Teste le cas où la colonne est invalide (colonne hors de portée)
        result = self.gestion_csv.trier_par_colonne(
            self.file1, 10
        )  # Colonne 10 n'existe pas
        self.assertEqual(
            result, []
        )  # Si la colonne n'existe pas,
        # la méthode doit renvoyer un tableau vide


if __name__ == "__main__":
    unittest.main()
