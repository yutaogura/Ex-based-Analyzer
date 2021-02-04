"""
Created on Mon Sep 14 2020

pyディレクトリの上から実行してください

Incremental_chart_Parsing 

CategoryとLexiconはこんな感じ
Category = ["S","I_C","II_C","V_C","II_G","V_G","V_Gb","II_Gb","V_D","II_D"]
Lexicon = {"Cmaj7":["I_Cmaj"],"Dmin7":["II_Cmaj"],"G7":["V_Cmaj"],"D7":["V_Gmaj"],"Emin7":["II_Dmaj"],"A7":["V_Dmaj"],"Amin7":["II_Gmaj"],"Abmin7":["II_Gbmaj"],"Db7":["V_Gbmaj"]}

デバッグしたいところにこれブチ込む
import pdb; pdb.set_trace()


@author:yuta ogura
"""

import copy
import re
import pandas as pd
import shutil
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import collections
import datetime
import csv


#ログファイル
FILE_NAME = "./py/chart2.log"

#ログ形式 
#LOG_FORMAT = 0  #readable format
#LOG_FORMAT = 1 #tex format
LOG_FORMAT = 2  #cairosvg format
TEMP_DIR_PATH = "./py/temp/"


#Analysis target 
ANALYSIS_TARGET_FILE = "./py/target.txt"
#inputファイル
FILE_NAME_NONTERMINAL = "./py/nonterminals.txt"
FILE_NAME_LEXICON = "./py/lexicon.txt"
FILE_NAME_GRAMMAR = "./py/pcfg.txt"
FILE_TONIC_CHORD = "./py/tonic.txt"
Category = []
Lexicon = {}
Grammar = []
#どの深さまでlocal_chartを展開するか？
Depth_Limit = 5

REDUCTION_TREE = True
SURVIVE_TREE_NUM = 100

Sentense_tmp = 0
root_count_by_step = []


"""
Rule class 
"""
class Rule:
    def __init__(self,left,right,prob=None):
        self.left = left   #String
        self.right = right #List
        self.prob = prob  #Float

    def print_rule(self):
        if self.prob:
            tot = self.left + " -> " + (' '.join(self.right)) + ' ['+str(self.prob)+']'
        else:
            tot = self.left + " -> " + (' '.join(self.right))
        return tot

"""
State class
"""

class State:
    def __init__(self,category,content,prob=1.0,decided = True):
        self.category = category   #String
        self.content = content   #[State] or []  List
        self.decided = decided 
        self.id = 0
        self.prob = prob

    def setId(self,id):
        self.id = id

    def print_state(self,str=""):
        tot = ''
        #[]リスト
        if len(self.content) == 0:
            if self.decided == True:
                tot = self.category
            else:
                tot = self.category + "\n" + str + "|- ?"

        # # #終端文字
        # elif len(self.content) == 1:
        #     tot =  self.category +"\n|- " + self.content[0].print_state()
        #Stateのリスト
        else: 
            tot = self.category
            for s in self.content:
                tot = tot + "\n" + str + "|-" +s.print_state(str + "  ")
        return tot

    def print_state_tex(self):
        tot = ''
        #[]リスト
        if len(self.content) == 0:
            if self.decided == True:
                tot = "{\\rm " + self.category + "}"
            else:
                tot = "[?]_{\\rm "+self.category + "}"
        # # #終端文字
        # elif len(self.content) == 1:
        #     tot =  self.category +"\n|- " + self.content[0].print_state()
        #Stateのリスト
        else: 
            tot = ""
            m = ""
            for s in self.content:
                #print(m + "=>")
                m =  m + s.print_state_tex()
                tot = "[" + m + "]" + "_{\\rm " + self.category + "}"

        #print("<=" + tot)        
        return tot

    #タプルを返す    
    def print_state_cairo(self):
        tot = ''
        #空リスト
        if len(self.content) == 0:
            if self.decided == True:
                tot = '\"'+self.category+'\"' 
            else:
                tot = '\"'+self.category+'\"'  
        # # #終端文字
        # elif len(self.content) == 1:
        #     tot =  self.category +"\n|- " + self.content[0].print_state()
        #Stateのリスト
        else: 
            tot = ""
            m = ""
            for s in self.content:
                #print(m + "=>")
                m =  m + ", " + s.print_state_cairo()
                tot = '(\"'+self.category+'\"' + m + ' )'

        #print("<=" + tot)        
        return tot

    def return_state_list(self):
        if len(self.content) == 0:
            if self.decided == True:
                tot = self.category
            else:
                tot = [self.category,"?"]
        else:
            tot = []
            tot.append(self.category)
            for s in self.content:
                tot.append(s.return_state_list())
        return tot

    def print_id(self):
        return str(self.id) 

    #木の深さを返す
    def return_height(self,height=0):
        height = height + 1
        for s in self.content:
            height = s.return_height(height)

        return height

    #深さ優先で最左未決定項を探す
    def lvt(self,temp=""):
        #print("-> " + self.category)
        #停止条件
        if self.content == []:
            if self.decided == False:
                if temp == "":
                    return self.category
                else:
                    return temp
            else:
                return ""

        for s in self.content:
            temp = s.lvt(temp)
            #print("temp := " + temp) 
        
        return temp

    #項の置き換え
    def replace(self,term,flag=True):
        if self.content == []:
            if (self.decided == False) and (flag):
                #print("(rewrite)==>" + self.category + str(flag))
                self.content = term.content
                self.decided = True
                return False
        for s in self.content:
            #print("==>" + s.category + str(s.decided)+str(flag))
            flag = s.replace(term,flag)

        return flag

