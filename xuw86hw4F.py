############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Xuezhou Wen"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import os
import math
import collections
from collections import OrderedDict
############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    msgList=[]
    emailFile=open(email_path,"r")
    #msgList=emailFile.read().split()
    msg=email.message_from_file(emailFile)
    msgIterator=email.iterators.body_line_iterator(msg)

    for x in msgIterator:
        msgList+=x.split()


    return msgList


def log_probs(email_paths, smoothing):
    dictWord={}
    theSameWord=set()
    totalCount=0
    vocabularyCount=0
    dictResult={}
    for x in email_paths:

        allTokensOneEmail=load_tokens(x)
        for i in range(len(allTokensOneEmail)):
            if tuple(allTokensOneEmail[i]) not in theSameWord:
                dictWord[allTokensOneEmail[i]]=1
                vocabularyCount+=1
                theSameWord.add(tuple(allTokensOneEmail[i]))
            else:
                dictWord[allTokensOneEmail[i]]+=1

    for x in dictWord:
        totalCount+=dictWord[x]
    dictResult["<UNK>"]=math.log(smoothing/(totalCount+smoothing*(vocabularyCount+1)))

    for x in dictWord:
        dictResult[x]=math.log((dictWord[x]+smoothing)/(totalCount+smoothing*(vocabularyCount+1)))
    return dictResult




class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spamPaths=[]
        hamPaths=[]
        self.spam_dir=spam_dir
        self.ham_dir=ham_dir
        self.smoothing=smoothing
        for f in os.listdir(spam_dir):
            fname = os.fsdecode(f)
            spamPaths.append(spam_dir+"/"+fname)
        for f in os.listdir(ham_dir):
            fname = os.fsdecode(f)
            hamPaths.append(ham_dir+"/"+fname)
        self.probHam=math.log(len(hamPaths)/(len(spamPaths)+len(hamPaths)))
        self.probSpam=math.log(len(spamPaths)/(len(spamPaths)+len(hamPaths)))
        self.unloggedHam={}
        self.unloggedSpam={}
        self.hamDict=log_probs(hamPaths,smoothing)
        self.spamDict=log_probs(spamPaths,smoothing)
        #theSameWord=set()
        #resultDict=OrderedDict{}
        for x in self.hamDict:
            self.unloggedHam[x]=math.exp(self.hamDict[x])
        for x in self.spamDict:
            self.unloggedSpam[x]=math.exp(self.spamDict[x])
        listSpam=" ".join(self.unloggedSpam.keys()).split()
        listHam=" ".join(self.unloggedHam.keys()).split()
        self.unionSet=set()
        self.unionSet=set().union(listHam,listSpam)


        
    def theCountOneEmail(self,dirctory):
        dictWord={}
        theSameWord=set()
        #totalCount=0
        vocabularyCount=0
        #dictResult={}
        allTokensOneEmail=load_tokens(dirctory)
        for i in range(len(allTokensOneEmail)):
            if tuple(allTokensOneEmail[i]) not in theSameWord:
                dictWord[allTokensOneEmail[i]]=1
                vocabularyCount+=1
                theSameWord.add(tuple(allTokensOneEmail[i]))
            else:
                dictWord[allTokensOneEmail[i]]+=1
        return dictWord
        
    def is_spam(self, email_path):
        currentDictWord=self.theCountOneEmail(email_path)
        probSpamDecide=self.probSpam
        probHamDecide=self.probHam
        newDict={}
        spamUnknown=0
        hamUnknown=0
        for x in currentDictWord:
            if x in self.hamDict:
                probHamDecide+=self.hamDict[x]*currentDictWord[x]
            else:
                #hamUnknown+=1
                probHamDecide+=self.hamDict["<UNK>"]*currentDictWord[x]

            if x in self.spamDict:
                probSpamDecide+=self.spamDict[x]*currentDictWord[x]
                #spamUnknown+=1
            else:
                probSpamDecide+=self.spamDict["<UNK>"]*currentDictWord[x]
        #print("probSpamDecide",probSpamDecide,"probHamDecide",probHamDecide,"probSpam",self.probSpam,"probHam",self.probHam)
        if probSpamDecide>=probHamDecide:
            return True
        else:
            return False

    def most_indicative_spam(self, n):
        resultDict={}
        for x in self.unionSet:
            if x in self.hamDict and x in self.spamDict:
                resultDict[x]=math.log(self.unloggedSpam[x]/(self.unloggedHam[x]+self.unloggedSpam[x]))
            #elif x in self.hamDict:
            #    resultDict[x]=math.log(self.unloggedSpam["<UNK>"]/(self.unloggedHam[x]+self.unloggedSpam["<UNK>"]))
            #elif x in self.spamDict:
            #    resultDict[x]=math.log(self.unloggedSpam[x]/(self.unloggedHam["<UNK>"]+self.unloggedSpam[x])) 


        resultDict_final=OrderedDict(sorted(resultDict.items(), key=lambda x: x[1],reverse=True))
        resultList=[]
        counter=0
        for x in resultDict_final:
            if counter==n:
                return resultList
            else:
                resultList.append(x)
                counter+=1



    def most_indicative_ham(self, n):
        resultDict={}
        for x in self.unionSet:
            if x in self.hamDict and x in self.spamDict:
                resultDict[x]=math.log(self.unloggedHam[x]/(self.unloggedHam[x]+self.unloggedSpam[x]))
            #elif x in self.hamDict:
            #    resultDict[x]=math.log(self.unloggedSpam["<UNK>"]/(self.unloggedHam[x]+self.unloggedSpam["<UNK>"]))
            #elif x in self.spamDict:
            #    resultDict[x]=math.log(self.unloggedSpam[x]/(self.unloggedHam["<UNK>"]+self.unloggedSpam[x])) 


        resultDict_final=OrderedDict(sorted(resultDict.items(), key=lambda x: x[1],reverse=True))
        resultList=[]
        counter=0
        for x in resultDict_final:
            if counter==n:
                return resultList
            else:
                resultList.append(x)
                counter+=1

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
15 hours
"""

feedback_question_2 = """
the filter the spam email is very challenging
"""

feedback_question_3 = """
i like using statistic to find out the email that are most likely to be a spam

"""
count = 0
sf = SpamFilter("homework4_data/train/spam",
"homework4_data/train/ham", 1e-5)


x = [sf.is_spam("homework4_data/dev/ham/%s" %i) for i in os.listdir("homework4_data/dev/ham")]

for i in x:
    if i:
        count+=1
print(count)