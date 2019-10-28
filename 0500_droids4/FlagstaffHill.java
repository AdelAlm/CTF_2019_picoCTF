package com.hellocmu.picoctf;

import android.content.Context;

public class FlagstaffHill {
  public static native String cardamom(String str);

  public static String getFlag(String input, Context ctx) {
    return cardamom(input);
  }
}

