#include <stdlib.h>

typedef void (*fp)();

void foo(){}

int main(int argc, const char *argv[])
{
	fp x = foo;
	if(x == foo)
		return 1;
	return 0;
}
