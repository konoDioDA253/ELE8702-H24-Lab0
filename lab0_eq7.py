## Numéro d'équipe : 
## Bouh Abdillahi (Matricule : 1940646)
## Vincent Yves Nodjom (Matricule : 1944011)
## Équipe : 7
## Github link : https://github.com/konoDioDA253/ELE8702-H24-Lab0

import sys
import math
import yaml
import random
import os
import argparse

# Variables GLOBAL
# Numero propres a l'équipe
numero_equipe = '7'
numero_lab = '0'
# Variables servant à la fonction treat_args()
parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str)
args = parser.parse_args()


# Germe de toutes les fonctions aléatoires
random.seed(123)

class Antenna:
    
    def __init__(self, id):
        self.id = id
        self.group = None
        self.coords = None
        self.assoc_ues = []
        self.scenario = None
        self.frequency = None
        self.gen    = None # type de gÃ©neration de coordonnÃ©es: 'g', 'a', etc. (str)\n",
        # self.height = None
        # (PROF) Est-ce que c'est correct de modifier comme cela la classe?
        # self.coordx = None
        # self.coordy = None

    
class UE:
    
    def __init__(self, id, app_name):
        self.id= id
        self.group = None
        self.coords = None
        self.app=app_name
        self.assoc_ant=None #id de l'antenne associÃ©e Ã  l'UE (int)\n",
        self.los = True
        self.gen = None # type de gÃ©neration de coordonnÃ©es: 'g', 'a', etc. (str)\n",
        # Attribut rajoutee par notre equipe
        self.apptype = None # Pas besoin car tirer de la chaine de caractere de group


def fill_up_the_lattice(N, lh, lv, nh, nv):
    """Function appelée par get_rectangle_lattice_coords()"""
    
    def get_delta1d(L, n):
        return L/(n + 1)
    
    coords = []
    deltav = get_delta1d(lv, nv)
    deltah = get_delta1d(lh, nh)
    line = 1
    y = deltav
    count = 0
    while count < N:
        if count + nh < N:
            x = deltah
            for  i in range(nh):
                # Fill up the horizontal line
                coords.append((x,y))
                x = x + deltah
                count += 1
            line += 1
        else:
            deltah = get_delta1d(lh, N - count)
            x = deltah
            for i in range(N - count):
                # Fill up the last horizontal line
                coords.append((x,y))
                x = x + deltah
                count += 1
            line += 1
        y = y +deltav
    return coords

def get_rectangle_lattice_coords(lh, lv, N, Np, nh, nv):
    """Function appelee par gen_lattice_coords()"""
    
    if Np > N:
        coords = fill_up_the_lattice(N, lh, lv, nh, nv)
    elif Np < N:
        coords = fill_up_the_lattice(N, lh, lv, nh, nv + 1)
    else:
        coords = fill_up_the_lattice(N, lh, lv, nh, nv)
    return coords

def gen_lattice_coords(terrain_shape: dict, N: int):
    """Génère un ensemble de N coordonnées placées en grille 
       sur un terrain rectangulaire
    
       Args: terrain_shape: dictionary {'rectangle': {'length' : lh,
                                                   'height' : lv}
           lh and lv are given in the case file"""
    #CETTE FONCION EST OBLIGATOIRE POUR L'OPTION GRILLE (g) DU FICHIER DE CAS

    shape = list(terrain_shape.keys())[0]
    lh = terrain_shape[shape]['length']
    lv = terrain_shape[shape]['height']
    R = lv / lh    
    nv = round(math.sqrt(N / R))
    nh = round(R * nv)
    Np = nh * nv
    if shape.lower() == 'rectangle':
        coords = get_rectangle_lattice_coords(lh, lv, N, Np, nh, nv)
    else:
        msg = [f"\tImproper shape ({shape}) used in the\n",
                "\tgeneration of lattice coordinates.\n"
                "\tValid values: ['rectangle']"]
        ERROR(''.join(msg), 2)
    return coords        

def get_from_dict(key, data, res=None, curr_level = 1, min_level = 1):
    """Fonction qui retourne la valeur de n'importe quel clé du dictionnaire
       key: clé associé à la valeur recherchée
       data: dictionnaire dans lequel il faut chercher
       les autres sont des paramètres par défaut qu'il ne faut pas toucher"""
    if res:
        return res
    if type(data) is not dict:
        msg = f"get_from_dict() works with dicts and is receiving a {type(data)}"
        ERROR(msg, 1)
    else:
        # data IS a dictionary
        for k, v in data.items():
            if k == key and curr_level >= min_level:
                #print(f"return data[k] = {data[k]} k = {k}")
                return data[k]
            if type(v) is dict:
                level = curr_level + 1
                res = get_from_dict(key, v, res, level, min_level)
    return res 

