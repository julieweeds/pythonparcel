__author__ = 'juliewe'
import sys
from nltk import CFG
from nltk.parse.generate import generate

class CorpusGenerator:

    no_sents=10
    debug=False

    def __init__(self):
        self.grammarstring=""

    def readfile(self,filename):


        print "Reading "+filename
        processed=0
        with open(filename) as instream:
            for line in instream:
                processed+=self.processline(line)
                if processed>0 and CorpusGenerator.debug:
                    break
        self.grammar=CFG.fromstring(self.grammarstring)
        self.start=self.grammar.start()

    def processline(self,line):

        #check not blank or comment
        if(len(line)>0 and not line.startswith("//")):
            self.grammarstring+=line+" "
            return 1
        else:
            return 0

    def showgrammar(self):
        print self.grammar

    def generate(self,topstart="top",n=no_sents):
        if topstart=="top":
            topstart=self.start
        else:
            topstart=self.findstart(topstart)

        if n>0:
            max=n
        else:
            max=CorpusGenerator.no_sents

        sentences=0
        for sentence in generate(self.grammar,start=topstart,n=max):
            if max<100000000:
                print (' '.join(sentence))
            sentences+=1
        print "Produced sentences: "+str(sentences)

    def findstart(self,start):
        for prod in self.grammar.productions():
            if str(prod.lhs())==start:
                return prod.lhs()


if __name__=='__main__':

    filename=sys.argv[1]
    if len(sys.argv)>2:
        start=sys.argv[2]
    else:
        start="top"
    if len(sys.argv)>3:
        no_sents=int(sys.argv[3])
    else:
        no_sents=0
    myGen = CorpusGenerator()
    myGen.readfile(filename)
    print "Starting with rules for: "+start
    myGen.showgrammar()
    myGen.generate(start,n=no_sents)


