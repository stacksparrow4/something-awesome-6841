#include <stdio.h>

int main() {
  char buf[4];

  printf("Enter an integer:\n");
  fgets(buf, 10, stdin);
  printf("You entered %s\n", buf);
}
