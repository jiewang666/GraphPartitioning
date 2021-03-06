#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time

def PDSAL(edgelist, numOfParts, rs, cs):
    f = open(edgelist, "r")
    # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    vertexDic = {}
    # 存储总边数
    edgeNum = 0

    # PDS 对应点约束集合
    # numOfParts = 32
    row = rs  # 行 
    col = cs  # 列
    # { part:set(part1, part2,...),... }            初始化PDS集合特性
    partSet = {}
    # 将列元素全部加入集合
    for i in range(0, numOfParts):
        tempSet = set()
        irow = int(i / col)
        icol = i - irow * col
        for j in range(0, numOfParts):
            jrow = int(j / col)
            jcol = j - jrow * col
            if icol == jcol:
                tempSet.add(j)
        partSet[i] = tempSet
        del tempSet
    # 将行元素有选择性加入集合
    for r in range(0, row):
        for c in range(0, col):
            i = r * col + c
            if col % 2 == 0:
                cols = col / 2 + 1
            else:
                cols = (col + 1)/2
            for m in range(0, cols):
                j = (c + m) % col
                partSet[i].add(r * col + j)

    # for i in range(0, numOfParts):
    #     print partSet[i] 

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

        # 分边策略
        # print src
        # print tar
        # flag = flag + 1
        # if flag > 30:
        #     exit()
      
        mixingPrime = 1125899906842597L                          # 用于进行随机化，单纯使用 hash 会导致分配到的 part 很集中
        partsrc = abs(hash(src * mixingPrime)) % numOfParts
        parttar = abs(hash(tar * mixingPrime)) % numOfParts
        partset = partSet[partsrc] & partSet[parttar]
        partlist = list(partset)
        # print partlist
        part = random.choice(partlist)

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

parts = [3,4,8,18,32,50,72,100,128,162,200,242,256]
rs = [1,2,2,3,4,5,6,10,8,9,10,11,16]
cs = [3,2,4,6,8,10,12,10,16,18,20,22,16]
for i in range(len(parts)):
    print parts[i]
    PDSAL("/home/w/data/web-BerkStan.txt", parts[i], rs[i], cs[i])

# PDSAL("/home/w/data/testdata/bfs1.txt", 18, 3, 6)

time_end = time.time()
time_used = time_end - time_start

print time_used

