#include <stdio.h>
void mystery(char *a,int *b,int c){
    int *d = b-1;
    c=*b+c;
    *b=c-*d;
    *d=*b-*d;
    a[2]=a[b-d];
}
int main(int argc,char **argv){
    char ant[4]="bed";
    int x[2];
    *x=6;
    x[1]=7;
    int y=4;
    int *z=&y;
    *z=*x;
    printf("%d %d %d %s\n",*x,x[1],y,ant);
    mystery(ant,x+1,y);
    printf("%d %d %d %s\n",*x,x[1],y,ant);
}