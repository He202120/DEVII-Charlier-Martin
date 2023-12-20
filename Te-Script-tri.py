import unittest
import trieFichier
from click.testing import CliRunner


class TestTrieMethods(unittest.TestCase):

    def test_trier_regroupement(self):
        runner = CliRunner()
        # test de la fonction
        self.assertRaises(FileNotFoundError, trieFichier.trier_regroupement, "fichier", "fichier2")
        # test par l'appel la fonction
        # Va tester s'il déplace bien les fichiers
        result = runner.invoke(trieFichier.trier_fichiers, ["fichier3", "fichier4", "--tri-regroupement"])
        self.assertEqual(0, result.exit_code)
        # Va tester s'il y a une erreur lorsque que le fichier source n'existe pas (le 1 dans le assertEqual correspond
        # à une erreur
        result = runner.invoke(trieFichier.trier_fichiers, ["fichie", "fichier2", "--tri-regroupement"])
        self.assertEqual(1, result.exit_code)


    def test_trier_fichiers(self):
        runner = CliRunner()
        # test de la fonction
        self.assertRaises(FileNotFoundError, trieFichier.trier_par_extension, "fichier", "fichier2")
        # Va tester s'il déplace bien les fichiers
        result = runner.invoke(trieFichier.trier_fichiers, ["fichier5", "fichier4", "--tri-par-extension"])
        self.assertEqual(0, result.exit_code)
        # Va tester s'il y a une erreur lorsque que le fichier source n'existe pas (le 1 dans le assertEqual correspond
        # à une erreur
        result = runner.invoke(trieFichier.trier_fichiers, ["fichie", "fichier2", "--tri-par-extension"])
        self.assertEqual(1, result.exit_code)

    def test_renommer_avec_numéro_Croiss(self):
        runner = CliRunner()
        # test de la fonction
        self.assertRaises(FileNotFoundError, trieFichier.renommer_avec_numéro_Croiss, "fichier")
        # test de la fonction pour renommer
        result = runner.invoke(trieFichier.trier_fichiers, ["fichier4", "fichier2", "--renommer-fichiers"])
        self.assertEqual(0, result.exit_code)

    def test_supprimer_fichiers_source(self):
        runner = CliRunner()
        # test de la fonction
        self.assertRaises(FileNotFoundError, trieFichier.supprimer_fichiers_source, "fichier")
        result = runner.invoke(trieFichier.trier_fichiers, ["fichier4", "fichier2", "--supprimer-fichiers"])
        self.assertEqual(0, result.exit_code)


if __name__ == '__main__':
    unittest.main()
