import itertools
import random
def getParams(NS,NB):
	NS_ = range(NS[0],NS[1]+1,NS[2])
	NB_ = range(NB[0],NB[1]+1,NB[2])

	a = [NS_,NB_]

	return list(itertools.product(*a))

def getRandom(NS,NB):
	a,b = (random.randrange(NS[0],NS[1]+1),
		random.randrange(NB[0],NB[1]+1))

	
        result = ((a/100)*100,(b/2)*2)
	return result

if __name__ == "__main__":
	#foo =(getParams((32000,98000,2000),(64,256,8)))
	foo =(getRandom((32000,98000,2000),(64,256,8)))
	print foo
	print len(foo)
