// load Unit.js module
var test = require('unit.js');
var wordsearch = require('./wordsearch.js');


describe("wordInSet", function () {
  function testCase(word, charset, expected) {
    it((expected ? "finds '" : "does not find '") + word + "' in charSet '" + charset + "'", function () {
      test.assert(wordsearch.wordInSet(word, charset) === expected);
    });
  };

  testCase('a', 'aa', true);
  testCase('aa', 'a', false);
  testCase('hi', 'herti', true);
  testCase('there', 'herti', false);
  testCase('dude', 'herti', false);
  testCase('dude', 'dde.', true);
  testCase('dude', 'd.e.', true);
  testCase('dude', 'de.', false);
});

describe("findWords", function () {
  it("works", function () {
    var wordlist = ["hi", "there", "dude"];
    var charset = "herti";
    wordsearch.findWords(wordlist, charset, function (goodWords) {
      test.value(goodWords)
        .contains(["hi"])
        .notContains(["there", "dude"])
    });
  });
});
