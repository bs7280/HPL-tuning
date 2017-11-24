import itertools
import random
def getParams(NS,NB):
	NS_ = range(NS[0],NS[1]+1,NS[2])
	NB_ = range(NB[0],NB[1]+1,NB[2])

	a = [NS_,NB_]

	return list(itertools.product(*a))

<<<<<<< HEAD
def getRandom(NS,NB,NS_base=100,NB_base=2):
    a,b = (random.randrange(NS[0],NS[1]+1),
    random.randrange(NB[0],NB[1]+1))


    result = ((a/NS_base)*NS_base,(b/NB_base)*NB_base)
    return result

def prepData(data):
    return list(map(lambda x: (x[1],x[0],float(x[0])/float(x[1]),(float(x[0])/float(x[1]))%1),data))

def getPredictor(lines):
    data = list(map(lambda x: x.replace("\r","").replace("\n","").split(","), lines))[1:]
    data = list(map(lambda x: ((int(x[0]),int(x[1])),float(x[3])),data))
    data = list(map(lambda x: ((x[0][0],x[0][1],float(x[0][1])/float(x[0][0]),float(x[0][1])/float(x[0][0])%1),x[1]),data))

    #return data 

    print data[:10]

    X,y = zip(*data)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42)
    lr = LinearRegression(normalize=True)
    lr.fit(X_train,y_train)
    
    return lr
    #return zip(lr.predict(X_test),y_test)

def getCanidates(lines,n,k,NS=(32000,120000),NB=(64,256)):

    lr = getPredictor(lines)

    r = list(map(lambda x: getRandom(NS,NB),range(0,n)))
    r = prepData(r)
    
    #return r
    l = zip(r,lr.predict(r))
    a,b = zip(*sorted(l,key=lambda x: x[1])[::-1][:k])
    return list(a)

=======
def getRandom(NS,NB):
	a,b = (random.randrange(NS[0],NS[1]+1),
		random.randrange(NB[0],NB[1]+1))

	
        result = ((a/100)*100,(b/2)*2)
	return result
>>>>>>> 3dd9b0d2287ec2cd240b6b81d9b0f99e766cbf89

if __name__ == "__main__":
	#foo =(getParams((32000,98000,2000),(64,256,8)))
	foo =(getRandom((32000,98000,2000),(64,256,8)))
	print foo
	print len(foo)
