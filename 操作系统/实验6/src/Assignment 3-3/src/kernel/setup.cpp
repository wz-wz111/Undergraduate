#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include "program.h"
#include "thread.h"
#include "sync.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;
// 程序管理器
ProgramManager programManager;

Semaphore chopstick[5];


// void a_mother(void *arg)
// {
//     semaphore.P();
//     int delay = 0;

//     printf("mother: start to make cheese burger, there are %d cheese burger now\n", cheese_burger);
//     // make 10 cheese_burger
//     cheese_burger += 10;

//     printf("mother: oh, I have to hang clothes out.\n");
//     // hanging clothes out
//     delay = 0xfffffff;
//     while (delay)
//         --delay;
//     // done

//     printf("mother: Oh, Jesus! There are %d cheese burgers\n", cheese_burger);
//     semaphore.V();
// }

// void a_naughty_boy(void *arg)
// {
//     semaphore.P();
//     printf("Wz   : Look what I found!\n");
//     // eat all cheese_burgers out secretly
//     cheese_burger -= 10;
//     // run away as fast as possible
//     semaphore.V();
// }

void first_philosopher(void* arg){
    while(1){
        for(int cnt = 0; cnt < 100000000; cnt++){}
        chopstick[4].P();
        printf("The first_philosopher(7371) got 4 \n");

        for(int cnt = 0; cnt < 1000000000; cnt++){}
        chopstick[0].P();
        printf("The first_philosopher(7371) got 0 \n");

        printf("The first_philosopher(7371) is eating \n");
        //延长吃饭时间
        for(int cnt = 0; cnt < 100000000; cnt++){}
        chopstick[4].V();
        chopstick[0].V();
        printf("The first_philosopher(7371) is full \n");
    }
}

void second_philosopher(void* arg){
    while(1){
        for(int cnt = 0; cnt < 100000000; cnt++){}
        chopstick[1].P();
        printf("The second_philosopher got 1 \n");

        for(int cnt = 0; cnt < 1000000000; cnt++){}
        chopstick[0].P();
        printf("The second_philosopher got 0 \n");

        printf("The second_philosopher is eating \n");

        chopstick[1].V();
        chopstick[0].V();
        printf("The second_philosopher is full \n");
    }
}

void third_philosopher(void* arg){
    while(1){
        for(int cnt = 0; cnt < 100000000; cnt++){}
        chopstick[1].P();
        printf("The third_philosopher got 1 \n");

        for(int cnt = 0; cnt < 1000000000; cnt++){}
        chopstick[2].P();
        printf("The third_philosopher got 2 \n");

        printf("The third_philosopher is eating \n");

        chopstick[1].V();
        chopstick[2].V();
        printf("The third_philosopher is full \n");
    }
}

void fourth_philosopher(void* arg){
    while(1){
        for(int cnt = 0; cnt < 100000000; cnt++){}
        chopstick[3].P();
        printf("The fourth_philosopher got 3 \n");

        for(int cnt = 0; cnt < 1000000000; cnt++){}
        chopstick[2].P();
        printf("The fourth_philosopher got 2 \n");

        printf("The fourth_philosopher is eating \n");

        chopstick[3].V();
        chopstick[2].V();
        printf("The fourth_philosopher is full \n");
    }
}

void fifth_philosopher(void* arg){
    while(1){
        for(int cnt = 0; cnt < 100000000; cnt++){}
        chopstick[3].P();
        printf("The fifth_philosopher got 3 \n");
        
        for(int cnt = 0; cnt < 1000000000; cnt++){}
        chopstick[4].P();
        printf("The fifth_philosopher got 4 \n");

        printf("The fifth_philosopher is eating \n");

        chopstick[3].V();
        chopstick[4].V();
        printf("The fifth_philosopher is full \n");
    }
}


void first_thread(void *arg)
{
    // 第1个线程不可以返回
    stdio.moveCursor(0);
    for (int i = 0; i < 25 * 80; ++i)
    {
        stdio.print(' ');
    }
    stdio.moveCursor(0);

    for(int i = 0; i < 5; i++){
        chopstick[i].initialize(1);
    }

    printf("Create first_philosopher\n");
    programManager.executeThread(first_philosopher, nullptr, "second thread", 1);
    printf("Create second_philosopher\n");
    programManager.executeThread(second_philosopher, nullptr, "third thread", 1);
    printf("Create third_philosopher\n");
    programManager.executeThread(third_philosopher, nullptr, "fourth thread", 1);
    printf("Create fourth_philosopher\n");
    programManager.executeThread(fourth_philosopher, nullptr, "fifth thread", 1);
    printf("Create fifth_philosopher\n");
    programManager.executeThread(fifth_philosopher, nullptr, "sixth thread", 1);

    asm_halt();
}

extern "C" void setup_kernel()
{

    // 中断管理器
    interruptManager.initialize();
    interruptManager.enableTimeInterrupt();
    interruptManager.setTimeInterrupt((void *)asm_time_interrupt_handler);

    // 输出管理器
    stdio.initialize();

    // 进程/线程管理器
    programManager.initialize();

    // 创建第一个线程
    int pid = programManager.executeThread(first_thread, nullptr, "first thread", 1);
    if (pid == -1)
    {
        printf("can not execute thread\n");
        asm_halt();
    }

    ListItem *item = programManager.readyPrograms.front();
    PCB *firstThread = ListItem2PCB(item, tagInGeneralList);
    firstThread->status = RUNNING;
    programManager.readyPrograms.pop_front();
    programManager.running = firstThread;
    asm_switch_thread(0, firstThread);

    asm_halt();
}
