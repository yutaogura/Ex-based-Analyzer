# 実験メモ

## 実験条件メモ

###  文法規則
- Total grammar number 584 <!-- TODO　この数本当に合ってる？　確認して3.3章の修正 -->
  - 調性(C Major keyへの)による正規化なし
  - (C Major / C minor　にマッピングすることも考えられる)
- Tonic 
  - {C,Db,...,B} ×  {M7, M, m7, m} = 48パターン
  - M6, m6をいれることも考えられる
###  漸進的チャートパーサ
- 次ステップに残すglobal chart内の項の数 100
  - 確率順に並べたときに上位n個
  - 本当に良いのか？
  
## 解析楽曲

### Take The A Train
#### コード進行
```
[A]
CM7 CM7 D7 D7 Dm7 G7 CM7 Dm7 G7 
[A]
CM7 CM7 D7 D7 Dm7 G7 CM7 Dm7 G7
[B]

[A]
CM7 CM7 D7 D7 Dm7 G7 CM7 Dm7 G7 
```
#### メモ

### Lady Bird
#### コード進行
```
CM7 CM7 Fm7 Bb7 CM7 CM7 Bbm7 Eb7 AbM7 AbM7 Am7 D7 Dm7 G7 CM7
```

## 考察
- セクションを跨ぐ解析はあまり意味がなさそう
- 同じクオリティを同一視するような規則が必要かもしれない 