var wordlist = [];
var wordlistLoaded = false;
var gw = [];

function wordInSet(word, charString) {
  var charsRemaining = charString.slice();
  for (var i = 0; i < word.length; i++) {
    var ch = word[i];
    var index = charsRemaining.indexOf(ch);
    if (index == -1) {
      index = charsRemaining.indexOf('.');
      if (index == -1) {
        return false;
      }
    }
    charsRemaining = charsRemaining.slice(0, index) + charsRemaining.slice(index + 1);
  }
  return true;
}

function sortfunc(x,y) {
  if (x.length < y.length) {
    return -1;
  }
  if (x.length > y.length) {
    return 1;
  }
  if (x < y) {
    return -1;
  }
  if (x > y) {
    return 1;
  }
  return 0;
}

function inputChanged() {
  var charString = document.getElementById("characters").value.toLowerCase();
  var regex = new RegExp(document.getElementById("regex").value.toLowerCase());

  findWords(wordlist, charString, function (goodWords) {
    var filteredWords = goodWords.filter(function (word) {
      return word.match(regex);
    });
    document.getElementById("results").textContent = filteredWords.join("\n");
    gw = goodWords;
  })
}

function findWords(wordlist, charString, callback) {
  var goodWords = [];
  for (var i = 0; i < wordlist.length; i++) {
    var word = wordlist[i];
    if (wordInSet(word, charString)) {
      goodWords.push(word);
    }
  }
  goodWords.sort(sortfunc);
  goodWords.reverse();
  callback(goodWords);
}

var isNode=new Function("try {return this===global;}catch(e){return false;}");

if (isNode()) {
  module.exports.wordInSet = wordInSet;
  module.exports.findWords = findWords;
}