"""
Chart class
"""

class Chart:
    def __init__(self):
        self.chart = [] #List
        self.number = 1

    def push(self,state):
        self.chart.append(state)
        state.setId(self.number)
        self.number += 1

    def reduce(self,survive_num):
        whole = []
        for s in self.chart:
            x = {}
            x['id'] = s.id
            x['prob'] = s.prob 
            whole.append(x) 
        whole_sorted = sorted(whole,key=lambda x:x['prob'],reverse = True)
        new_chart = []
        for x in whole_sorted[:survive_num]:
            for s in self.chart:
                if x['id'] == s.id:
                    new_chart.append(s)
        
        self.chart = new_chart

        

    def print_chart(self):
        for s in self.chart:
            prob = "prob : " + str(s.prob) #HACK:もうちょいきれいに
            readable_log = "(" + s.print_id() + ") "+ prob +  "\n" + s.print_state()
            tex_log = "(" + s.print_id() + ") "+ prob +  "\n" + "$" + s.print_state_tex() + "$"
            cairo_log = "(" + s.print_id() + ") "+ prob +  "\n" + s.print_state_cairo()
            print(readable_log)
            if LOG_FORMAT==0:
                logging(readable_log+'\n')
            elif LOG_FORMAT==1:
                logging(tex_log+'\n')
            elif LOG_FORMAT==2:
                tuple_var = ()
                logging(cairo_log+'\n')  
            else:
                pass

    def print_max_prob(self):
        max_prob = 0
        for s in self.chart:
            if s.prob > max_prob :
                max_prob = s.prob
        print("max prob:",max_prob)
                
    def print_min_prob(self):
        min_prob = 1
        for s in self.chart:
            if s.prob < min_prob :
                min_prob = s.prob
        print("min prob:",min_prob)

    def save_probhist(self):
        global Sentense_tmp
        fig = plt.figure()
        x = []
        for s in self.chart:
            x.append(s.prob)
        xd = sorted(x,reverse = True) 
        plt.hist(xd[:100], bins=50) #上位100だけhistogramに追加
        fig.savefig("./py/hist/time"+str(Sentense_tmp)+".png") # この行を追記  
        Sentense_tmp = Sentense_tmp + 1

    def count_root(self):
        global root_count_by_step
        
        categories = [(c.category) for c in self.chart]
        cs = collections.Counter(categories)
        root_count_by_step.append(cs)

    def get_chart(self):
        return self.chart


"""
util function
"""

def category_generator(file_name):
    global Category

    with open(file_name, 'r') as f:
        non_terminals = [v.rstrip() for v in f.readlines()]
    Category.extend(non_terminals)
    #print(Category)

def lexicon_generator(file_name):
    global Lexicon

    with open(file_name, 'r') as f:
        rules = [v.rstrip() for v in f.readlines()]
    
    for r in rules:
        array = r.split(' ')
        key = array[2]
        value = array[0]
        Lexicon.setdefault(key,[]).append(value)
    #print(Lexicon)

