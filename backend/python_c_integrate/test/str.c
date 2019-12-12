#include<stdio.h>

int check(char* s, char* t) {
	int i = 0;
	for(; s[i]!='\0' && t[i]!='\0'; i++)
		if(s[i] != t[i])
			return 0;
	if(s[i]=='\0' && t[i]=='\0')
		return 1;
	return 0;
}

int main() {
	char* s = "123456";
	char* t = "12456";
	//printf("%c", s[5]);
	printf("%d\n", check(s, t));
	return 0;
}