def read_yaml_file(fname):
    # Fonction utilisée pour lire les fichiers de type .yaml
    # fname: nom du fichier .yaml à lire
    # le retour de la fonction est un dictionnaire avec toute l'information qui se trouve
    # dans le fichier .yaml
    # Si vous préférez vous pouvez utiliser une autre fonction pour lires les fichiers
    # de type .yaml.
    # À noter que dans cette fonction il faut ajouter les vérifications qui s'imposent
    # par exemple, l'existance du fichier
    
    # Vérifier l'existence du fichier
    if not os.path.exists(fname):
        raise FileNotFoundError(f"Le fichier {fname} n'existe pas.")

    # Ouvrir et lire le fichier YAML
    with open(fname, 'r') as file:
        return yaml.safe_load(file)

# Fonction attribuant des coordonnées aléatoires
# Prends en paramètre le fichier de cas pour avoir la longueur et la largeur du terrain    
def gen_random_coords(fichier_de_cas):
    # Cette fonction doit générer les coordonées pour le cas de positionnement aléatoire
    # TODO PRESENTABLE
    longueur_geometry = fichier_de_cas['ETUDE_IMPORTANT']['GEOMETRY']['Surface']['rectangle']['length']
    hauteur_geometry = fichier_de_cas['ETUDE_IMPORTANT']['GEOMETRY']['Surface']['rectangle']['height']
    

    x_aleatoire = random.randint(1, longueur_geometry)
    y_aleatoire = random.randint(1, hauteur_geometry)
    coordonnees_aleatoires = [x_aleatoire, y_aleatoire]
    return coordonnees_aleatoires



# fonction initialisant une liste de ues et assignant des coordonnées aléatoirement à chaque ue dans la liste
def assigner_coordonnees_ues(fichier_de_cas):
    liste_ues_avec_coordonnees = []

    nombre_ues_ue1 = fichier_de_cas['ETUDE_IMPORTANT']['DEVICES']['UE1-App1']['number']
    nombre_ues_ue2 = fichier_de_cas['ETUDE_IMPORTANT']['DEVICES']['UE2-App2']['number']
    type_de_generation = fichier_de_cas['ETUDE_IMPORTANT']['UE_COORD_GEN']

    for i in range(nombre_ues_ue1):
        ue = UE(id=len(liste_ues_avec_coordonnees), app_name='UE1-App1')
        if (type_de_generation == 'a') :
            coords = gen_random_coords(fichier_de_cas)
        ue.gen = type_de_generation
        ue.coords = coords
        ue.apptype = "app1"
        liste_ues_avec_coordonnees.append(ue)

    for i in range(nombre_ues_ue2):
        ue = UE(id=len(liste_ues_avec_coordonnees), app_name='UE2-App2')
        if (type_de_generation == 'a') :
            coords = gen_random_coords(fichier_de_cas)
        ue.gen = type_de_generation
        ue.coords = coords
        ue.apptype = "app2"
        liste_ues_avec_coordonnees.append(ue)

    return liste_ues_avec_coordonnees

# fonction initialisant une liste de antennes et assignant des coordonnées selon la grille à chaque antenne
def assigner_coordonnees_antennes(fichier_de_cas):
    liste_antennes_avec_coordonnees = []

    nombre_antennes = fichier_de_cas['ETUDE_IMPORTANT']['DEVICES']['Antenna1']['number']
    type_de_generation = fichier_de_cas['ETUDE_IMPORTANT']['ANT_COORD_GEN']
    
    terrain_shape =  fichier_de_cas['ETUDE_IMPORTANT']['GEOMETRY']['Surface']
    coords = gen_lattice_coords(terrain_shape, nombre_antennes)

    for id, coord in enumerate(coords):
        antenna = Antenna(id)
        antenna.coords = coord
        antenna.gen = type_de_generation
        antenna.group = "Antenna1"
        liste_antennes_avec_coordonnees.append(antenna)

    return liste_antennes_avec_coordonnees

# fonction qui ecrit les information par rapport aux antennes et au UEs
def write_to_file(antennas, ues, fichier_de_cas):

    with open(fichier_de_cas['ETUDE_IMPORTANT']['COORD_FILES']['write'], 'w') as file:
        for antenna in antennas:
            line = f"antenna\t{antenna.id}\t{antenna.group}\t{round(antenna.coords[0],1)}\t{round(antenna.coords[1], 1)}\n"
            file.write(line)

        for ue in ues:
            line = f"ue\t{ue.id}\t{ue.app}\t{ue.coords[0]}\t{ue.coords[1]}\t{ue.apptype}\n"
            file.write(line)