def grammar_generator(file_name):
    global Grammar
    with open(file_name, 'r') as f:
        rules = [v.rstrip() for v in f.readlines()]
    
    for r in rules:
        array = r.split(' ')
        lhs = array[0]
        rhs = []
        include_prob = False
        prob = 0.0 
        for rh in array[2:] :
            result = re.search(r'\[(.*)\]',rh)
            if result:
                #matchする->確率部である 
                prob = float(result.groups()[0])
                include_prob = True
                #print(prob)
            else:
                #ただの右辺
                #print(rh)
                rhs.append(rh)  
                
        if include_prob:
            #確率あり
            Grammar.append(Rule(lhs,rhs,prob))
        else:
            #確率なし
            Grammar.append(Rule(lhs,rhs))

def logging(str):
    with open(FILE_NAME, 'a') as f:
                f.write(str)


'''
Chart_Parsing本体
'''
def Chrat_Parsing(global_chart,w):
    local_chart = Chart()
    temp = Chart()
    
    # print("===init===")
    # print("Global")
    st ="========= " + w + " is inputed =========\n"
    #logging(st)
    # print(st)
    # global_chart.print_chart()
    #step1 Consulting Dictionary
    for cat in Category:  
        if cat in Lexicon[w]:
            local_chart.push(State(cat,[State(w,[])],1.0))
    print("===step1===")
    # print("Local")
    st = "===step1===\n===Local===\n"
    #logging(st)
    #local_chart.print_chart()

    #step2 Application Rules
    already_used_lrules = [] 
    #下記local_chartの中で同じ左再帰ルール適用は一度だけ
    for a in local_chart.get_chart():
        # print("\n==state==")
        # print("height : "+ str(a.return_height()))
        # print(a.print_state())
        # a: State
        #木の深さチェック
        if( a.return_height() < Depth_Limit):
            for g in Grammar:
                # g : each grammar
                #左再帰ルールチェック
                if(g.left == g.right[0]): 
                    #左再帰だった時
                    #既に使われていないか？
                    if(g not in already_used_lrules):
                        #ルール適用可能か?(右辺の第一項が現在のlocal chartのカテゴリと等しいか？)
                        if g.right[0] == a.category:
                            subseq = [a]
                            for right in g.right[1:]:
                                subseq.append(State(right,[],decided=False))
                            # print("grammar->",g.print_rule())
                            #TODO:g.probがNoneの時の処理    
                            local_chart.push(State(g.left,subseq,a.prob*g.prob))
                        already_used_lrules.append(g)
                else:
                    #左再帰ではなかった時  
                    #ルール適用可能か?(右辺の第一項が現在のlocal chartのカテゴリと等しいか？)    
                    if g.right[0] == a.category:
                        subseq = [a]
                        for right in g.right[1:]:
                            subseq.append(State(right,[],decided=False))
                        # print("grammar-->",g.print_rule())
                        #TODO:g.probがNoneの時の処理    
                        local_chart.push(State(g.left,subseq,a.prob*g.prob))
    print("===step2===")
    # print("Local")
    st = "===step2===\n===Local===\n"
    #logging(st)
    #local_chart.print_chart()    

    print("===step3===")        
    #step3 Replacing Terms

    for g in global_chart.get_chart():
        for l in local_chart.get_chart():
            if g.lvt() == l.category:
                #print("match")
                #print(g.print_state())
                #print("g.lvt() = " + g.lvt())
                t = copy.deepcopy(g)
                # print("tree:")
                # print(t.print_state())
                # print(t.prob)
                # print("local:")
                # print(l.print_state()) 
                # print(l.prob)
                t.replace(l) #項の置き換え
                #挿入するlocal_chartの確率を掛け算
                t.prob  = t.prob * l.prob
                #print(t.print_state())
                temp.push(t)
                #print("----------------")
    global_chart = temp
    print("global_len(pre reduction)",len(global_chart.get_chart()))

    if REDUCTION_TREE:
        print("===step4===")        
        #step4 Chart Reduction
        global_chart.reduce(SURVIVE_TREE_NUM)


    # print("Global")
    # st = "===Global===\n"
    # logging(st)
    print("global_len",len(global_chart.get_chart()))
    global_chart.print_max_prob()
    global_chart.print_min_prob()
    global_chart.save_probhist()
    global_chart.count_root()
    # print("local_len",len(local_chart.get_chart()))
    # global_chart.print_chart()


    return global_chart
    

class ParseError(Exception):
    pass


