// Object.freezeを使用しないと外部で値を書き換えることが出来る
// Object.freezeはネストしたオブジェクトまで見ないので、Objectの中でObjectを宣言する場合、宣言するObjectにもObject.freezeをつける
export default Object.freeze({
    Dm7 : ['D3', 'F4', 'A4', 'C5', 'E5'],
    G7 : ['G3', 'F4','A4','B4','D5'],
    CM7 : ['C3', 'E4', 'G4','B4','D5'],
    A7 : ['A3', 'Db4','E4','G4', 'A4'],
  });