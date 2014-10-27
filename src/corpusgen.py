__author__ = 'juliewe'
#take a file of templates and generate a corpus
#terminals are a list of quoted words or a database ref {1}
#nonterminals are a mixture of uppercase and _

import sys,re

class Rule:


    def __init__(self,text):
        self.text=text
        self.process()

    def getText(self):
        return self.text

    def getLeft(self):
        return self.left

    def process(self):
        parts = self.text.split(" --> ")
        self.left=parts[0]
        self.right=parts[1]
        self.processright()

    def processright(self):
        if self.right.startswith("["):
            self.processlex()
            self.isLex=True
        else:
            self.processgram()
            self.isLex=False

    def processgram(self):
        self.expansions=self.right.split(" ")

    def processlex(self):
        parts=self.right.split(",")
        self.expansions=[]
        for part in parts:
            self.expansions.append(self.clean(part))


    def clean(self,lexstring):

        if lexstring.startswith('['):
            result=lexstring[1:]
        else:
            result = lexstring

        if result.endswith(']'):
            stringlength=len(result)
            result=result[:stringlength-1]



        stringlength=len(result)
        result=result[1:stringlength-1]
        return result

    def show(self):
        result=self.left+"-->"
        for exp in self.expansions:
            #print exp
            result += exp+","
        return result


class CorpusGenerator:

    def __init__(self):
        self.rules={} #dictionary of rules

    def readfile(self,filename):
        debug=False

        print "Reading "+filename
        processed=0
        with open(filename) as instream:
            for line in instream:
                processed+=self.processline(line.rstrip())
                if processed>0 and debug:
                    break


    def processline(self,line):

        #check not blank or comment
        if(len(line)>0 and not line.startswith("//")):
            self.makerule(line)
            return 1
        else:
            return 0


    def makerule(self,line):
        newRule=Rule(line)
        left=newRule.getLeft()
        self.addrule(left,newRule)

    def addrule(self,key,rule):
        current = self.rules.get(key,[])
        current.append(rule)
        self.rules[key]=current

    def showrules(self):

        for key in self.rules.keys():
            for rule in self.rules[key]:
                print key, " : ", rule.show()


if __name__ =="__main__":

    filename=sys.argv[1]
    myGen = CorpusGenerator()
    myGen.readfile(filename)
    myGen.showrules()
