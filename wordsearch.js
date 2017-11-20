var wordlist = [];
var wordlistLoaded = false;
var gw = [];

function getWordlist(callback) {
  var request = new XMLHttpRequest();
  request.open('GET', 'scrabble.txt', true);
  request.send(null);
  request.onreadystatechange = function () {
    if (request.readyState === 4 && request.status === 200) {
      var type = request.getResponseHeader('Content-Type');
      if (type.indexOf("text") !== 1) {
        var wordlist = request.responseText.split('\n').slice(0,-1);
        callback(wordlist);
      }
    }
  }
}

function wordInSet(word, charString) {
  var charSet = new Set(charString.split(''));
  for (var i = 0; i < word.length; i++) {
    var letter = word[i];
    if (!charSet.has(letter)) {
      return false;
    }
    charSet.delete(letter);
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
  var charString = document.getElementById("characters").value;
  var regex = new RegExp(document.getElementById("regex").value);

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

(function () {
  getWordlist(function (wl) {
    wordlist = wl;
    wordlistLoaded = true;
    //findWords(wordlist, "rstlne", function (gw) {
      //console.log(gw);
      //goodWords = gw;
    //});
  });
})()
