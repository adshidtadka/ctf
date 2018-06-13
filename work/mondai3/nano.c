#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(void)
{
	char shellcode[140];
	fread(shellcode, 1, 140, stdin);
	setreuid(geteuid(), -1);
	(*(void (*)())shellcode)();
	return 0;
}
