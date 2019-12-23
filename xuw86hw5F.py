############################################################
# CMPSC 442: Homework 5
############################################################

student_name = "Xuezhou Wen"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import string
import itertools
import random
import math
############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    theText=" "+text+" "
    #theText.strip()
    #theText=text.strip(" ")
    t=[]
    tail=None
    for i in range(len(theText)):
        if theText[i]!=" ":
            if theText[i] in string.punctuation:
                if tail !=None:
                    t.append(theText[tail:i])
                    tail=None
                t.append(theText[i])
            elif theText[i] in string.ascii_letters or theText[i] in string.digits:
                if tail==None:
                    tail=i
                
        else:
            if tail !=None:
                t.append(theText[tail:i])
                tail=None
    return t

def ngrams(n, tokens):
    t=[]
    for i in range(n-1):
        t.append("<START>")
    t=t+tokens+["<END>"]

    t5=[]
    for i in range(len(t)):
        t4=[]
        if i+n-1<=len(t)-1:
            t2=[]
            for j in range(n-1):
                t2.append(t[i+j])
            t3=tuple(t2)
            t4.append(t3)
            t4.append(t[i+n-1])
            t4=tuple(t4)
        t5.append(t4)




    for i in reversed(range(len(t5))):
        if t5[i]==[]:
            t5.pop()

    return t5



class NgramModel(object):

    def __init__(self, n):
        self.n=n
        self.internal=[]

    def update(self, sentence):
        tokens=tokenize(sentence)
        #print(tokens)
        #print(ngrams(self.n,tokens))
        self.internal+=ngrams(self.n,tokens)
        

    def prob(self, context, token):
        totalContext=0
        for i in range(len(self.internal)):
            if self.internal[i][0]==context:
                #print(self.internal[i])
                totalContext+=1
        #print(self.internal,totalContext)
        if self.internal.count((context,token))==0 or totalContext==0:
        #print(self.internal.count((context,token)),totalContext,self.internal)
            return 0

        return self.internal.count((context,token))/totalContext

    def random_token(self, context):
        r=random.random()

        newDict={}
        probSum=0
        test1=[]
        for i in range(len(self.internal)):
            if self.internal[i][0]==context:
                newDict[self.internal[i][1]]=self.prob(context,self.internal[i][1])
                test1.append(self.internal[i][1])
        #print(sorted(newDict),"sorted newDict")
        #print(newDict.keys())
        #if len(newDict.keys())==1:
        #    for i in newDict:
        #        return i
        
        #for i in range(len(self.internal)):
            #if self.internal[i][0]==context:
                


        test1=sorted(test1)
        #print(test1)
        #print(newDict)
        #test=['a', 'b', 'c', 'd', '<END>']
        #test=[ 'a', 'a', 'a', 'b', 'b', 'b', 'c', 'd','<END>', '<END>']
        #print(r,"r")
        for i in test1:
            probSum+=(newDict[i]/test1.count(i))
            if probSum >=r:
                return i
        
        #return "<None>"


    def random_text(self, token_count):
        context_list=[]
        #for i in range(self.n -1):
        #    context_list.append("<START>")
        context_list=["<START>"]*(self.n -1)
        context_tuple=tuple(context_list)
        context_tuple_starting=tuple(context_list)
        text=[]
        #print(context_list,"context_list")
        for i in range(token_count):
            #print(i,"index")
            newToken=self.random_token(context_tuple)
            text.append(str(newToken))
            if newToken=="<END>":
                context_tuple=context_tuple_starting
            else:
                if context_list!=[]:

                    del context_list[0]
                    context_list.append(str(newToken))
                context_tuple=tuple(context_list)
        text_string=""
        #for i in range(len(text)):
        #    text_string+=text[i]+" "
        if text!=[]:
            text_string=" ".join(text)
        else:
            text_string=""
        text_string.strip()
        return text_string




    def perplexity(self, sentence):
        probability=0
        #self.update(sentence)
        token_list=ngrams(self.n,tokenize(sentence))
        for i in range(len(token_list)):
            
            if self.prob(token_list[i][0],token_list[i][1])!=0:

                probability+=math.log(self.prob(token_list[i][0],token_list[i][1]))
                #print(math.log(self.prob(token_list[i][1],token_list[i+1][1])))
        #print(token_list)
        product=probability
        #probability=probability/len(token_list)
        probability=(1/math.exp(product))**(1/len(token_list))
        return probability

def create_ngram_model(n, path):
    newObject=NgramModel(n)
    with open(path) as theFile:
        sentence=theFile.readline()
        newObject.update(sentence)
        while sentence:
            sentence=theFile.readline()
            newObject.update(sentence)
    return newObject

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
16 hours spent to complete this assignment.
"""

feedback_question_2 = """
the random token part is very challenging, i failed to pass the last test case.
"""

feedback_question_3 = """
i like the random_text part, nothing needs to be changed.
"""
