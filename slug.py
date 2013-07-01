L=22
TH=50
THH=80

def process_lines(x):
    return map(int,x.split())

def findmin(start,direction):
    global rightmargin,leftmargin
    min=1
    
    
    if direction==1:
        rightmargin=N+1 
        for j in xrange(N-N/L-1,start-1,-1):
            if sum(compare[i][j:j+N/L])<min:
                rightmargin=j+N/L-1
                min=sum(compare[i][j:j+N/L])
        if rightmargin<N and compare[i][rightmargin]>TH: rightmargin=N+1 
        c=0
        while rightmargin<N and compare[i][rightmargin]<-TH and c<N/L: 
            rightmargin+=direction;c+=1 
    if direction==-1:
        leftmargin=-2
        for j in xrange(start-N/L+1):
            if sum(compare[i][j:j+N/L])<min:
                leftmargin=j-N/L+1
                min=sum(compare[i][j:j+N/L])
        if leftmargin>=0 and compare[i][leftmargin]>TH: leftmargin=-2
        c=0
        while leftmargin>=0 and compare[i][leftmargin]<-TH and c<N/L: 
            leftmargin+=direction; c+=1
    
def to_str(x):
    if x>TH: return '^'
    if x<-TH: return '-'
    return '0'    


def test_range(x):
    #if (i>=1537 and i<=1539): return True
    return False    
            
def number_of_nonzeros(x):
    return sum([y!=0 for y in x])

def find_slug(datafilename,locationfilename,resultfilename):
    global rightmargin,leftmargin,compare,N,L,i
    with open(datafilename,'r') as f:
        data=f.read().splitlines()
        data=map(process_lines,data)
    data=[data[0][:]]+data #alignment
    base=data[0][:]
    l=len(data)
    N=len(data[0])
    #print N/L
    compare=[[] for i in xrange(l)]
    #              where,len,pos  where=-2,no slug; where=-1, partial slug to the left; where=1, partial slug to the right;   where=0, whole slug in the center                   
    position_all=[(-2,0,0)]
    for i in xrange(1,l):
        where=-2;length=0;pos=0
        compare[i]=[data[i][x]-base[x] for x in xrange(N)]
        if test_range(i): print str(i)+' '*(5-len(str(i)))+''.join(map(to_str,compare[i]))
        max=0
        for j in xrange(N/L/2,N-N/L/2+1):
            if max<sum(compare[i][j-N/L/2:j+N/L/2]): 
                max=sum(compare[i][j-N/L/2:j+N/L/2])
                center=j
        if max<THH*(N/L/2)*2: 
            where=-2
        else:
            findmin(center-N/L/2,-1)
            findmin(center+N/L/2,1)
            if leftmargin<0: 
                where=-1
            elif rightmargin>=N: 
                where=1
            else:
                where=0
            if test_range(i): print '\t',max,center,leftmargin,rightmargin,sum(compare[i][rightmargin-N/L:rightmargin]),sum(compare[i][leftmargin+1:leftmargin+N/L+1]),-TH*N/L
            length=rightmargin-leftmargin
            pos=(rightmargin+leftmargin)/2
            if length>N-4*N/L or length<N/L:
                where=-2
            if rightmargin<N-1 and sum(compare[i][rightmargin-N/L:rightmargin])>-TH*N/L:
                flag=True
                for t in range(3):
                    rightmargin-=1
                    if sum(compare[i][rightmargin-N/L:rightmargin])<=-TH*N/L: 
                        flag=False;break
                if flag: where=-2
            if leftmargin>0 and sum(compare[i][leftmargin+1:leftmargin+N/L+1])>-TH*N/L:
                flag=True
                for t in range(3):
                    leftmargin+=1
                    if sum(compare[i][leftmargin+1:leftmargin+N/L+1])<=-TH*N/L: 
                        flag=False;break
                if flag: where=-2
            #if test_range(i):
            #    print max,THH*(N/L/2)*2,sum(compare[i][leftmargin+1:leftmargin+N/L+1]),-TH*N/L,leftmargin,
        if where==-2:
            length=0;pos=0;leftmargin=-2;rightmargin=0
        position_all.append((where,length,pos))
        if test_range(i): print '\t',where,length,pos
        leftend=0;rightend=N
        while rightend>0 and sum(compare[i][rightend-N/L:rightend])<-TH*N/L: rightend-=N/L
        if rightend<=N/2: rightend=N
        while leftend<N and sum(compare[i][leftend:leftend+N/L])<-TH*N/L: leftend+=N/L
        if leftend>N/2: leftend=0
        for x in range(leftend,leftmargin+1)+range(rightmargin,rightend):
            base[x]=base[x]*0.7+data[i][x]*0.3 

    f=open(locationfilename,'w')
    for line in position_all[1:]:
        f.write('\t'.join(map(str,line))+'\n')
    f.close()
    i=1
    slugs=[]
    while i<l-1:
        if position_all[i][2]>position_all[i+1][2]: #new slug
            length=0
            while position_all[i][0]==1:
                i+=1
                if position_all[i][1]>length: length=position_all[i][1]
            if position_all[i][1]>length: length=position_all[i][1]
            if length>2: slugs.append((length*100.0/N,i*0.3))
            while position_all[i][0]==0 or position_all[i][0]==-1:
                i+=1
        else:
            i+=1
    avglen=sum([x for (x,y) in slugs])/len(slugs)
    f=open(resultfilename,'w')
    for line in slugs:
        f.write('\t'.join(map(str,line))+'\n')
    f.write('avg length '+str(avglen))
    f.close()
            
            


#find_slug('data.txt','location.txt','result.txt')