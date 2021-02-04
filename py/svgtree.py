import svgling
import svgling.html
import svgling.figure
# from svgling.figure import SideBySide, RowByRow, Caption
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPM 
# import cairosvg
import subprocess
import os
import pandas as pd
import glob
import shutil
# read pkl data

# 各ステップごとにいくつ木を描くか？
DRAWING_THRESHOLD=50 
PKL_DATA_PATH = "./py/temp/"
SVG_DATA_PATH = "./py/svg/"
def main():

    #svgディレクトリの中を空っぽに(作り直す)
    files = os.listdir(SVG_DATA_PATH)
    if files: #なんか入ってたら
        shutil.rmtree(SVG_DATA_PATH) #消して
        os.mkdir(SVG_DATA_PATH) #作る

    #tempフォルダ内のファイルを読み込む
    files = os.listdir(PKL_DATA_PATH)
    print(files)

    for step_idx, pkl_file_name in enumerate(files):

        #svgファイルの保存場所確保
        parsed_chord = pkl_file_name.replace(".pkl","")
        # print(parsed_chord)
        svg_save_dir = SVG_DATA_PATH+parsed_chord   
        if not os.path.exists(svg_save_dir):
            os.makedirs(svg_save_dir)

        #pkl展開->tree書き出し
        trees = pd.read_pickle(PKL_DATA_PATH + pkl_file_name)
        # print(trees)

        for idx,tree in enumerate(trees):
            if idx < DRAWING_THRESHOLD:
                data = tree['tree'] 
                svg_image = svgling.draw_tree(data,leaf_nodes_align=True)
                # id あり
                # svg_image.get_svg().saveas(svg_save_dir+"/"+ "rank_" + str(idx) +"id_"+str(tree['id'])+"prob_"+str(tree['prob'])+".svg",pretty=True)
                # id なし
                svg_image.get_svg().saveas(svg_save_dir+"/"+"step_" + '{0:03d}'.format(step_idx) + "rank_" + '{0:03d}'.format(idx) +"prob_"+str(tree['prob'])+".svg",pretty=True)


if __name__ == "__main__":
    main()

