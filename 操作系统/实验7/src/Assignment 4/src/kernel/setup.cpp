#include "asm_utils.h"
#include "interrupt.h"
#include "stdio.h"
#include "program.h"
#include "thread.h"
#include "sync.h"
#include "memory.h"

// 屏幕IO处理器
STDIO stdio;
// 中断管理器
InterruptManager interruptManager;
// 程序管理器
ProgramManager programManager;
// 内存管理器
MemoryManager memoryManager;

void first_thread(void *arg)
{
    char *p1 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 6);
    char *p2 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 5);

    //模拟访问页面0
    int virtual_addr = memoryManager.kernelVirtual .startAddress + 0* PAGE_SIZE; 
    //求出虚拟地址的页目录项
    unsigned int* pte = (unsigned int*)(0xffc00000 + ((virtual_addr & 0xffc00000) >> 10) + (((virtual_addr & 0x003ff000) >> 12) * 4)); 
    (*pte) = (*pte) | (1<<5);

    //延时
    for(int cnt = 0; cnt < 1e7; cnt++){}
    char *p3 = (char *)memoryManager.allocatePages(AddressPoolType::KERNEL, 3);
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

    // 内存管理器
    memoryManager.openPageMechanism();
    memoryManager.initialize();

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
