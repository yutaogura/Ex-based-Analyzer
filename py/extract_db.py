"""
Created on Mon Sep 15 2020

Jazz Harmony Treebank からlexicon.txt と　nonterminals.txtを作る


デバッグしたいところにこれブチ込む
import pdb; pdb.set_trace()

pyディレクトリ中で
python extract_db.py
を実行 

@author:yuta ogura
"""

import json
import numpy as np
import re
import collections
import math


#Globals
years = {}
lengths = {}
depths = []
turnarounds = {}
rules = []
rules_minor = []
rules_major = []

rule_with_prob = {}

FILE_NAME_TREEBANK = './treebank/treebank.json'
FILE_NAME_NONTERMINAL = "./nonterminals.txt"
FILE_NAME_LEXICON = "./lexicon.txt"
FILE_NAME_GRAMMAR = "./pcfg.txt"
FILE_TONIC_CHORD = "./tonic.txt"

# Key and chord utility functions
note_norm = {'A' : 9,'B' : 11,'C' : 0,'D' : 2,'E' : 4,'F' : 5,'G' : 7,'A#' : 10,'B#' : 0,'C#' : 1,'D#' : 3,'E#' : 5,'F#' : 6,'G#' : 8,'Ab' : 8,'Bb' : 10,'Cb' : 11,'Db' : 1,'Eb' : 3,'Fb' : 4,'Gb' : 6}
flats = {0 : 'C', 1 : 'Db', 2 : 'D', 3 : 'Eb', 4 : 'E',5 : 'F',6 : 'Gb',7 : 'G',8 : 'Ab',9 : 'A',10: 'Bb',11: 'B'}
sharps = {0 : 'C',1 : 'C#',2 : 'D',3 : 'D#',4 : 'E',5 : 'F',6 : 'F#',7 : 'G',8 : 'G#',9 : 'A',10: 'A#',11: 'B'}

tonic_chord_type =['^7','^','m7','m']


# Tree utility functions
def treedepth(t):
    if(t['children'] == []):
        return 0
    else:
        return 1 + max(map(treedepth, t['children']))
    
def width_of_tree(t):
    if(t['children'] == []):
        return 1
    else:
        return sum(map(width_of_tree, t['children']))



# Normalising a chord to a specific tree
def key_normalize_chord(chord, key):
    regex = re.compile("([A-G][b#]?)([m]?)(.*)")
    
    (chord_pitch,chord_minor,chord_quality) = regex.match(chord).groups()
    (key_pitch,  key_minor,  key_quality  ) = regex.match(key).groups()
    
    chord_numeric_pitch = note_norm[chord_pitch]
    key_numeric_pitch   = note_norm[key_pitch]
    
    chord_normalized_numeric_pitch = (chord_numeric_pitch - key_numeric_pitch) % 12

    # ハーフディミニッシュ%とメジャー^をhdim，Mに置き換え
    chord_quality = replace_badsymbol(chord_quality)

    # We're using the flats for now
    return flats[chord_normalized_numeric_pitch] + chord_minor + chord_quality

def key_nonnormalize_chord(chord,key):
    regex = re.compile("([A-G][b#]?)([m]?)(.*)")
    
    (chord_pitch,chord_minor,chord_quality) = regex.match(chord).groups()
    
    chord_numeric_pitch = note_norm[chord_pitch]

    # ハーフディミニッシュ%とメジャー^をhdim，Mに置き換え
    chord_quality = replace_badsymbol(chord_quality)

    # We're using the flats for now
    return flats[chord_numeric_pitch] + chord_minor + chord_quality

def key_is_minor(key):
    regex = re.compile("([A-G][b#]?)([m]?)(.*)")
    (key_pitch,  key_minor,  key_quality  ) = regex.match(key).groups()
    return key_minor == 'm'

# The key of a tree is its rightmost leaf(本当か？)
def get_key(t):
    if(t['children'] == []):
        return t['label']
    else:
        return get_key((t['children'])[-1])

