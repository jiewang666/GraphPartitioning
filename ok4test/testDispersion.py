#!/usr/bin/python
# -*- coding: utf-8 -*-

# 用于测试给定数据集和窗口策略下的离散度

import random
import math
import time

time_start = time.time()

# 划分子图数量
numOfParts = 21000

# 存储总边数
edgeNum = 0
# 窗口初始大小
windowsize = 16997*90
# 每次分配边的比例
AssignProportion = 0.01

# [[(src, dst), (src, dst),...],[()],[()]....]          每个分区对应的边集合
Partitions = [[] for i in range(numOfParts)]
# { part:set(v1,v2,...), ... }                          存储每个分区对应的点
vertexDic = {}
# { vertex:set(part1, part2,...),... }                  存储每个点对应的分区
ver2partDic = {}

edges = []
window = []
f = open("/home/w/ba-bfs-edges.txt", "r")
for line in f:
    srcTar = line.strip().split()
    if(srcTar[0] == '#'):
        continue
    src = long(srcTar[0])
    tar = long(srcTar[1])
    edges.append((src, tar))

for i in range(numOfParts):
    vertexDic[i] = set()

line = 0  # 记录当前处理的是第几条边
while(line < len(edges)):
    while(len(window) < windowsize and line < len(edges)):   # 将窗口填满，或者是最后一点了
        window.append(edges[line])
        line = line + 1
    if(len(window) < windowsize):                            # 最后一点时，修正windowsize
        windowsize = len(window)
    print "windowsize: " + str(windowsize)
    random.shuffle(window)
    if(line == len(edges)):
        AssignProportion = 1
    removeLen = int(len(window) * AssignProportion)
    # 进行本轮的分配
    for i in range(removeLen):
        src = window[i][0]
        tar = window[i][1]

        edgeNum = edgeNum + 1
        if edgeNum % 100000 == 0:
            print edgeNum
        
        # 更新src和tar所存在的Partition和全局的度信息
        if(ver2partDic.has_key(src)):
            srcMachines = ver2partDic[src]
        else:
            ver2partDic[src] = set()
            srcMachines = ver2partDic[src]
        if(ver2partDic.has_key(tar)):
            tarMachines = ver2partDic[tar]
        else:
            ver2partDic[tar] = set()
            tarMachines = ver2partDic[tar]

        # 开始根据策略对边进行分配
        if (len(srcMachines) == 0) and (len(tarMachines) == 0):      # A(u) 和 A(v) 都是空集  选择边数量最少的子图加入
            part = -1
            for i in range(numOfParts):
                if part == -1:
                    part = i
                    continue 
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        elif (len(srcMachines) > 0) and (len(tarMachines) == 0):
            part = -1
            for i in srcMachines:
                if part == -1:
                    part = i
                    continue
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        elif (len(srcMachines) == 0) and (len(tarMachines) > 0):
            part = -1
            for i in tarMachines:
                if part == -1:
                    part = i
                    continue
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        elif ((len(srcMachines) > 0) and len(tarMachines) > 0):
            Intersection = srcMachines & tarMachines
            Convergence = srcMachines | tarMachines
            if (len(Intersection) > 0):
                part = -1
                for i in Intersection:
                    if part == -1:
                        part = i
                        continue
                    if len(Partitions[i]) < len(Partitions[part]):
                        part = i
            elif (len(Intersection) == 0):
                part = -1
                for i in Convergence:
                    if part == -1:
                        part = i
                        continue
                    if len(Partitions[i]) < len(Partitions[part]):
                        part = i

        # 得到target part，更新相关数据
        Partitions[part].append((src, tar))
        vertexDic[part].add(src)
        vertexDic[part].add(tar)
        ver2partDic[src].add(part)
        ver2partDic[tar].add(part)
        
    # 修正窗口大小和内容
    window = window[removeLen:windowsize]

# 全部分配完成，统计数据
# 获取所有子图的顶点个数    
allVertex = 0L
maxVertices = 0L
minVertices = 1000000000L
for i in range(numOfParts):
    allVertex = allVertex + len(vertexDic[i])
    print len(vertexDic[i])
    if maxVertices < len(vertexDic[i]):
        maxVertices = len(vertexDic[i])
    if minVertices > len(vertexDic[i]):
        minVertices = len(vertexDic[i])
# 获取整个图的顶点个数
vertexAll = vertexDic[0]
for i in range(1, numOfParts):
    vertexAll.update(vertexDic[i])
# 获取顶点的LSD和LRSD
temp = 0L
AveVerSize = len(vertexAll)/float(numOfParts)
for i in range(0, numOfParts):
    temp = temp + (len(vertexDic[i]) - AveVerSize) * (len(vertexDic[i]) - AveVerSize)
temp = temp/numOfParts
temp = math.sqrt(temp)

VLSD = temp
VLRSD = VLSD/AveVerSize

VRF = allVertex/float(len(vertexAll))

# 获取边的相关信息
maxEdges = 0L
minEdges = 1000000000L
AveSize = edgeNum/float(numOfParts)
temp = 0L
ans = 0
for i in range(numOfParts):
    temp = temp + (len(Partitions[i]) - AveSize) * (len(Partitions[i]) - AveSize)
    if maxEdges < len(Partitions[i]):
        maxEdges = len(Partitions[i])
    if minEdges > len(Partitions[i]):
        minEdges = len(Partitions[i])
    if(len(Partitions[i])>0):
        ans = ans+1

temp = temp/numOfParts
temp = math.sqrt(temp)

LSD = temp
LRSD = LSD/AveSize

print edgeNum
# 依次是 VRF  LSD  LRSD  VLSD  VLRSD  子图点最大值  子图点平均值  子图边最大值  子图边平均值
# print VRF, LSD, LRSD, VLSD, VLRSD, maxVertices, allVertex/numOfParts, maxEdges, edgeNum/numOfParts
# print "VRF " + str(VRF)
# print "max-edges " + str(maxEdges)
# print "min-edges " + str(minEdges)
# print "avg-edges " + str(edgeNum/numOfParts)
# print "max-vertices " + str(maxVertices)
# print "min-vertices " + str(minVertices)
# print "avg-vertices " + str(allVertex/numOfParts)
# print "LRSD " + str(LRSD)
# print "VLRSD " + str(VLRSD)

time_end = time.time()
time_used = time_end - time_start
print "time " + str(time_used)
print "ans " + str(ans)