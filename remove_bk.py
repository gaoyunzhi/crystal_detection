'''
remove back ground for grey scale image
'''
import cv2

#constants
grid_size=10


def rm_bk(image):
    print 'start subprocess'
    h,w=image.shape
    print h,w
    assert (30<=h<=200) and (50<=w<=200)
    mu, sigma = map(int,cv2.meanStdDev(image)) 
    min, max=image.min(), image.max()
    th_black=(mu+min)/2 # assertion, change as needed
    g_h=h/grid_size+1
    g_w=w/grid_size+1
    bk=[[0 for _ in xrange(g_w)] for _ in xrange(g_h)]
    th=[[None for _ in xrange(g_w)] for _ in xrange(g_h)]
    num=[[1 for _ in xrange(g_w)] for _ in xrange(g_h)] # bias assertion, doesn't matter so much
    for i in xrange(h):
        for j in xrange(w):
            if image[i][j]>th_black:
                bk[i/grid_size][j/grid_size]+=image[i][j]
                num[i/grid_size][j/grid_size]+=1
    print 'finished counting'
    for i in xrange(g_h):
        for j in xrange(g_w):
            c_sum=0;c_num=0
            for u in xrange(-1,2):
                for v in xrange(-1,2):
                    if 0<=i+u<g_h and 0<=j+v<g_w:
                        c_sum+=bk[i+u][j+v]
                        c_num+=num[i+u][j+v]
            th[i][j]=c_sum/c_num-sigma
            
    for i in xrange(h):
        for j in xrange(w):
            if image[i][j]<th_black:
                image[i][j]=0
            elif image[i][j]>th[i/grid_size][j/grid_size]:
                image[i][j]=255
    
    filled=[[False for _ in xrange(w)] for _ in xrange(h)]            
    visited=set()

    for i1 in xrange(h):
        for j1 in xrange(w):
            if image[i1][j1]==255 and not (i1,j1) in visited:
                visited.add((i1,j1))
                aganda=[(i1,j1)]
                p=0
                while p<len(aganda):
                    i,j=aganda[p]
                    for u in xrange(-1,2):
                        for v in xrange(-1,2):
                            ii=i+u
                            jj=j+v
                            if 0<=ii<h and 0<=jj<w and image[ii][jj]==255 and not (ii,jj) in visited:
                                aganda.append((ii,jj))
                                visited.add((ii,jj))
                    p+=1
                print i1,j1,len(aganda),len(aganda)<h*w/10
                if len(aganda)<h*w/10:
                    for i,j in aganda:
                        image[i][j]=0
                        filled[i][j]=True
                          
    return image 


    