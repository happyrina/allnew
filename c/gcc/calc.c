#include <stdio.h>
#include "libmy.h"

void main() {
  int x, y;
  printf("Input two numbers : ");
  scanf("%d %d", &x, &y);
<<<<<<< HEAD
  printf("%d + %d = %d\n", x, y, plus(x, y));
=======
  printf("%d + %d = %d\n", x, y, plus(x,y));
>>>>>>> bafb65b (super)
  printf("%d - %d = %d\n", x, y, minus(x, y));
}
