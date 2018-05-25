//import Constants from './constants'
var Constants = require('constants');
console.log(Constants.sBox)

class AES {


  constructor() {
    this.sBox = Constants.sBox
    this.sBoxInverted = Constants.sBoxInverted
    this.roundConst = Constants.roundConst
    console.log('AES Created');
  }

  keyExpansion() {
    function rotWord() {};

    function subWord() {};
  };

  addRoundKey() {};

  mixColumns() {};
  reverseMixColumns() {};
  shiftRows() {};
  reverseShiftRows() {};

  subBytes() {};
  reverseSubBytes() {};

  encryptBlock(block, key) {
    addRoundKey();

    for (var i = 0; i < 9; i++) {
      subBytes();
      shiftRows();
      mixColumns();
      addRoundKey();
    }

    subBytes();
    shiftRows();
    addRoundKey();
  }

  decryptBlock(block, key) {}

  encrypt(source, key) {
    var cipher = [];
    var blocks = split(source, 16);
    var length = block.length
    for (var i = 0; i < length; i++) {
      cipher.push(encryptBlock(blocks[i], key))
    }
  }

  decrypt(cipher, key) {}
}

var aes = new AES();
console.log(aes.roundConst);