# Retourne une liste d'antennes et d'ues avec leurs coordonnées initialisées
def lab0 (fichier_de_cas):
    #TODO ....
    # antennas est une liste qui contient les objets de type Antenna
    # ues est une liste qui contient les objets de type UE
    #
    # antennas = [ant0,ant1,...] 
    #            ant1, ant2 etc sont des instances (objets) de la classe Antenna
    # ues = [ue0, ue1,...] 
    #             ue0, ue1, etc sont des instances (objets) de la classe UE
    # avant de faire le retour, les objets appartenant aux listes antennas et ues 
    # doivent avoir leur coordonées initialisées
    # CETTE FONCTION EST OBLIGATOIRE

    ues = assigner_coordonnees_ues(fichier_de_cas)
    antennas = assigner_coordonnees_antennes(fichier_de_cas)
    return (antennas,ues)

# Fonction vérifiant si le fichier YAML fournit en input a la bonne structure 
def validate_yaml_structure(file_path):
    try:
        with open(file_path, 'r') as file:
            yaml_content = yaml.load(file, Loader=yaml.FullLoader)
    except yaml.YAMLError as e:
        print(f"Error loading YAML file '{file_path}': {e}")
        return False

    # Define the expected structure
    expected_structure = {
        'ETUDE_IMPORTANT': {
            'SCENARIO': None,
            'ANT_COORD_GEN': None,
            'UE_COORD_GEN': None,
            'COORD_FILES': None,
            'DEVICES': {
                'Antenna1': {'number': None},
                'UE1-App1': {'number': None},
                'UE2-App2': {'number': None},
            },
            'GEOMETRY': {
                'Surface': {
                    'rectangle': {
                        'length': None,
                        'height': None
                    }
                }
            }
        }
    }

    # Validate the structure
    if not validate_structure(yaml_content, expected_structure):
        # Invalid structure in YAML file
        return False

    # Valid structure in YAML file
    return True

# Fonction comparant deux structures YAML et retournant False si différence existe
def validate_structure(content, expected_structure):
    if not isinstance(content, dict) or not isinstance(expected_structure, dict):
        return False

    for key, value in expected_structure.items():
        if key not in content:
            return False

        if value is not None and not validate_structure(content[key], value):
            return False

    return True


def treat_args() :
    # cette fonction doit retourner le nom du fichier de cas à partir de l'interface de commande (CLI)
    #... 
    # TODO
    #....
    # CETTE FONCTION EST OBLIGATOIRE
    # À noter que dans cette fonction il faut ajouter les vérifications qui s'imposent
    # par exemple, nombre d'arguments appropriés, existance du fichier de cas, etc.
    case_file_name = args.config
    # Check if the file exists
    YAML_file_exists = True
    YAML_file_correct_extension = True
    correct_yaml_structure = True
    if os.path.isfile(case_file_name):
        # Check if the file has a YAML extension
        _, file_extension = os.path.splitext(case_file_name)
        if file_extension.lower() not in ['.yaml', '.yml']:
            YAML_file_correct_extension = False
        else:
            # YAML has the correct extension
            # Check if the YAML structure is good
            file_path = case_file_name
            if validate_yaml_structure(file_path):
                correct_yaml_structure = True
            else:
                correct_yaml_structure = False
    else:
        YAML_file_exists = False
    return YAML_file_exists, YAML_file_correct_extension, correct_yaml_structure, case_file_name

def main():
    yaml_exist, yaml_correct_extenstion, correct_yaml_structure, case_file_name = treat_args()
    print("YAML file name = ", case_file_name)
    if (yaml_exist == False):
        print("YAML file doesn't exist!")   
        return 
    else:
        print("YAML file exists")
    if yaml_correct_extenstion == False :
        print(f"The YAML file does not have the correct extension.")
        return
    else:
        print(f"The YAML file has the correct extension.")
    if correct_yaml_structure == True:
        print(f"The YAML file has the correct structure.")
    else:
        print(f"The YAML file does not have the correct structure.")
        return

    #
    #TODO les instructions de main qui vont faire appel aux autres fonctions du programme
    #.....
    fichier_de_cas = read_yaml_file(case_file_name)

    antennas, ues = lab0(fichier_de_cas)

    write_to_file(antennas,ues,fichier_de_cas)
    


if __name__ == '__main__':
    main()
