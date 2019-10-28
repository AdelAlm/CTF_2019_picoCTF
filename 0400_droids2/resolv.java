class Test {

  public static void main(String[] args){

      String[] witches = {"weatherwax", "ogg", "garlick", "nitt", "aching", "dismass"};
      int second = 3 - 3;
      int third = (3 / 3) + second;
      int fourth = (third + third) - second;
      int fifth = 3 + fourth;
      int sixth = (fifth + second) - third;
      String str = ".";
      System.out.println("".concat(witches[fifth]).concat(str).concat(witches[third]).concat(str).concat(witches[second]).concat(str).concat(witches[sixth]).concat(str).concat(witches[3]).concat(str).concat(witches[fourth]));
        
  }
}

/*We execute this code and get the good input, and the app give the flag
 * picoCTF{what.is.your.favourite.colour} */
