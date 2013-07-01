L=22
TH=40
THH=60

def process_lines(x):
    return map(int,x.split())

def findmin(start,direction):
    global rightmargin,leftmargin
    min=1
    
    
    if direction==1:
        rightmargin=N+1 
        for j in xrange(N-N/L-1,start-1,-1):
            if sum(compare[i][j:j+N/L])<min:
                rightmargin=j
                min=sum(compare[i][j:j+N/L])
        if rightmargin<N and compare[i][rightmargin]>TH: rightmargin=N+1 
        while rightmargin<N and compare[i][rightmargin]<-TH : rightmargin+=direction 
    if direction==-1:
        leftmargin=-2
        for j in xrange(start-N/L+1):
            if sum(compare[i][j:j+N/L])<min:
                leftmargin=j
                min=sum(compare[i][j:j+N/L])
        if leftmargin>=0 and compare[i][leftmargin]>TH: leftmargin=-2
        while leftmargin>=0 and compare[i][leftmargin]<-TH: leftmargin+=direction 
    
def to_str(x):
    if x>TH: return '^'
    if x<-TH: return '-'
    return '0'    


def test_range(x):
    if (i>=144 and i<148) or (i>=8 and i<=10): return True
    return False    
            
def number_of_nonzeros(x):
    return sum([y!=0 for y in x])

def find_slug(filename):
    global rightmargin,leftmargin,compare,N,L,i
    with open(filename,'r') as f:
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
        if test_range(i): print str(i)+' '*(4-len(str(i)))+''.join(map(to_str,compare[i]))
        if sum(compare[i][:N/L])>N/L*THH: # left case
            findmin(0,1)
            leftmargin=-1
            where=-1 #left
        if sum(compare[i][N-N/L:N])>N/L*THH: # right
            findmin(N,-1)
            rightmargin=N
            where=1 #right
        center=0
        for j in xrange(N-2*N/L):
            if sum(compare[i][j:j+2*N/L])>2*N/L*THH:
                center=1
                break       
        center=center*(where==-2) # whether there is a slug in the center
        if test_range(i):
            print center,j,sum(compare[i][j:j+2*N/L]),2*N/L*THH,sum(compare[i][55:55+2*N/L]),sum(compare[i][N-N/L:N]),N/L*THH
        if center:
            findmin(j,-1)
            findmin(j+2*N/L-1,1)  
            where=0
        if where!=-2:
            length=rightmargin-leftmargin
            pos=(rightmargin+leftmargin)/2
        if where==-2 or length>N-N/L or length<N/L or leftmargin==-2 or rightmargin==N+1:
            where=-2;pos=0;length=0
            leftmargin=-2;rightmargin=0
        position_all.append((where,length,pos))
        if test_range(i): print '\t',where,length,pos
        leftend=0;rightend=N
        while rightend>0 and sum(compare[i][rightend-N/L:rightend])<-TH*N/L: rightend-=N/L
        while leftend<N and sum(compare[i][leftend:leftend+N/L])<-TH*N/L: leftend+=N/L
        for x in range(leftend,leftmargin+1)+range(rightmargin,rightend):
            base[x]=base[x]*0.7+data[i][x]*0.3 
        
    f=open('output.txt','w')
    for line in position_all[1:]:
        f.write('\t'.join(map(str,line))+'\n')
    f.close()
    i=1
    slugs=[]
    while i<l-1:
        if position_all[i][2]>position_all[i+1][2]: #new slug
            while position_all[i][0]==1:
                i+=1
            #assert position_all[i][0]==0
            slugs.append((position_all[i][1],i))
            while position_all[i][0]==0 or position_all[i][0]==-1:
                i+=1
        else:
            i+=1
    f=open('slugs.txt','w')
    for line in slugs:
        f.write('\t'.join(map(str,line))+'\n')
    f.close()
            
            


find_slug('data.txt')