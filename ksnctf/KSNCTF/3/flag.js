// javascript flag.js
var flag = "";
var o = '';
var p = Array(70, 152, 195, 284, 475, 612, 791, 896, 810, 850, 737, 1332, 1469, 1120, 1470, 832, 1785, 2196, 1520, 1480, 1449);
for (var i = 0; i < p.length; i++) {
  //pの値から本来入力するべき値を逆算する
  var o = p[i] / (i + 1);
  //Strings.fromCode(o)でoの数値をUnicodeの文字に戻す
  var flag = flag + String.fromCharCode(o);
};
console.log(flag);
