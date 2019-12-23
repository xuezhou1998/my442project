############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Xuezhou Wen"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
strongly typed means that Python is very likely to generate error if the argument passed into a certain 
function does not closely match the expected type. 
example:
>>>a=5
>>>b='xxxx'
>>>c=a+b
TypeError: unsupported operand type(s) for +: 'int' and 'str'

dynamically typed means the programmer does not need to specify the type of each variable when writing the 
program. The type is associated with a run-time value.
>>>a=500
>>>type(a)
<type 'int'>

Python is both Dynamically typed and strong typed means Python will assign type for each variable automatically,
while it does not accept argument whose type is not expected by the function.
"""

python_concepts_question_2 = """
The error is:
Traceback (most recent call last):
  File "<pyshell#3>", line 1, in <module>
    points_to_names = {[0, 0]: "home", [1, 2]: "school", [-1, 1]: "market"}


The reason for the problem is that a list cannot be a key in a dictionary. 
a list cannot be hashed

"""

python_concepts_question_3 = """
the function concatenate2 is better, since it the running-time of
concatenate1 is O(N^2), and the running-time of concatenate2 is O(NlogN).

When concatenate1 is running, the function visits "result" every time 
it joins a single string, while the length of "result" simultaneouly increase
in linear speed.
the concatenate2 is better since it use a recursive structure and 
the Divide and Conquer strategy.   
"""
####print(python_concepts_question_3)

############################################################
# Section 2: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)==True]
    #####require testing

def concatenate(seqs):
    return [a for b in seqs for a in b] 

def transpose(matrix):
    return [[r[x] for r in matrix] for x in range(len(matrix[0]))]

############################################################
# Section 3: Sequence Slicing
############################################################

def copy(seq):
    return seq[slice(0,len(seq),1)]

def all_but_last(seq):
    return seq[slice(0,len(seq)-1,1)]

def every_other(seq):
    return seq[slice(0,len(seq),2)]

############################################################
# Section 4: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(len(seq)+1):
        yield seq[slice(0,i,1)]

def suffixes(seq):
    for i in range(len(seq)+1):
        yield seq[slice(i,len(seq),1)]
    
def slices(seq):
    for i in range(len(seq)):
        for j in range(len(seq)-i):
            yield seq[slice(i,j+i+1,1)]

############################################################
# Section 5: Text Processing
############################################################

def normalize(text):
    ntext=str(text.strip().lower())
    ##print (ntext)
    ntext=ntext.split(' ')
    ##print (ntext)
    finaltext=""
    for i in range(len(ntext)):
        if ntext[i]!="":
            
            if i==0:
                finaltext+=ntext[i]
            else:
                finaltext+=" "+ntext[i]

            
    return finaltext

def no_vowels(text):
    return text.replace('a','').replace('e','').replace('i','').replace('o','').replace('u','').replace('A','').replace('E','').replace('I','').replace('O','').replace('U','')

def digits_to_words(text):
    
    digitdict={'1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','0':'zero'}
    for i in range(len(text)):
        if not text[i].isdigit():
            text=text.replace(text[i],' ',1)
    text=text.replace(' ','')
    if text=='':
        return text
    text=list(text)
    newtext=''
    for i in range(len(text)):
        newtext+=digitdict[text[i]]
        if i!=len(text)-1:
            newtext+=' '
    return newtext
            
    

def to_mixed_case(name):
    udscr=0
    fstword=1
    name1=name.split('_')
    name1=' '.join(name1).split()
    if len(name1)==0:
        return ''
    
    name1[0]=name1[0].lower()
    ##print(name1)
    for i in range(len(name1)-1):
        name1[i+1]=name1[i+1].capitalize()
    return ''.join(name1)
        
    #for i in range(len(name)):
        #if name[i].isalpha

############################################################
# Section 6: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial=polynomial
        

    def get_polynomial(self):
        return tuple(self.polynomial)

    def __neg__(self):
        self1=Polynomial(self.get_polynomial())
        poly=list(self1.get_polynomial())
        for i in range(len(poly)):
            
            a=list(poly[i])
            a[0]=a[0]*(-1)
            poly[i]=tuple(a)

        self1.polynomial=tuple(poly)
        return self1
            
        
        

    def __add__(self, other):
        self1=Polynomial(self.get_polynomial())
        poly=list(self1.get_polynomial())
        
        othpoly=list(other.get_polynomial())
        for i in range(len(othpoly)):
            poly.append(othpoly[i])

        self1.polynomial=tuple(poly)
        return self1

    def __sub__(self, other):
        self1=Polynomial(self.get_polynomial())
        
        poly=list(self1.get_polynomial())
        
        poly2=list(other.get_polynomial())
        for i in range(len(poly2)):
            
            a=list(poly2[i])
            a[0]=a[0]*(-1)
            poly2[i]=tuple(a)
        for i in range(len(poly2)):
            poly.append(poly2[i])

        self1.polynomial=tuple(poly)
        return self1

    def __mul__(self, other):
        self1=Polynomial(self.get_polynomial())
        poly=list(self1.get_polynomial())
        
        othpoly=list(other.get_polynomial())
        newpoly=[]
        for i in range(len(poly)):
            a=list(poly[i])
            for j in range(len(othpoly)):

                b=list(othpoly[j])
                c=[]
                c.append(b[0]*a[0])
                c.append(b[1]+a[1])
                newpoly.append(tuple(c))

        self1.polynomial=tuple(newpoly)
        return self1

    def __call__(self, x):
        poly=list(self.get_polynomial())
        summ=0
        for i in range(len(poly)):
            summ+=poly[i][0]*(x**poly[i][1])
        return summ
    def simplify(self):
        poly=list(self.get_polynomial())
        sortedpoly=sorted(poly, key=lambda elem:elem[1])

        newlist=[]
        for i in range(len(sortedpoly)):
            if i==0:
                newlist.append(sortedpoly[i])
            elif sortedpoly[i][1]==sortedpoly[i-1][1]:
                newlist[-1]=tuple([newlist[-1][0]+sortedpoly[i][0],sortedpoly[i][1]])
            else:
                newlist.append(sortedpoly[i])
        finallist=[]
        for i in range(len(newlist)):
            if newlist[i][0]!=0:
                finallist.append(newlist[i])
        finallist=sorted(finallist,key=lambda elem:elem[1],reverse=True)
        if finallist==[]:
            finallist=[(0,0)]
        self.polynomial=tuple(finallist)
            
    def __str__(self):
        poly=list(self.get_polynomial())
        newlist=""
        for i in range(len(poly)):
            if i==0:
                if abs(poly[i][0])!=1:
                    if poly[i][1]!=0 and poly[i][1]!=1:
                        newlist=newlist+str(poly[i][0])+"x"+"^"+str(poly[i][1])
                    elif poly[i][1]==1:
                        newlist=newlist+str(poly[i][0])+"x"
                    else:
                        newlist=newlist+str(poly[i][0])
                else:
                    if poly[i][0]<0:
                        if poly[i][1]!=0 and poly[i][1]!=1:
                            newlist=newlist+"-"+"x"+"^"+str(poly[i][1])
                        elif poly[i][1]==1:
                            newlist=newlist+"-"+"x"

                        else:
                            newlist=newlist+"-1"
                    else:
                        if poly[i][1]!=0 and poly[i][1]!=1:
                            newlist=newlist+"x"+"^"+str(poly[i][1])
                        elif poly[i][1]==1:
                            newlist=newlist+"x"
                        else:
                            newlist=newlist+'1'

            else:
                if abs(poly[i][0])!=1:
                    if poly[i][1]!=0 and poly[i][1]!=1:
                        if poly[i][0]<0:
                            
                            newlist=newlist+" - "+str(abs(poly[i][0]))+"x"+"^"+str(poly[i][1])
                        else:
                            newlist=newlist+" + "+str(poly[i][0])+"x"+"^"+str(poly[i][1])
                    elif poly[i][1]==1:
                        if poly[i][0]<0:
                            
                            newlist=newlist+" - "+str(abs(poly[i][0]))+"x"
                        else:
                            newlist=newlist+" + "+str(poly[i][0])+"x"

                    else:
                        if poly[i][0]<0:
                            newlist=newlist+" - "+str(abs(poly[i][0]))
                        else:
                            newlist=newlist+" + "+str(abs(poly[i][0]))
                else:
                    if poly[i][0]<0:
                        if poly[i][1]!=0 and poly[i][1]!=1:
                            newlist=newlist+" - "+"x"+"^"+str(poly[i][1])
                        elif poly[i][1]==1:
                            newlist=newlist+" - "+"x"
                        else:
                            newlist=newlist+" - 1"
                    

                    else:
                        if poly[i][1]!=0 and poly[i][1]!=1:
                            newlist=newlist+" + "+"x"+"^"+str(poly[i][1])
                        elif poly[i][1]==1:
                            newlist=newlist+" + "+"x"

                        else:
                            newlist=newlist+" + 1"
        

        return newlist                   


############################################################
# Section 7: Feedback
############################################################

feedback_question_1 = """
10hours
"""

feedback_question_2 = """
i think the section 6 is most challenging, especially 
dealing with strings, tuples, lists. there is no stumbling part for me.
"""

feedback_question_3 = """
i like the aspect of using class to programm in this assignment,
there is nothing i would have changed.
"""
