#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math
import time

def Greedy(edgelist, numOfParts):
    a1 = 0
    a2 = 0
    a3 = 0
    a4 = 0
    a5 = 0
    f = open(edgelist, "r")
    # [[(src, dst), (src, dst),...],[()],[()]....]  每个分区对应的边集合
    Partitions = [[] for i in range(numOfParts)]
    # { part:set(v1,v2,...), ... }                  存储每个分区对应的点
    vertexDic = {}
    # { vertex:set(part1, part2,...),... }          存储每个点对应的分区
    ver2partDic = {}
    # 存储总边数
    edgeNum = 0
    
    # 调试变量
    flag = 0

    for i in range(numOfParts):
        vertexDic[i] = set()
    
    for line in f:
        srcTar = line.strip().split()
        if (srcTar[0] == '#'):
            continue
        src = long(srcTar[0])
        tar = long(srcTar[1])
        edgeNum = edgeNum + 1
        # if edgeNum % 1 == 0:
        #     print edgeNum
        
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


        if (len(srcMachines) == 0) and (len(tarMachines) == 0):      # A(u) 和 A(v) 都是空集  选择边数量最少的子图加入
            a1 = a1 + 1
            part = -1
            for i in range(numOfParts):
                if part == -1:
                    part = i
                    continue 
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        elif (len(srcMachines) > 0) and (len(tarMachines) == 0):
            a2 = a2 + 1
            part = -1
            for i in srcMachines:
                if part == -1:
                    part = i
                    continue
                if len(Partitions[i]) < len(Partitions[part]):
                    part = i

        elif (len(srcMachines) == 0) and (len(tarMachines) > 0):
            a3 = a3 + 1
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
                a4 = a4 + 1
                part = -1
                for i in Intersection:
                    if part == -1:
                        part = i
                        continue
                    if len(Partitions[i]) < len(Partitions[part]):
                        part = i
            elif (len(Intersection) == 0):
                a5 = a5 + 1
                part = -1
                for i in Convergence:
                    if part == -1:
                        part = i
                        continue
                    if len(Partitions[i]) < len(Partitions[part]):
                        part = i

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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 16102276ccd553a0bd326a871a4aed920b9e3666
    print VRF, LSD, LRSD, VLSD, VLRSD, maxVertices, allVertex/numOfParts, maxEdges, edgeNum/numOfParts

    print a1, a2, a3, a4, a5

<<<<<<< HEAD
=======
=======
    # print VRF, LSD, LRSD, VLSD, VLRSD, maxVertices, allVertex/numOfParts, maxEdges, edgeNum/numOfParts
    print "VRF " + str(VRF)
    print "max-edges " + str(maxEdges)
    print "min-edges " + str(minEdges)
    print "avg-edges " + str(edgeNum/numOfParts)
    print "max-vertices " + str(maxVertices)
    print "min-vertices " + str(minVertices)
    print "avg-vertices " + str(allVertex/numOfParts)
    print "LRSD " + str(LRSD)
    print "VLRSD " + str(VLRSD)
>>>>>>> e0016cf33cb3ed6721e1eb9a52867e9b3a2fc558
>>>>>>> 16102276ccd553a0bd326a871a4aed920b9e3666

    # for i in range(numOfParts):
    #     for j in range(len(Partitions[i])):
    #         print Partitions[i][j]
    #     print '\n'


time_start = time.time()

# parts = [4,10,30,50,100,150,200,256]

# parts = [4,8,10,16,30,32,60,64,120,128,250,256,500,512]
# for i in range(len(parts)):
#     print parts[i]
<<<<<<< HEAD
#     Greedy("/home/wj/swr/data/soc-LiveRandomCPP.txt", parts[i])soc-LiveJournal1.txt

Greedy("/home/wj/swr/data/soc-LiveJournal1.txt", 100)
=======
<<<<<<< HEAD
#     Greedy("/home/wj/swr/data/soc-LiveRandomCPP.txt", parts[i])soc-LiveJournal1.txt

Greedy("/home/wj/swr/data/soc-LiveJournal1.txt", 100)
=======
#     Greedy("/home/w/data/Wiki-VoteRandom.txt", parts[i])

Greedy("/home/w/data/Wiki-VoteRandom.txt", 100)
>>>>>>> e0016cf33cb3ed6721e1eb9a52867e9b3a2fc558
>>>>>>> 16102276ccd553a0bd326a871a4aed920b9e3666

time_end = time.time()
time_used = time_end - time_start
print time_used

