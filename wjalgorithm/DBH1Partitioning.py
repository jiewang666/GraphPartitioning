#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time

def DBH1AL(edgelist, numOfParts):
    f = open(edgelist, "r")
    initf = open(edgelist, "r")
    # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    vertexDic = {}
    # { vertex:degree,... }                         存储每个点对应的度信息
    ver2degreeDic = {}
    # 存储总边数
    edgeNum = 0
    
    # 调试变量
    flag = 0

    # DBH 好像是需要提前预处理以获得所有点的 degrees 信息

    for line in initf:
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])

        if ver2degreeDic.has_key(src):
            srcDegrees = ver2degreeDic[src]
        else:
            srcDegrees = 0
            ver2degreeDic[src] = srcDegrees

        if ver2degreeDic.has_key(tar):
            tarDegrees = ver2degreeDic[tar]
        else:
            tarDegrees = 0
            ver2degreeDic[tar] = tarDegrees

        ver2degreeDic[src] = ver2degreeDic[src] + 1
        ver2degreeDic[tar] = ver2degreeDic[tar] + 1


    for i in range(numOfParts):
        vertexDic[i] = set()
    
    for line in f:
        
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])
        
        edgeNum = edgeNum + 1
        # if edgeNum % 1000000 == 0:
        #     print edgeNum
        
        if ver2degreeDic.has_key(src):
            srcDegrees = ver2degreeDic[src]
        else:
            srcDegrees = 0
            ver2degreeDic[src] = srcDegrees

        if ver2degreeDic.has_key(tar):
            tarDegrees = ver2degreeDic[tar]
        else:
            tarDegrees = 0
            ver2degreeDic[tar] = tarDegrees  

        # 分边策略
        # print src
        # print tar
        # print srcMachines
        # print tarMachines
        # flag = flag + 1
        # if flag > 30:
        #     exit()

        mixingPrime = 1125899906842597L                          # 用于进行随机化，单纯使用 hash 会导致分配到的 part 很集中
        if srcDegrees < tarDegrees :
            part = abs(hash(src * mixingPrime)) % numOfParts
        else:
            part = abs(hash(tar * mixingPrime)) % numOfParts
        
        # 更新各种集合数据
        Partitions[part].append((src, tar))
        
        # if vertexDic.has_key(part):
        #     vertexDic[part].add(src)
        #     vertexDic[part].add(tar)
        # else:
        #     vertexSet = set()  # 定义的是集合
        #     vertexSet.add(src)
        #     vertexSet.add(tar)
        #     vertexDic[part] = vertexSet

        vertexDic[part].add(src)
        vertexDic[part].add(tar)

        # ver2degreeDic[src] = ver2degreeDic[src] + 1
        # ver2degreeDic[tar] = ver2degreeDic[tar] + 1
        
    
    # 获取所有子图的顶点个数    
    allVertex = 0L
    maxVertices = 0L
    for i in range(numOfParts):
        allVertex = allVertex + len(vertexDic[i])
        if maxVertices < len(vertexDic[i]):
            maxVertices = len(vertexDic[i])
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
    AveSize = edgeNum/float(numOfParts)
    temp = 0L
    for i in range(numOfParts):
        temp = temp + (len(Partitions[i]) - AveSize) * (len(Partitions[i]) - AveSize)
        if maxEdges < len(Partitions[i]):
            maxEdges = len(Partitions[i])
        print len(Partitions[i])
    temp = temp/numOfParts
    temp = math.sqrt(temp)

    LSD = temp
    LRSD = LSD/AveSize

    # 依次是 VRF  LSD  LRSD  VLSD  VLRSD  子图点最大值  子图点平均值  子图边最大值  子图边平均值
    print VRF, LSD, LRSD, VLSD, VLRSD, maxVertices, allVertex/numOfParts, maxEdges, edgeNum/numOfParts


    # for i in range(numOfParts):
    #     for j in range(len(Partitions[i])):
    #         print Partitions[i][j]
    #     print '\n'


time_start = time.time()

parts = [4,10,30,50,100,150,200,256]

# parts = [3,4,8,11,16,29,32,59,64,99,119,128,201,249,256]
for i in range(len(parts)):
    print parts[i]
    DBH1AL("/home/w/data/web-BerkStan.txt", parts[i])

# DBH1AL("/home/w/data/web-BerkStan.txt", 64)

time_end = time.time()
time_used = time_end - time_start

print time_used

