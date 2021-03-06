#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time

def GreedyAL(edgelist, numOfParts):
    f = open(edgelist, "r")
    # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    vertexDic = {}
    # { vertex:set(part1, part2,...),... }          存储每个点对应的分区
    ver2partDic = {}
    # { vertex:degree,... }                         存储每个点对应的度信息
    ver2degreeDic = {}
    # { part1:score, part2:score,... }              存储每一条边相对每个子图的分数
    partSocre2edge = {}
    # 存储总边数
    edgeNum = 0

    # 文中所给的 lamda 参数
    x = 1.0
    
    # 调试变量
    flag = 0

    for i in range(numOfParts):
        vertexDic[i] = set()
    
    for line in f:
        srcTar = line.strip().split()
        src = long(srcTar[0])
        tar = long(srcTar[1])
        
        edgeNum = edgeNum + 1
        if edgeNum % 1000000 == 0:
            print edgeNum

        maxsize = 0
        minsize = 100000000
        for i in range(numOfParts):
            if maxsize < len(Partitions[i]):
                maxsize = len(Partitions[i])
            if minsize > len(Partitions[i]):
                minsize = len(Partitions[i])
        
        if ver2partDic.has_key(src):
            srcMachines = ver2partDic[src]
        else:
            src2partSet = set()
            ver2partDic[src] = src2partSet
            srcMachines = ver2partDic[src]

        if ver2partDic.has_key(tar):
            tarMachines = ver2partDic[tar]
        else:
            tar2partSet = set()
            ver2partDic[tar] = tar2partSet
            tarMachines = ver2partDic[tar]   

        # 分边策略
        # print src
        # print tar
        # print srcMachines
        # print tarMachines
        # flag = flag + 1
        # if flag > 30:
        #     exit()

        # 对每一个 part 计算 score
        for partTemp in range(numOfParts):

            if ver2degreeDic.has_key(src):
                partialDegSrc = ver2degreeDic[src]
            else:
                partialDegSrc = 0
                ver2degreeDic[src] = partialDegSrc

            if ver2degreeDic.has_key(tar):
                partialDegTar = ver2degreeDic[tar]
            else:
                partialDegTar = 0
                ver2degreeDic[tar] = partialDegTar

            if partialDegSrc == 0 and partialDegTar == 0:
                rDegSrc = 0
                rDegTar = 0
            else:
                rDegSrc = partialDegSrc / (float)(partialDegSrc + partialDegTar)
                rDegTar = partialDegTar / (float)(partialDegSrc + partialDegTar)

            if partTemp in srcMachines:
                gsrc = 1
            else:
                gsrc = 0
            if partTemp in tarMachines:
                gtar = 1
            else:
                gtar = 0

            rep = gsrc + gtar

            bal = x * (maxsize - len(Partitions[partTemp])) / (float)(maxsize - minsize + 1)   # 加 1 避免除 0

            score = rep + bal

            partSocre2edge[partTemp] = score

        part = 0
        for j in range(numOfParts):
            if partSocre2edge[part] < partSocre2edge[j]:
                part = j

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

        ver2partDic[src].add(part)
        ver2partDic[tar].add(part)

        ver2degreeDic[src] = ver2degreeDic[src] + 1
        ver2degreeDic[tar] = ver2degreeDic[tar] + 1
        
    
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


# time_start = time.time()

GreedyAL("/home/w/data/testdata/ba-1.txt", 100)

# time_end = time.time()
# time_used = time_end - time_start

# print time_used

