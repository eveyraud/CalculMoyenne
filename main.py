#C:\\cours\\CalculMoyenne-main\\src.txt
from time import sleep
import re
import html  # Pour décoder les caractères HTML

def extraire_notes_ue(contenu_html):
    """
    Extrait et calcule les moyennes des UEs à partir du contenu HTML
    
    Args:
        contenu_html (str): Contenu HTML brut du fichier
        
    Returns:
        tuple: (moyennes_ues, notes_sous_dix, matieres_importantes, moyenne_generale)
    """
    # Initialisation des structures de données
    donnees_ues = {}  # Stockage des données par UE
    notes_sous_dix = set()  # Set pour éviter les doublons des notes < 10
    matieres_importantes = set()  # Set pour les matières avec coeff >= 5
    ue_courante = None
    somme_ponderee_totale = 0
    total_coefficients = 0
    
    # Expressions régulières pour l'extraction des données
    motif_ue = re.compile(
        r'<td colspan="4" class="bleu">(.*?)</td>'
    )
    
    motif_ressource = re.compile(
        r'<td colspan="3" class="vert">(.*?)</td>.*?' +  # Nom ressource
        r'<td class="text_align_center">([\d.]+)</td>.*?' +  # Coefficient
        r'<td class="vert text_align_center">([\d.]*)</td>',  # Note
        re.DOTALL
    )

    def nettoyer_texte(texte):
        """
        Nettoie le texte en décodant les caractères HTML et en supprimant les espaces inutiles
        
        Args:
            texte (str): Texte à nettoyer
            
        Returns:
            str: Texte nettoyé
        """
        # Décode les entités HTML et supprime les espaces superflus
        texte_nettoye = html.unescape(texte)
        # Supprime les "UE RT X.X : " au début du texte si présent
        texte_nettoye = re.sub(r'^UE RT \d+\.\d+ : ', '', texte_nettoye)
        return texte_nettoye.strip()

    def calculer_moyenne_ue(donnees):
        """
        Calcule la moyenne pondérée d'une UE
        
        Args:
            donnees (dict): Données de l'UE (coefficients et somme pondérée)
            
        Returns:
            float/str: Moyenne calculée ou "Pas de notes"
        """
        if donnees['total_coefficients'] > 0:
            moyenne = donnees['somme_ponderee'] / donnees['total_coefficients']
            return round(moyenne, 2)
        return "Pas de notes"

    # Divise le HTML en blocs d'UE
    blocs_ue = re.split(r'<tr>\s*<td colspan="10"></td>\s*</tr>', contenu_html)
    
    # Traitement de chaque bloc d'UE
    for bloc in blocs_ue:
        correspondance_ue = motif_ue.search(bloc)
        
        if correspondance_ue:
            # Extraction et nettoyage du nom de l'UE
            ue_courante = nettoyer_texte(correspondance_ue.group(1))
            donnees_ues[ue_courante] = {
                'total_coefficients': 0,
                'somme_ponderee': 0
            }
            
            # Extraction des ressources de l'UE
            ressources = motif_ressource.finditer(bloc)
            
            # Traitement de chaque ressource
            for ressource in ressources:
                nom_ressource = nettoyer_texte(ressource.group(1))
                coefficient = float(ressource.group(2))
                note_str = ressource.group(3).strip()
                
                if note_str:  # Si une note existe
                    note = float(note_str)
                    # Mise à jour des totaux pour l'UE
                    donnees_ues[ue_courante]['total_coefficients'] += coefficient
                    donnees_ues[ue_courante]['somme_ponderee'] += coefficient * note
                    # Mise à jour des totaux généraux
                    somme_ponderee_totale += coefficient * note
                    total_coefficients += coefficient

                    # Enregistrement des notes < 10
                    if note < 10:
                        notes_sous_dix.add((nom_ressource, note))

                    # Enregistrement des matières importantes
                    if coefficient >= 5:
                        matieres_importantes.add((nom_ressource, coefficient))

    # Calcul des moyennes finales
    moyennes_ues = {
        ue: calculer_moyenne_ue(donnees)
        for ue, donnees in donnees_ues.items()
    }

    # Calcul de la moyenne générale
    moyenne_generale = round(somme_ponderee_totale / total_coefficients, 2) if total_coefficients > 0 else "Pas de notes"

    return moyennes_ues, notes_sous_dix, matieres_importantes, moyenne_generale

CheminValide = False
fichier_src="src.txt"
while not CheminValide:
    try:
        with open(fichier_src, 'r', encoding='utf-8') as fichier:
            contenu_html = fichier.read()
            CheminValide=True

    except FileNotFoundError:
        print("Erreur: Le fichier src.txt n'a pas été trouvé.")
        fichier_src = input("Veuillez entrer le chemin absolu du fichier: ")

    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        fichier_src = input("Veuillez entrer le chemin absolu du fichier: ")

try:
    moyennes, notes_sous_dix, matieres_importantes, moyenne_generale = extraire_notes_ue(contenu_html)
    # Affichage des notes sous 10
    print("\nNotes en dessous de la moyenne:")
    print("-" * 50)
    for matiere, note in sorted(notes_sous_dix):
        print(f"{matiere}: {note}")


    # Affichage des matières importantes

    print("\nMatières importantes (coefficient >= 5):")
    print("-" * 50)

    for matiere, coeff in sorted(matieres_importantes):
            print(f"{matiere} (coefficient: {coeff})")

    # Affichage des moyennes par UE
    print("\nMoyennes par UE:")
    print("-" * 50)
    for ue, moyenne in moyennes.items():
        print(f"{ue}: {moyenne}")

        # Affichage de la moyenne générale
    print("\nMoyenne générale:")
    print("-" * 50)
    print(f"Moyenne générale: {moyenne_generale}")
    input()
    input()

except Exception as e:
    print(f"Erreur lors du traitement des notes: {e}")