def save_gchart(g_chart,parsed_chord="",step_num=0):
    trees = []
    for state in g_chart.get_chart():
        tree = state.return_state_list()
        trees.append({"id":state.id,"prob":state.prob,"tree":tree})
    sorted_trees = sorted(trees, key=lambda x:x['prob'], reverse=True)
    # print(sorted_trees[:5])

    # prob.csvを保存
    with open(TEMP_DIR_PATH+'{0:02d}'.format(step_num)+'prob.csv','w') as f:
        writer = csv.writer(f)
        for rank,tree in enumerate(sorted_trees):
            writer.writerow(['{0:03d}'.format(rank),tree['prob']])

    
    #pklで保存
    # HACK:↓消す    
    # pd.to_pickle(sorted_trees,TEMP_DIR_PATH+parsed_chord+".pkl")
    # HACK:↑消す
    pd.to_pickle(sorted_trees,TEMP_DIR_PATH+'{0:02d}'.format(step_num)+".pkl")


def set_root(g_chart):

    with open(FILE_TONIC_CHORD, 'r') as f:
        tonics = [v.rstrip() for v in f.readlines()]

    for tonic in tonics:
        g_chart.push(State(tonic,[],decided=False))           


def plot_linegraph():
    global root_count_by_step

    # genreの確定
    genes = {}
    for key in root_count_by_step[0].keys():
        genes[key] = []
    # genereに追加    

    # 最高頻度を記録
    max_count_value = 0

    for step in root_count_by_step:
        for key in step.keys():
            if key in genes.keys():
                if max_count_value < step[key]:
                    max_count_value = step[key]
                genes[key].append(step[key])

    genes_sorted = sorted(genes.items(), key=lambda x:len(x[1]), reverse=True)
    print(genes_sorted)


    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    fig.subplots_adjust(right=0.7)

    gene_limit = 6
    limit = 0
    for k,v in genes_sorted:
        ax.plot(v, label=k)
        limit = limit + 1
        if limit == gene_limit:
            break


    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=18)
    ax.set_xlabel("chord step")
    ax.set_ylabel("root count")
    ax.set_ylim(0, max_count_value) #ここのmaxを系列のmaxに

    now = datetime.datetime.now()
    fig.savefig("./py/linegraph/root.pdf")
    # fig.savefig("./py/linegraph/"+ now.strftime('%Y%m%d_%H%M%S') +".png")

def main():
    g_chart = Chart()


    set_root(g_chart)
    
    #　とりあえずC^7だけでやりたい時
    # g_chart.push(State("C^7",[],decided=False))


    #なんか入ってたら削除
    for f in glob.glob(TEMP_DIR_PATH+'/*.pkl'):
        os.remove(f)

    with open(ANALYSIS_TARGET_FILE,"r") as f:
        line = f.read().replace('\n','')
    words = line.split(" ")
    
    #words = ["Dmin7","G7","Emin7","A7","Amin7","D7","Abmin7","Db7","Cmaj7"]
    #words = ["Dmin7","G7","Cmaj7"]

    with open(FILE_NAME, 'w') as f:
        f.write("input sequence : ")
        for s in words:
            f.write(s + " ")
        f.write("\n")

    category_generator(FILE_NAME_NONTERMINAL)
    lexicon_generator(FILE_NAME_LEXICON)
    grammar_generator(FILE_NAME_GRAMMAR)

    # print()
    
    #Grammar表示
    # for g in Grammar:
    #      print(g.print_rule())


    #temp(作業)ディレクトリの中を空っぽに(作り直す)
    files = os.listdir(TEMP_DIR_PATH)
    if files: #なんか入ってたら
        shutil.rmtree(TEMP_DIR_PATH) #消して
        os.mkdir(TEMP_DIR_PATH) #作る

    # ステップ対応表作成
    step_list = []
    for idx, chord_symbol in enumerate(words):
        map_tuple = ['{0:02d}'.format(idx),chord_symbol]
        step_list.append(map_tuple)
    with open(TEMP_DIR_PATH+"map_step.csv",'w') as f:
        writer = csv.writer(f)
        writer.writerows(step_list)



    #解析本体
    try:
        for idx,w in enumerate(words):
            if g_chart is None:
                raise ParseError("Error! : Global Chart is empty")
            g_chart = Chrat_Parsing(g_chart,w)
            save_gchart(g_chart,"".join(words[:idx+1]),idx)    

    except ParseError as e:
        print(e)

    plot_linegraph() 

if __name__ == "__main__":
    main()