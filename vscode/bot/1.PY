n =int(input())
for i in range (2,n//2):
    for j in range (i+1,n//2):
        for k in range (j+1,n//2):
            if i**2+j**2==k**2:
                print ("%d\t%d\t%d"%(i,j,k))