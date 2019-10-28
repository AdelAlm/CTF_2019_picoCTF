class Test {

  public static void main(String[] args){

      String str = "aaa";
      StringBuilder ace = new StringBuilder(str);
      StringBuilder jack = new StringBuilder(str);
      StringBuilder queen = new StringBuilder(str);
      StringBuilder king = new StringBuilder(str);
      ace.setCharAt(0, (char) (ace.charAt(0) + 4));
      ace.setCharAt(1, (char) (ace.charAt(1) + 19));
      ace.setCharAt(2, (char) (ace.charAt(2) + 18));
      jack.setCharAt(0, (char) (jack.charAt(0) + 7));
      jack.setCharAt(1, (char) (jack.charAt(1) + 0));
      jack.setCharAt(2, (char) (jack.charAt(2) + 1));
      queen.setCharAt(0, (char) (queen.charAt(0) + 0));
      queen.setCharAt(1, (char) (queen.charAt(1) + 11));
      queen.setCharAt(2, (char) (queen.charAt(2) + 15));
      king.setCharAt(0, (char) (king.charAt(0) + 14));
      king.setCharAt(1, (char) (king.charAt(1) + 20));
      king.setCharAt(2, (char) (king.charAt(2) + 15));
      System.out.println("".concat(queen.toString()).concat(jack.toString()).concat(ace.toString()).concat(king.toString()));
  }
}

/*We execute this code and get the good input, and the app give the flag
 * Hello World
 * alphabetsoup
 * https://docs.microsoft.com/fr-fr/xamarin/android/deploy-test/signing/manually-signing-the-apk
 * http://www.wagiro.com/archivos/397
 * picoCTF{not.particularly.silly}
 * */
