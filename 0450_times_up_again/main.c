#include <stdlib.h>
#include <stdio.h>
#include <time.h>


int main () {

  int epoch;
  for (int i = 0; i < 100000; i++) {
    epoch = time(NULL)+i;
    srand(epoch);

    int is_ok = 0;
    int chances = 4;
    for (int j = 0; j < 20; j++) {
      int r = rand();
      //printf("Result -> %i\n", r);

      if (0 < r % 0x32)
        chances--;
        if (chances == 0)
          break;
      else
        is_ok++;
    }
    if (is_ok > 5)
      printf("%i -> %i (+%i)\n", epoch, is_ok, i);
  }

  return 0;
}
