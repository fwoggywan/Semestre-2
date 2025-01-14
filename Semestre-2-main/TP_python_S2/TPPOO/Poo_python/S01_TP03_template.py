#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *
from S01_TP02_template import *


def get_words_graph_from_dictionary(dictionary, length):
    """ Retourne un graphe de mots bidirectionnel : dictionnaire Python dont les items sont chaque mot de 'dictionary'
    de longueur 'length' associé à la liste des mots qui sont à une distance de Hamming de 1."""
    mots = get_words_from_dictionary(dictionary, length)
    final_graph = {}
    for word in mots:
        final_graph[word] = get_words_hamming(word, mots, 1)
    return final_graph
def get_length_words(words_graph):
    """ retourne la longueur des mots du graphe de mots 'words_graph'."""
    list_words_graph = list(words_graph.keys())
    return len(list_words_graph[0])

def words_graph_to_file(path, words_graph):
    """ Sauve le graphe de mots 'words_graph' dans un fichier créé dans le dossier 'path' sous le nom 'n.wg' avec n la
    longueur des mots du graphe. Chaque ligne du fichier sera composée d'une liste de mots représentant une entrée de
     'words_graph' et la liste des mots à une distance de Hamming de 1."""
    with open(path+"//"+str(get_length_words(words_graph))+".wg", "a") as file:
        keys = str(words_graph.keys())
        values = str(words_graph.values())
        for i in range(len(keys)):
            file.write(keys[i] + values[i])
        

def get_words_graph_from_file(path, length):
    """ Reconstruit le graphe de mots de longueur 'length' à partir du fichier 'n.wg' sauvé dans le dossier 'path'."""
    dico = {}
    with open(path+"//"+str(length)+".wg", "r") as file:
        content = file.readlines()
        for element in content:
            element = element.split(' ')
            if len(element[0]) == length and len(element) > 1:
                element[-1] = element[-1].strip()
                liste = []
                for i, word in enumerate(element):
                    if i != 0:
                        liste.append(word)
                dico[element[0]] = liste[:]
        return dico

def insert_word(new_word, words_graph):
    """ Insère le nouveau mot 'new_word' dans le graphe de mots 'words_graph' s'il n'y est pas déjà. Une 'Exception'
    sera levée si le nouveau mot n'a pas la longueur adéquate. Attention à bien représenter toutes les nouvelles
    connexions (graphe bidirectionnel)"""
    if len(new_word) != get_length_words(words_graph):
        return 0
    list_keys = list(words_graph.keys())
    if new_word in list_keys:
        return 0
    new_entries = []
    for i in range(len(list_keys)):
        if get_hamming_distance(new_word, list_keys[i]) == 1:
            words_graph[list_keys[i]].append(new_word)
            new_entries.append(list_keys[i])
    words_graph[new_word] = new_entries
    return



def get_shortest_scale(words_graph, starting_word, target_word):
    """ Retourner la liste des mots du plus court chemin dans le graphe 'words_graph' entre les mots 'starting_word' et
    'target_word'. Ces deux mots peuvent ne pas être dans le dictionnaire et doivent donc être insérer dans le graphe
    (avant la recherche d'une solution en parcourant le graphe en largeur d'abord). Il s'agit de maintenir pendant le
    parcours (1) un dictionnaire Python des éléments visités associés à leur prédécesseur et initialisé à
    {starting_word: None} ; (2) une liste des éléments qu'il reste à explorer initialisé à [starting_word].
    Tant qu'il reste des mots à explorer dans (2) :
    - si (2) est vide, il n'y a pas de solutions. None est retourné.
    - si le premier mot de (2) est 'target_word' la solution est trouvée
    - dans les autres cas, le premier mot est retiré et tous ses voisins non visités sont ajoutés en (1) avec
    ce mot comme prédécesseur et également en fin de (2) comme nouvelles solutions à explorer.
    Dès que 'target_word' est atteint, il suffit d'utiliser le dictionnaire (1) pour retrouver la solution en remontant
    de prédécesseur en prédécesseur jusqu'à None."""
    words_graph_keys = list(words_graph.keys())
    deux = [starting_word]
    un = {starting_word : None}
    words_graph = insert_word(starting_word, words_graph)
    words_graph = instert_word(target_word, words_graph)
    liste = get_words_hamming(deux[0] ,words_graph, 1)
    deux = liste[:]
    un[starting_word] = liste[:]


