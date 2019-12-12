//https://blog.csdn.net/jason314/article/details/5640969

/*
 *  fork_test.c
 *  version 1
 *  Created on: 2010-5-29
 *      Author: wangth
 */
/*
#include <unistd.h>
#include <stdio.h>
 
int main () 
{ 
	pid_t fpid; //fpid表示fork函数返回的值
	int count=0;
	fpid=fork(); 
	if (fpid < 0) 
		printf("error in fork!"); 
	else if (fpid == 0) {
		printf("i am the child process, my process id is %d\n",getpid()); 
		printf("我是爹的儿子\n");//对某些人来看着更直白。
		count++;
	}
	else {
		printf("i am the parent process, my process id is %d\n",getpid()); 
		printf("我是孩子他爹\n");
		count++;
	}
	printf("统计结果是: %d\n",count);
	return 0;
}
*/


/*
 *  fork_test.c
 *  version 2
 *  Created on: 2010-5-29
 *      Author: wangth
 */
#include <unistd.h>
#include <stdio.h>

int main(void)
{
   int i=0;
   printf("i son/pa ppid pid  fpid\n");
   //ppid指当前进程的父进程pid
   //pid指当前进程的pid,
   //fpid指fork返回给当前进程的值
   for(i=0;i<2;i++){
       pid_t fpid=fork();
       if(fpid==0)
    	   printf("%d child  %4d %4d %4d\n",i,getppid(),getpid(),fpid);
       else
    	   printf("%d parent %4d %4d %4d\n",i,getppid(),getpid(),fpid);
   }
   return 0;
}
