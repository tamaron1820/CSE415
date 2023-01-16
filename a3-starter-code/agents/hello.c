#include <stdio.h>
#include <string.h>
void  Swap(int x, int y)
{
    int  work;        /* 作業用 */

    work = x;        /* xの値を一時保存 */
    x = y;          /* xの値をyの値に書き換える */
    y = work;        /* yの値をxの値に書き換える */
}

void main(void)
{
    int  x = 10, y = 20;         /* int型の変数の宣言 */
                   /* pyはyのアドレスを指す */

    printf("　交換前: x = %d   y = %d\n", x, y);

    Swap(x, y);                /* アドレスを渡すので&が必要 */
    printf("　交換後: x = %d   y = %d\n", x, y);

}