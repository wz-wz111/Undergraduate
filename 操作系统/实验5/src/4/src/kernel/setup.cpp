#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include "program.h"
#include "thread.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;
// 程序管理器
ProgramManager programManager;

void third_thread(void *arg) {
    while(1) {
            for (int i = 0; i < 100000000000; i++)
                if(i % 100000000 == 0)
                    printf("pid %d name \"%s\": Hello World!,fpid is :%d,priority is %d,time:%d\n", programManager.running->pid, programManager.running->name,programManager.running->fpid,programManager.running->priority,programManager.running->ticksPassedBy);
    }
}
void second_thread(void *arg) {
    while(1) {
            for (int i = 0; i < 100000000000; i++)
                if(i % 100000000 == 0)
                    printf("pid %d name \"%s\": Hello World!,fpid is :%d,priority is %d,time:%d\n", programManager.running->pid, programManager.running->name,programManager.running->fpid,programManager.running->priority,programManager.running->ticksPassedBy);
    }
}
void first_thread(void *arg)
{
    // 第1个线程不可以返回
    printf("pid %d name \"%s\": Hello World!,fpid is :%d,priority is %d,time:%d\n", programManager.running->pid, programManager.running->name,programManager.running->fpid,programManager.running->priority,programManager.running->ticksPassedBy);
    if (!programManager.running->pid)
    {
        programManager.executeThread(second_thread, nullptr, "second thread", 1);
        //programManager.executeThread(third_thread, nullptr, "third thread", 1);
    }
    asm_halt();
}

void high_thread(void *arg) {
    while(1) {
            for (int i = 0; i < 100000000000; i++)
                if(i % 100000000 == 0)
                    printf("pid %d name \"%s\": Hello World!,fpid is :%d,priority is %d,time:%d\n", programManager.running->pid, programManager.running->name,programManager.running->fpid,programManager.running->priority,programManager.running->ticksPassedBy);
    }
}

void multithread(void *arg){
    //一开始先创建多个（10个）优先级不同的线程
    for(int i = 1; i < 6 ; i++){
        programManager.executeThread(second_thread, nullptr, "second thread", i%6);
        programManager.executeThread(third_thread, nullptr, "third thread", i%6);
    }
    while(1) {
            for (int i = 0; i < 100000000000; i++){
                if(i % 100000000 == 0){
                    printf("pid %d name \"%s\": Hello World!,fpid is :%d,priority is %d,time:%d\n", programManager.running->pid, programManager.running->name,programManager.running->fpid,programManager.running->priority,programManager.running->ticksPassedBy);
                }
                //创建一个优先级高的线程
                if(i  == 200000000){
                    programManager.executeThread(high_thread, nullptr, "high thread", 1);
                }
            }
    }
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
    int pid = programManager.executeThread(multithread, nullptr, "first thread", 1);
    if (pid == -1)
    {
        printf("can not execute thread\n");
        asm_halt();
    }

    ListItem *item = programManager.readyPrograms[1].front();
    PCB *firstThread = ListItem2PCB(item, tagInGeneralList);
    firstThread->status = RUNNING;
    programManager.readyPrograms[1].pop_front();
    programManager.running = firstThread;
    asm_switch_thread(0, firstThread);

    asm_halt();
}
