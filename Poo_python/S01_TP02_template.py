#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import *
from S01_TP01_template import get_hamming_distance
from time import perf_counter


def get_words_from_dictionary(file_path, length=None):
    """ Retourne la liste des mots du fichier de nom 'file_name' si 'length' vaut 'None'.
        Sinon retourne la liste des mots de longueur 'length'."""
    with open(file_path, 'r') as f_in:
        contenu = f_in.readlines()
    liste = []
    for i,ligne in enumerate(contenu):
        if length == None :
            liste.append(ligne[:-1])
        else :
            if len(ligne)-1 == length :
                liste.append(ligne[:-1])
    return liste
    

def get_words_hamming(word, words, hamming_distance):
    """ Retourne une sous-liste de la liste de mots 'words' qui sont à une distance de Hamming
        'hamming_distance' du mot 'word'."""
    liste = []
    for mot in words : 
        if get_hamming_distance(word , mot) == hamming_distance :
            liste.append(mot)
    return liste


def is_perfect_scale(scale):
    """Retourne 'True' si l'échelle de mots 'scale' est parfaite. 'False' sinon. Une échelle de mots est dite parfaite
    si le nombre d'étape pour passer du mot de départ au mot cible est égal à leur distance de hamming."""
    return  len(scale)-1 == get_hamming_distance(scale[0] ,scale[-1]) 
        


def get_removed_words(words_to_remove, all_words):
    """ Retourne une sous-liste des mots de 'all_words' en retirant ceux de 'words_to_remove'"""
    liste = []
    for mot in all_words : 
        if mot not in words_to_remove :
            liste.append(mot)
    return liste 


def get_next_scales(scale, words):
    """ retourne la liste des échelles de mots possibles constituées par l'échelle de mot 'scale' et un mot de
    la liste 'words'"""
    conteneur = []
    words = get_removed_words(scale, words)
    for mot in words : 
        if get_hamming_distance(mot,scale[-1]) == 1 :
            conteneur.append(scale + [mot])
            
    return conteneur



def get_scale(file_path, word1, word2):
    with open(file_path, 'r') as f_in:
        contenu = [line.strip() for line in f_in.readlines()]
    liste = [word1]
    taille = get_hamming_distance(word1, word2)
    contenu = get_removed_words([word1, word2], contenu)
    for i in range(taille):
        big = get_next_scales(liste, contenu)   
        for mot in contenu:
            if get_hamming_distance(mot, word2) == taille - i - 1 and get_hamming_distance(mot, word1) == i+1 :
                liste.append(mot)
                contenu = get_removed_words([mot], contenu)
                break
    liste.append(word2)
    print(liste)
    return liste
        

        
    


if __name__ == "__main__":
    DICT_NAME = PATH_DICTIONARIES + 'fr_long_dict_cleaned.txt'
    WORD6 = get_words_from_dictionary(DICT_NAME, 6)
    assert WORD6[:9] == ['A-T-IL', 'ABAQUE', 'ABATEE', 'ABATTE', 'ABATTU', 'ABBAYE', 'ABCEDE', 'ABERRE', 'ABETIE']
    assert get_words_hamming("ORANGE", WORD6, 0) == ['ORANGE']
    assert get_words_hamming("ORANGE", WORD6, 1) == ['FRANGE', 'GRANGE', 'ORANGS', 'ORANTE',
                                                     'ORONGE']
    assert get_words_hamming("ORANGE", WORD6, 2) == ['BRANDE', 'BRANLE', 'BRANTE', 'CHANGE',
                                                     'CRANTE', 'GRANDE', 'GRINGE', 'ORACLE', 'ORANTS', 'TRANSE',
                                                     'URANIE']
    assert  is_perfect_scale(['SUD', 'SUT', 'EUT', 'EST'])
    assert is_perfect_scale(['HOMME', 'COMME', 'COMTE', 'CONTE'])
    assert not is_perfect_scale(['HOMME', 'COMME', 'COMTE', 'CONTE', 'CONGE'])
    NEW_WORD6 = get_removed_words(['A-T-IL', 'ABATTU'], WORD6)
    assert WORD6[:9] == ['A-T-IL', 'ABAQUE', 'ABATEE', 'ABATTE', 'ABATTU', 'ABBAYE', 'ABCEDE', 'ABERRE', 'ABETIE']
    assert NEW_WORD6[:9] == ['ABAQUE', 'ABATEE', 'ABATTE', 'ABBAYE', 'ABCEDE', 'ABERRE', 'ABETIE', 'ABETIR', 'ABETIS']
    
    assert get_next_scales(['CHANGE', 'CHANTE'], WORD6) == [
        ['CHANGE', 'CHANTE', 'CHANCE'],
        ['CHANGE', 'CHANTE', 'CHANTA'],
        ['CHANGE', 'CHANTE', 'CHANTS'],
        ['CHANGE', 'CHANTE', 'CHARTE'],
        ['CHANGE', 'CHANTE', 'CHASTE'],
        ['CHANGE', 'CHANTE', 'CHATTE'],
        ['CHANGE', 'CHANTE', 'CRANTE']]

    t1 = perf_counter()
    print(get_scale(DICT_NAME, 'SUD', 'EST'))
    assert get_scale(DICT_NAME, 'SUD', 'EST') == ['SUD', 'SUT', 'EUT', 'EST']
    t2 = perf_counter()
    print(t2 - t1)
    # Ne tester les assertions suivantes en commentaires uniquement sur un ordinateur puissant
    # assert get_scale(DICT_NAME, 'HOMME', 'SINGE') ==  ['HOMME', 'COMME', 'COMTE', 'CONTE', 'CONGE',
    #                                                    'SONGE', 'SINGE']
    # t3 = perf_counter()
    # print(t3 - t2)
    # assert get_scale(DICT_NAME, 'EXOS', 'MATH') == ['EXOS', 'EROS', 'GROS', 'GRIS', 'GAIS', 'MAIS',
    #                                                 'MATS', 'MATH']
    # t4 = perf_counter()
    # print(t4 - t3)
    # assert get_scale(DICT_NAME, 'TOUT', 'RIEN') == ['TOUT', 'BOUT','BRUT', 'BRUN', 'BREN', 'BIEN', 'RIEN']
    # t5 = perf_counter()
    # print(t5 - t4)
    print("All tests OK")