if __name__ == "__main__":
    DICT_NAME = PATH_DICTIONARIES + 'fr_long_dict_cleaned.txt'
    # Les 4 lignes de code suivantes sont à commenter dès que la question 3 est résolue car la construction de
    # WORDS5_GRAPH peut être un peu longue
    """
    WORDS5_GRAPH = get_words_graph_from_dictionary(DICT_NAME, 5)
    assert WORDS5_GRAPH['HOMME'] == ['COMME', 'GOMME', 'HOMIE', 'NOMME', 'POMME', 'SOMME', 'TOMME']
    assert get_length_words(WORDS5_GRAPH) == 5
    words_graph_to_file(PATH_OUT + 'WG/', WORDS5_GRAPH)
    """

    with open(PATH_OUT + 'WG/5.wg', 'r', encoding='utf-8') as f_in:
        assert f_in.readlines()[:3] == ['ABACA AGACA\n', 'ABATS EBATS\n', 'ABBES ABCES ABLES AUBES\n']

    # Les deux lignes de code suivantes doivent toujours être commentées dans le TP car le processus est long.
    # Pour faire l'opération manuellement, une fois la question 3 résolue, il faut décompresser l'archive de ecampus
    # contenant les 25 fichiers de graphes 'n.wg' dans le répertoire '/OUT/WG' de votre arborescence
    # for i in range(1, 26):
    #     words_graph_to_file(PATH_OUT, get_words_graph_from_dictionary(PATH_DICT, i))

    WORDS_GRAPHS = {}
    for i in range(1, 26):
        WORDS_GRAPHS[i] = get_words_graph_from_file(PATH_OUT + 'WG/', i)
    assert WORDS_GRAPHS[5]['HOMME'] == ['COMME', 'GOMME', 'HOMIE', 'NOMME', 'POMME', 'SOMME', 'TOMME']
    assert WORDS_GRAPHS[3]['IRA'] == ['ARA', 'IRE']
    assert WORDS_GRAPHS[3]['OSA'] == ['OSE', 'OST', 'OTA', 'USA']
    assert WORDS_GRAPHS[3]['USA'] == ['OSA', 'USE', 'UVA']
    try:
        WORDS_GRAPHS[3]['ISA']
    except KeyError as e:
        assert e.args == ('ISA',)
    insert_word('ISA', WORDS_GRAPHS[3])
    assert WORDS_GRAPHS[3]['ISA'] == ['IRA', 'OSA', 'USA']
    assert WORDS_GRAPHS[3]['IRA'] == ['ARA', 'IRE', 'ISA']
    assert WORDS_GRAPHS[3]['OSA'] == ['OSE', 'OST', 'OTA', 'USA', 'ISA']
    assert WORDS_GRAPHS[3]['USA'] == ['OSA', 'USE', 'UVA', 'ISA']

    t1 = perf_counter()
    assert get_shortest_scale(WORDS_GRAPHS[5], 'HOMME', 'SINGE') == ['HOMME', 'COMME', 'COMTE',
                                                                     'CONTE', 'CONGE', 'SONGE', 'SINGE']
    t2 = perf_counter()
    print(t2 - t1)
    assert get_shortest_scale(WORDS_GRAPHS[4], 'TOUT', 'RIEN') == ['TOUT', 'BOUT', 'BRUT',
                                                                   'BRUN', 'BREN', 'BIEN', 'RIEN']
    t3 = perf_counter()
    print(t3 - t2)
    assert get_shortest_scale(WORDS_GRAPHS[4], 'RASE', 'PRES') == ['RASE', 'RAIE', 'PAIE',
                                                                   'PAIS', 'PRIS', 'PRES']
    t4 = perf_counter()
    print(t4 - t3)
    assert get_shortest_scale(WORDS_GRAPHS[4], 'MATH', 'PURE') == ['MATH', 'MATE', 'MARE',
                                                                   'MURE', 'PURE']
    t5 = perf_counter()
    print(t5 - t4)
    assert get_shortest_scale(WORDS_GRAPHS[3], 'SUD', 'EST') == ['SUD', 'SUT', 'EUT', 'EST']
    t6 = perf_counter()
    print(t6 - t5)
    assert get_shortest_scale(WORDS_GRAPHS[3], 'ISA', 'FAB') == ['ISA', 'OSA', 'OST', 'OIT',
                                                                 'FIT', 'FAT', 'FAB']
    t7 = perf_counter()
    print(t7 - t6)
    assert get_shortest_scale(WORDS_GRAPHS[5], 'AVANT', 'APRES') == ['AVANT', 'AVENT', 'AIENT',
                                                                     'LIENT', 'LIENS', 'LIEES', 'LIRES', 'AIRES',
                                                                     'APRES']
    t8 = perf_counter()
    print(t8 - t7)
    print("All tests OK")

