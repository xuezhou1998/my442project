############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Xuezhou Wen"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import collections
import itertools
from itertools import permutations
import math

############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    #newObject=NgramModel(n)
    newObject=[]

    with open(path) as theFile:
        sentence=theFile.readline()
        corpusList=sentence.split()
        dequeObject=collections.deque(corpusList)
        newObject2=[]
        while len(dequeObject)!=0:
            
            newObject2.append(tuple(dequeObject.popleft().split("=")))
        #newObject.update(sentence)
        newObject.append(newObject2)
        while sentence:
            sentence=theFile.readline()
            corpusList=sentence.split()
            dequeObject=collections.deque(corpusList)
            newObject2=[]
            while len(dequeObject)!=0:
                
                newObject2.append(tuple(dequeObject.popleft().split("=")))
            #newObject.update(sentence)
            newObject.append(newObject2)
    return newObject

class Tagger(object):

    def __init__(self, sentences):
        lapLaceConstant=3.14e-10
        self.sentences=sentences
        self.dictTag={"NOUN":0,"VERB":0,"ADJ":0,"ADV":0,"PRON":0,"DET":0,"ADP":0,"NUM":0,"CONJ":0,"PRT":0,".":0,"X":0}
        self.sentDeque=collections.deque(sentences)
        for i in range(len(self.sentDeque)):
            #print(self.sentDeque.popleft()[0])
            a=self.sentDeque[i]
            if a!=[]:

                self.dictTag[a[0][1]]+=1
        #for i in range(len(self.sentences)):
        #    if self.sentences[i]!=[]:
        #        print(self.sentences[i][0][1])
        total=sum(self.dictTag.values())
        self.init_probs={"NOUN":0,"VERB":0,"ADJ":0,"ADV":0,"PRON":0,"DET":0,"ADP":0,"NUM":0,"CONJ":0,"PRT":0,".":0,"X":0}
        for i in self.init_probs:
            self.init_probs[i]=math.log((self.dictTag[i]+lapLaceConstant)/(total+len(self.init_probs.keys())*lapLaceConstant))
        #self.dictTagIndexPair={"NOUN":A,"VERB":B,"ADJ":C,"ADV":D,"PRON":E,"DET":F,"ADP":G,"NUM":H,"CONJ":I,"PRT":J,".":K,"X":L}
        self.dictTagComb={}
        self.dictList=[{},{},{},{},{},{},{},{},{},{},{},{}]
        self.tagList=["NOUN","VERB","ADJ","ADV","PRON","DET","ADP","NUM","CONJ","PRT",".","X"]
        tagPermutation=list(itertools.product(self.tagList,repeat=2))
        self.oneDemensinoSentence=list(itertools.chain.from_iterable(self.sentences))
        #for i in range(len(self.oneDemensinoSentence)):
        a=self.oneDemensinoSentence
        totalCond={"NOUN":0,"VERB":0,"ADJ":0,"ADV":0,"PRON":0,"DET":0,"ADP":0,"NUM":0,"CONJ":0,"PRT":0,".":0,"X":0}
        if a!=[]:

            for j in range(len(a)-1):
                x=a[j][1]
                u=a[j][0]
                y=a[j+1][1]
                z=tuple([x,y])
                totalCond[x]+=1
                if z in self.dictTagComb.keys():
                    self.dictTagComb[z]+=1
                else:
                    self.dictTagComb[z]=1
                tagindex=self.tagList.index(x)
                targetDict=self.dictList[tagindex]
                if u in targetDict.keys():
                    targetDict[u]+=1
                else:
                    targetDict[u]=1
            x=a[len(a)-1][1]
            u=a[len(a)-1][0]
            tagindex=self.tagList.index(x)
            targetDict=self.dictList[tagindex]
            if u in targetDict.keys():
                targetDict[u]+=1
            else:
                targetDict[u]=1
        total=sum(self.dictTagComb.values())
        self.trans_probs={}
        for i in tagPermutation:
            if i in self.dictTagComb:
                self.trans_probs[i]=math.log((self.dictTagComb[i]+lapLaceConstant)/(totalCond[i[0]]+len(self.tagList)*lapLaceConstant))
            else:
                self.trans_probs[i]=math.log((lapLaceConstant)/(totalCond[i[0]]+len(self.tagList)*lapLaceConstant))

        #print("total2",sum(self.trans_probs.values()))
        #print("det noun",self.trans_probs["DET->NOUN"],
        #self.trans_probs["NOUN->NOUN"],self.trans_probs["NOUN->ADJ"],
        #self.trans_probs["X->."])        
        #print("the dict",self.trans_probs)
        #print("dictlist",self.dictList[0])
        dictlistTotal=[]
        for i in range(len(self.dictList)):
            dictlistTotal.append(sum(self.dictList[i].values()))
        for i in range(len(dictlistTotal)):
            a=self.dictList[i]
            for j in a:
                a[j]=math.log((a[j]+lapLaceConstant)/(dictlistTotal[i]+len(a.keys())*lapLaceConstant))
        self.dictSum=dictlistTotal

        #print(dictlistTotal)
        #print(sum(self.init_probs.values()),"sum")
        self.lapLaceConstant=lapLaceConstant





    def most_probable_tags(self, tokens):
        b=[]
        for j in tokens:
            a=0
            c=None
            for i in range(len(self.dictList)):
                if j in self.dictList[i].keys():
                    if c!=None:

                        if self.dictList[i][j]>c:
                            a=i
                            c=self.dictList[i][j]
                    else:
                        a=i
                        c=self.dictList[i][j]
            if c!=None:
                b.append(self.tagList[a])
            else:
                b.append(self.tagList[len(self.tagList)-1])
        return b

    def viterbi_tags(self, tokens):
        initProbs=self.init_probs
        transProb=self.trans_probs
        emissionProbs=self.dictList
        lc=self.lapLaceConstant
        tagSet=self.tagList
        trellis=[[None]*len(tokens) for i in range(len(tagSet))]
        #for i in trellis:
        #    i=[ 0 for i in range(len(tokens))]
        backpointers=[[None]*len(tokens)  for i in range(len(tagSet))]
        #for i in backpointers:
           # i=[ [None]*len(tokens)  for i in range(len(tokens))]
        #print(trellis)
        for i in range(len(tagSet)):
            if tokens[0] in emissionProbs[i].keys():

                e=emissionProbs[i][tokens[0]]
            else:
                e=math.log(lc/(len(emissionProbs[i].keys())*lc+self.dictSum[i]))

            trellis[i][0]=(initProbs[tagSet[i]]+e)
            backpointers[i][0]=(0)
        for j in range(1,len(tokens)):
            for i in range(len(tagSet)):
                a=[]
                b=[]
                for k in range(len(tagSet)):

                    

                    a.append(trellis[k][j-1]+transProb[tuple([tagSet[k],tagSet[i]])])
                    b.append(trellis[k][j-1]+transProb[tuple([tagSet[k],tagSet[i]])])####potential place of issue, trellis computed may affect 
                if tokens[j] in emissionProbs[i].keys():

                    e=emissionProbs[i][tokens[j]]
                else:
                    e=math.log(lc/(len(emissionProbs[i].keys())*lc+self.dictSum[i]))
                    ### the computation of backpointers!!!!!!
                resultMaxTrellis=max(a)+e
                #resultMaxTrellisIndex=a.index(resultMaxTrellis)
                resultMaxBackpointerIndex=b.index(max(b))


                trellis[i][j]=resultMaxTrellis
                backpointers[i][j]=resultMaxBackpointerIndex
        returnListZ=collections.deque()
        returnListX=collections.deque()
        returnListZ=[None for i in range(len(tokens))]
        returnListX=[None for i in range(len(tokens))]
        a=[]
        for i in range(len(tagSet)):
            a.append(trellis[i][len(tokens)-1])
        returnListZ[len(tokens)-1]=a.index(max(a))
        returnListX[len(tokens)-1]=tagSet[returnListZ[len(tokens)-1]]
        #print(a,returnListX,returnListZ)
        #print(backpointers)
        for i in reversed(range(1,len(tokens))):
            returnListZ[i-1]=backpointers[returnListZ[i]][i]
            returnListX[i-1]=tagSet[returnListZ[i-1]]
        #print(trellis)
        return list(returnListX)





############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
16 hours
"""

feedback_question_2 = """
the most challeging aspect of this assignment is to calculate the most probable tag,
i stumbled there
"""

feedback_question_3 = """
i like the writing init part, i hope next time you can give us a uniform way representing data in init
"""