def replace_badsymbol(chord):
    if '^' in chord:
        chord = chord.replace('^','M')
    if '%' in chord:
        chord = chord.replace('%','hdim')
    return chord

# 楽曲のkeyはroot(素直)
def get_root(t):
    root_chord = t['label']
    # ハーフディミニッシュ%とメジャー^をhdim，Mに置き換え
    root_chord = replace_badsymbol(root_chord)

    return root_chord

# Return all the rules used in a tree. Trees are at most binary
def get_rules(t,key):
    if(t['children'] == []):
        return []
    else:
        lefts = get_rules(t['children'][0],key)
        if len(t['children']) == 2 :
            rights = get_rules(t['children'][1],key)
            return [(key_nonnormalize_chord(t['label'],key) , (
                                   key_nonnormalize_chord(t['children'][0]['label'],key),
                                   key_nonnormalize_chord(t['children'][1]['label'],key)
            ))] + lefts + rights
        else:
            return [(key_nonnormalize_chord(t['label'],key) , (key_nonnormalize_chord(t['children'][0]['label'],key)), key)] + lefts



## main 


# Load the treebank
with open(FILE_NAME_TREEBANK, 'r') as f:
    tunes = json.load(f)


chords = [] 
for t in tunes:
    #tree アノテーションが存在するものに限定
    if 'trees' in t.keys():
        for i in t['chords']:
            if not i in chords:
                chords.append(i)


#lexiconの作成
exist_chords = sorted(chords) 
with open(FILE_NAME_LEXICON,'w') as f:
    for i in exist_chords:
        i = replace_badsymbol(i)
        f.write(i + " -> "  + i + "\n")

#nonterminalsの作成
with open(FILE_NAME_NONTERMINAL,'w') as f:
    for i in exist_chords:
        i = replace_badsymbol(i)
        f.write(i + "\n")

# pcfgの作成

valid_tune_num = 0

for t in tunes:
    if (t.get('trees') != None) and (len(t.get('chords')) < 40):
        tree = t['trees'][0]['complete_constituent_tree']
        depths.append((len(t.get('chords')),width_of_tree(tree),treedepth(tree)/math.log(width_of_tree(tree)),treedepth(tree),t.get('year'),t.get('title'),tree))
        # We extract all the rule applications in each tree, and make a common list, as well segregated by minor/major
        print(valid_tune_num,":",t.get('title'),get_root(tree))
        valid_tune_num += 1
        t_rules = get_rules(tree,get_key(tree))
        rules += t_rules
        if (key_is_minor(get_key(tree))):
            rules_minor += t_rules
        else:
            rules_major += t_rules

rule_counter = collections.Counter(rules)
rule_counter = sorted(rule_counter.items(),key=lambda x:x[0])
# print(rule_counter)

# 確率パラメータ推定
for rule in rule_counter:
    #該当ルールをpickup
    target_rule_count = rule[1]
    parent = rule[0][0]
    same_parent_rule_counter = 0
    for rule_j in rule_counter:
        if rule_j[0][0] == parent:
            same_parent_rule_counter += rule_j[1]

    #print(rule[0] ,target_rule_count, "/" , same_parent_rule_counter)
    rule_with_prob[rule[0]] = target_rule_count / same_parent_rule_counter

#print(rule_with_prob)

# tonic生成ルール
with open(FILE_TONIC_CHORD,'w') as f:
    for root in flats.values():
        for chord_type in tonic_chord_type:
            chord_type = replace_badsymbol(chord_type)
            f.write(root + chord_type +"\n")

# 文法作成
with open(FILE_NAME_GRAMMAR,'w') as f:
    for i in rule_with_prob:
        #print(i)
        f.write(i[0]+ " -> "+ i[1][0] +" "+ i[1][1] + " [" + str (rule_with_prob[i]) +"]" + "\n")