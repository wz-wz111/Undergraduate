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

Semaphore semaphore;

int material[3];
// int cheese_burger;


void producer(void *arg){
    // 不断生产
    while(1){
        //i表示哪个不生产
        for(int i = 0; i < 3; i++){
            for(int cnt = 0; cnt < 80000000; cnt++){}
            semaphore.P();
            for(int j = 0; j < 3; j++){
                if(i != j){
                    material[j] = 1;
                }else{
                    material[j] = 0;
                }
            }
            semaphore.V();
        }
    }
}

void first_smoker(void *arg){
    while(1){
        for(int i = 0; i < 100000000; i++){
            int hold = 0;
            // semaphore.P();
            if(material[hold] == 0 && i %80000000 == 0){
                printf("heyhey first_smoker (7371) got one %d %d %d \n ",material[0],material[1],material[2]);
            }
            // semaphore.V();
        }
    }
}
void second_smoker(void *arg){
    while(1){
        for(int i = 0; i < 100000000; i++){
            int hold = 1;
            // semaphore.P();
            if(material[hold] == 0 && i %80000000 == 0){
                printf("heyhey second_smoker got one %d %d %d \n ",material[0],material[1],material[2]);
            }
            // semaphore.V();
        }
    }
}
void third_smoker(void *arg){
    while(1){
        for(int i = 0; i < 100000000; i++){
            int hold = 2;
            // semaphore.P();
            if(material[hold] == 0 && i %80000000 == 0){
                printf("heyhey third_smoker got one %d %d %d \n ",material[0],material[1],material[2]);
            }
            // semaphore.V();
        }
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

    for(int i = 0; i < 3; i++){
        material[i] = 0;
    }
    // cheese_burger = 0;
    semaphore.initialize(1);

    programManager.executeThread(producer, nullptr, "second thread", 1);
    programManager.executeThread(first_smoker, nullptr, "third thread", 1);
    programManager.executeThread(second_smoker, nullptr, "fourth thread", 1);
    programManager.executeThread(third_smoker, nullptr, "fifth thread", 1);

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
