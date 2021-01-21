# 進捗メモ

## 1/22分(1/15~1/22)
- とりあえず修論を（実験を含めて）最後まで書いた
  - 添削まち

- 楽曲解析
  - take the a train
    - 漸進的解析の概要(図の読み方)
  - autumn leaves 
    - 平行調での転調
    - ルート遷移図
  - lady bird 
    - 複数の調への転調，意外性の評価
    - ルート遷移図



# 実験メモ

## 実験条件メモ

###  文法規則
- Chord Quallity
  - {C,Db,...,B} × {M7, M, m7, m, 7, m6, aug, aug7, hdim7, o, o7, sus, sus4} = **156パターン 実際は92かも**
  - テンションなどはなし
- Total grammar number：**584** <!-- TODO　この数本当に合ってる？　確認して3.3章の修正 -->
  - 調性(C Major keyへの)による正規化なし
  - (C Major / C minor　にマッピングすることも考えられる)
- Tonic 
  - global chartの初期状態として登録しておく開始規則
  - {C,Db,...,B} × {M7, M, m7, m} = **48パターン**
  - M6, m6を導入することも考えられる
###  漸進的チャートパーサ
#### 枝刈り
コード進行が長くなると（単語数が増えると），global chart（トップダウンで先頭からの解析結果を保持していくチャート）内の項が指数関数的に増え，計算量も指数関数的に増えることへの対処法

確率順に並べたときに上位n個だけ残す
- 本当にこれをしてしまって良いのか？

- 次ステップに残すglobal chart内の項の数： **100**

  
## 解析楽曲

### Take The A Train コレ!
- JHT掲載なし
#### コード進行
```
[A]
CM7 CM7 D7 D7
Dm7 G7 CM7 Dm7 G7
[A]
CM7 CM7 D7 D7
Dm7 G7 CM7 Gm7 C7
[B]
FM7 FM7 FM7 FM7
D7 D7 Dm7 G7
[A]
CM7 CM7 D7 D7
Dm7 G7 CM7 Dm7 G7
```
#### メモ

### Lady Bird コレ!
- JHT掲載あり
#### コード進行
```
CM7 CM7 Fm7 Bb7
CM7 CM7 Bbm7 Eb7
AbM7 AbM7 Am7 D7
Dm7 G7 (CM7 EbM7 AM7 DbM7)
```
JHTは()部分がCM7で簡略化

<!-- <img src="***画像URL***" width="***サイズ***"> -->
#### コード・アナライズ
![](./fig/lady.jpeg)

### Red Clay
```
Cm7 Bbm7 Dbsus Ebsus Fsus Gsus Cm7 Bbm7 Eb7 AbM7 Dhdim7 G7 Cm7
```

### Afternoon in Paris
```
CM7 Cm7 F7 BbM7 Bbm7 Eb7 AbM7 Dm7 G7 CM7
```

### There will never be another you
```
EbM7 EbM7 Dhdim7 G7 Cm7 F7 Bbm7 Eb7 AbM7 
```

### All the things you are 

### Autumn leaves コレ！
```
Cm7 F7 BbM7 EbM7 Ahdim7 D7 Gm7 Cm7
```


#### メモ

## 考察
- セクションを跨ぐ解析はあまり意味がなさそう
- 同じクオリティを同一視するような規則が必要かもしれない 