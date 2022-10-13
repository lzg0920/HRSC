import os
import sys

import dgl

import tqdm
from DrugDataset_Load02 import loaddata,dataSavePath

import numpy as np
#二截图10，二+关10
num_walks_per_node = 30
walk_length = 100


#存放各种节点数
superNodeNum = 1195
userNodeNum = 4
drugNodeNum = 132
actionNodeNum = 221
# 数据所在路径
# path = sys.argv[1]

LD = loaddata() #读数据
SU_Node_s, SU_Node_u, SD_Node_s, SD_Node_d, SA_Node_s, SA_Node_a, dictU, dictD, dictA, \
user_drug_ID_u, user_drug_ID_d, drug_action_ID_d, drug_action_ID_a, action_user_ID_a, action_user_ID_u, dictUD_u, dictUD_d, dictDA_d, dictDA_a, dictAU_a, dictAU_u = LD.load_2section_IncidenceGraphData()
def ConstructHeterogeneous_2section_IncidenceGraph():
    #通过字典构建关联图异质图

    hgIncidence = dgl.heterograph({
        ('super', 'su', 'user'): (SU_Node_s,SU_Node_u),
        ('user', 'us', 'super'): (SU_Node_u,SU_Node_s),
        ('super', 'sd', 'drug'): (SD_Node_s,SD_Node_d),
        ('drug', 'ds', 'super'): (SD_Node_d,SD_Node_s),
        ('super', 'sa', 'action'): (SA_Node_s,SA_Node_a),
        ('action', 'as', 'super'): (SA_Node_a,SA_Node_s),

        ('user', 'ud', 'drug'): (user_drug_ID_u, user_drug_ID_d),
        ('drug', 'du', 'user'): (user_drug_ID_d, user_drug_ID_u),
        ('drug', 'da', 'action'): (drug_action_ID_d, drug_action_ID_a),
        ('action', 'ad', 'drug'): (drug_action_ID_a, drug_action_ID_d),
        ('action', 'au', 'user'): (action_user_ID_a, action_user_ID_u),
        ('user', 'ua', 'action'): (action_user_ID_u, action_user_ID_a)
    })
    print(hgIncidence.num_nodes(),hgIncidence.num_nodes('super'),hgIncidence.num_nodes('user'),hgIncidence.num_nodes('drug'),hgIncidence.num_nodes('action'),hgIncidence.num_edges())
    print(dictU)
    print(dictD)
    print(dictA)
    return hgIncidence,dictU,dictD,dictA,dictUD_u,dictUD_d,dictDA_d,dictDA_a,dictAU_a,dictAU_u

# def ConstructHeterogeneous2sectionGraph():
#     #构建二截图异质图
#     UD_Node_u,user_drug_ID_d,  drug_action_ID_d,drug_action_ID_a,  action_user_ID_a,AU_Node_u, dictUD_d,dictDA_d,dictDA_a,dictAU_a = LD.load2sectionGraphData()
#     hg2section = dgl.heterograph({
#         ('user', 'ud', 'drug'): (UD_Node_u,user_drug_ID_d),
#         ('drug', 'du', 'user'): (user_drug_ID_d,UD_Node_u),
#         ('drug', 'da', 'action'): (drug_action_ID_d,drug_action_ID_a),
#         ('action', 'ad', 'drug'): (drug_action_ID_a,drug_action_ID_d),
#         ('action', 'au', 'user'): (action_user_ID_a,AU_Node_u),
#         ('user', 'ua', 'action'): (AU_Node_u,action_user_ID_a)})
#     print(hg2section.num_nodes(), hg2section.num_nodes('user'),hg2section.num_nodes('drug'), hg2section.num_nodes('action'), hg2section.num_edges())
#     print(dictDA_a[26])
#     print(dictAU_a[25])
#     return hg2section,dictUD_d,dictDA_d,dictDA_a,dictAU_a


path = dataSavePath()

#产生2截图关联图游走语料库
def generate_metapath_2section_Incidence(hg,dictU,dictD,dictA,  dictUD_u,dictUD_d,dictDA_d,dictDA_a,dictAU_a,dictAU_u,walk_length,num_walks_per_node):
    output_path = open(os.path.join(path, "output_2section_metapath.txt"), "w",encoding='utf-8')
    # 类型是list，index是id
    # 产生generate_metapath：user1 - super_edge1 - drug1 -  super_edge2 - action1 - super_edge4 - drug2 - super_edge3 - user2 'ud','ds','sa','as','sd','du'
    for user_idx in tqdm.trange(hg.number_of_nodes('user')):
        #traces是列表的列表，每个列表是一个sequence 'us','sd','ds','sa','as','sd','ds','su'  2+guan 'us','sd','da','as','sa','ad','ds','su'
        traces, _ = dgl.sampling.random_walk(
            hg, [user_idx] * num_walks_per_node, metapath=['us','sd','da','ad','ds','su'] * walk_length)
        for tr in traces:
            trList = tr.tolist()
            for i in range(len(trList)):#删除所有路径中的-1
                if trList[i] == -1:
                    del trList[i:]
                    break
            for i in range(0,len(trList)):
                if trList[i] != -1:
                    # if i % 8 == 0:
                    #     trList[i] = trList[i] + superNodeNum
                    # elif i % 8 == 2 or i % 8 == 6  :
                    #     trList[i] = trList[i] + superNodeNum + userNodeNum
                    # elif i % 8 == 3 or i % 8 == 5:
                    #     trList[i] = trList[i]+ superNodeNum + userNodeNum +drugNodeNum
                    if i % 6 == 0 :
                        trList[i] = trList[i] + superNodeNum
                    elif i % 6 == 2 or i % 6 == 4 :
                        trList[i] = trList[i] + superNodeNum + userNodeNum
                    elif i % 6 == 3:
                        trList[i] = trList[i]+ superNodeNum + userNodeNum +drugNodeNum
            outline =' '.join(str(trList[i]) for i in range(len(trList)))
            print(outline, file=output_path)
    output_path.close
# #获取关联图+2截图元路径游走语料库
# hg2section,dictU,dictD,dictA,   dictUD_u,dictUD_d,dictDA_d,dictDA_a,dictAU_a,dictAU_u = ConstructHeterogeneous_2section_IncidenceGraph()
# generate_metapath_2section_Incidence(hg2section,dictUD_d,dictDA_d,dictDA_a, dictUD_u,dictUD_d,dictDA_d,dictDA_a,dictAU_a,dictAU_u,walk_length,num_walks_per_node)

