#include "address_pool.h"
#include "os_constant.h"
#include "stdio.h"

AddressPool::AddressPool()
{
}

// 设置地址池BitMap
void AddressPool::initialize(char *bitmap, const int length, const int startAddress)
{
    resources.initialize(bitmap, length);
    this->startAddress = startAddress;
    this->clock = 0;
    this->virtual_num = 5;
    for(int i = 0; i < 5; i++){
        this->LRU[i] = 0;
    }
}

// 从地址池中分配count个连续页
int AddressPool::allocate(const int count)
{
    int start = resources.allocate(count);
    return (start == -1) ? -1 : (start * PAGE_SIZE + startAddress);
}

// 释放若干页的空间
void AddressPool::release(const int address, const int amount)
{
    resources.release((address - startAddress) / PAGE_SIZE, amount);
}

void AddressPool::updateLRU() 
{ 
    clock++; 
    for (int i = 0; i < resources.length; i++) 
    { 
        if(!resources.get(i)) 
        // 如果该虚拟地址还未被占有，则跳过 
            continue; 
        //得到虚拟地址
        int virtual_addr = startAddress + i * PAGE_SIZE; 
        //求出虚拟地址的页目录项
        unsigned int* pte = (unsigned int*)(0xffc00000 + ((virtual_addr & 0xffc00000) >> 10) + (((virtual_addr & 0x003ff000) >> 12) * 4)); 
        //观察页目录项A位是否被访问过
        if((*pte) & (1<<5)) 
        { 
            printf("Accessing page %d\n", i); 
            LRU[i] = clock; 
            // 重新置零 
            (*pte) = (*pte) & (~ 3 << 5); 
        } 
    } 
} 

int AddressPool::swapout() 
{   
    //找出最早被访问的帧，来进行替换
    int min_time = clock + 1;
    int index = 0; 
    for (int i = 0; i < resources.length; i++) 
    {   
        if(!resources.get(i)){
            // 如果该虚拟地址还未被占有，则跳过 
            continue; 
        } 
        
        if(LRU[i] < min_time) 
        { 
            min_time = LRU[i]; 
            index = i; 
        } 
    } 
    //返回被替换帧的虚拟地址
    return startAddress + index * PAGE_SIZE;
}