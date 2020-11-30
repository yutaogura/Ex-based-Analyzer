"""
Created on Mon Sep 15 2020

Incremental_chart_Parsing_main 

デバッグしたいところにこれブチ込む
import pdb; pdb.set_trace()


@author:yuta ogura
"""

import incremental_chart
import svgtree

def main():
    # #文法作成
    # grammar_generator.main()
    #漸進的構文解析
    incremental_chart.main()
    #svgで画像として出力 
    svgtree.main()    
if __name__ == "__main__":
    main()