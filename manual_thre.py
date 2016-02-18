import numpy as np
import csv
import math
import operator
import copy
from random import sample
class cluster:
	w_low = 0.7
	w_up  = 0.3	
	def __init__(self):
		self.lower=[]
		self.upper=[]
		self.boundary=[]
		self.lower_extra=[]
		self.boundary_extra=[]
                self.sum_low_membership=0
                self.sum_up_membership=0
                self.upper_membership=[]
	def add_lower(self,val,row):
		self.lower.append(row)
		row =row * val
		self.lower_extra.append(row)
		self.sum_low_membership=self.sum_low_membership+val
	def add_boundary(self,val, row):
		self.boundary.append(row)
		self.upper_membership.append(val)
		row =row * val
		self.boundary_extra.append(row)
		self.sum_up_membership=self.sum_up_membership+val
	def show(self):
		print "lower bound"
		print len(self.lower)
		print "boundary bound "
		print len(self.boundary)
	def find_new_cluster(self):
 	   #	self.boundary = [row for row in self.upper if row not in self.lower]
		sum1 =  sum(self.lower_extra)
		len1 = len(self.lower)
		len2 = len(self.boundary)
		print "length of lower",len1
		print "length of boundary",len2
		if len1 == 0:
		        print "lower is empty"
		        kaka=raw_input()
		if len2 > 0:
			sum2  =  sum(self.boundary_extra)
			term1 = calculation(cluster.w_low,self.sum_low_membership,sum1)
			term2 =  calculation(cluster.w_up,self.sum_up_membership,sum2)
		        term1=np.array(term1)
		        term2=np.array(term2)	
		        sum_total =  term1+term2
			return sum_total	 
		else:
			new_w_low = 1
			term1 = calculation(new_w_low,self.sum_low_membership,sum1)	
			return term1 
	def delete(self):
		del self.lower[:]
		del self.upper[:]
		del self.boundary[:]
		del self.boundary_extra[:]
		del self.lower_extra[:]
		del self.upper_membership[:]
		self.sum_low_membership=0
		self.sum_up_membership=0
	def add_up_low(self,x):
		self.lower.append(x)
		self.upper.append(x)
	
	def compare_lower(self, a):
	        for row in self.lower:
                        if row == a:
	                        return 1
	        return 0
	def compare_boundary(self,a):
	        for row in self.boundary:
	               if row == a:
	                        return 1
	        return 0                   						
def calculation(weight,leng1,summ):	
        final_cal= (weight*summ)/leng1
        return final_cal
def checkforequal(a=None,b=None):
        print len(a)
        print len(b)
	a=np.array(a).astype(float)
	b=np.array(b).astype(float)
	print a
        print b
        val = distancee(a,b)
        print "val is ",val
  #      kak=raw_input()
        if val < 0.03:
                return 1
        else:
                return 0        
def change_precision(p,a):
        val=float(a)	
	val=round(val,p)
	return val
def distancee(A=None,B=None):
	distances =(A-B)**2
	distances=distances.sum(axis=-1)
	distances=np.sqrt(distances)
	return distances		
if __name__ =='__main__':
	threshold=0.02
	count=1
        reader=np.array(list(csv.reader(open("sample.txt","r"),delimiter=',')))	
#	X=copy.deepcopy(reader[:,:])
	rows=len(reader)
	print "rows are",rows
	cols=len(reader[0])
	print "cols are", cols
	X=list()
	reader=np.array(reader).astype('float')
	#converting into 1 dimension
	for i in xrange(0,rows):
	        for j in xrange(0,cols):
	                X.append(reader[i][j]) 
	X=np.array(X).astype('float')
	Xrows=len(X)
	old_mem_collector=list()
	old_mem_collector=[1 for i in xrange(0,Xrows)]
	new_mem_collector=list()
	print "Enter the number of clusters you want"
        k = input()
        V=list()	
  #	V=np.zeros((k,cols))
   #   	V=np.array(X).astype('float')
	litee= sample(xrange(Xrows),k)
	for i in xrange(0,k):
                V.append(X[litee[i]])
	V=np.array(V).astype('float')
	c=[]
        for i in xrange(0,k):
		c.append(cluster())
	#calculating the distance between the cluster centers and the data points
	dist={}
	U={}
	flag = 1
	cc=0
	sum_mem=0
	print "first seq is",litee
#	kak=raw_input()
	while flag == 1:
	        print "count is" 
	        print count 	
	#	kak=raw_input()            			      
		if count > 1:
		        for xx in xrange(0,k):
			        c[xx].delete()	
		        
		for i in xrange(0,Xrows):
		        dist.clear()   #you can use dist = {} also
	        	U.clear()
		        deno=0
		        for j in xrange(0,k):		
		        	distances =X[i]-V[j]
		        	dist[j]=distances**2
		#	print dist
		#       sum_val=summ_cluster_data_distances(dist)
	#	        print "distances are",dist
		        mini_key=min(dist.iteritems(), key=operator.itemgetter(1))[0]
		        if dist[mini_key] == 0:
		                new_mem_collector.append(1)
		                c[int(mini_key)].add_lower(1,X[i])
		        else:
		                for pp in xrange(0,k):
		                        for ij in xrange(0,k):
		                                deno = deno+((dist[pp]/dist[ij])**2)
		                        U[pp]=1/deno
		                        deno=0

			        first_max_key=max(U.iteritems(), key=operator.itemgetter(1))[0]
	   		        first_max_value=U[first_max_key]
			                
			        del U[first_max_key]    	# can also use U.pop('key')
		                second_max_key=max(U.iteritems(), key=operator.itemgetter(1))[0]
        	                second_max_value=U[second_max_key]
 			        diff=(first_max_value-second_max_value)
	        		if diff < threshold :
			                new_mem_collector.append((first_max_value+second_max_value)/2)
			                c[int(first_max_key)].add_boundary(first_max_value,X[i])
                	        	c[int(second_max_key)].add_boundary(second_max_value,X[i])
	                        		
	                        else:
	                               	new_mem_collector.append(1)
			        	c[int(first_max_key)].add_lower(1,X[i])

		V_new = []
		del V_new[:] 	#for future, delete all elements
        	for i2 in xrange(0,k):
			V_new.append(c[i2].find_new_cluster())
        	#checking cluster distance
        	V_new=np.array(V_new)
#        	print "len of old v",len(V)
#        	print "len of new v",len(V_new)
        	for i3 in xrange(0,k):
        	        for j in xrange(0,k):
        	                if i3 == j:
        	                        continue
        	                print "distance between %d cluster and %d cluster is" %(i3+1,j+1)
        	                print V_new[i3] - V_new[j]
                               
        	V_new=V_new.tolist()
        	# end
        	V=V.tolist()
	#	new_mem_collector=change_precision(5,new_mem_collector)
		print "comparing clusters result"
	#	print checkforequal(old_mem_collector,new_mem_collector)
		if checkforequal(old_mem_collector,new_mem_collector):
			flag = 0
		else:
			flag = 1
			del old_mem_collector[:]
			old_mem_collector=copy.deepcopy(new_mem_collector)
			del new_mem_collector[:]
			cc=0
		if flag == 1:
		        del V[:]
			V = copy.deepcopy(V_new)
		count=count+1
		V=np.array(V)
	
	print "final clusters are :"
	print V
	print "Final answer is \n"
		
	for i in xrange(0,k):
			print "The lower bound and upper bound of %s cluster is " %(i+1)
			c[i].show()

        #making the image 
        i_matrix=[]
        for i in xrange(0,Xrows):
                flagg=0
                average=0
                for j in xrange(0,k):
                         if c[j].compare_lower(X[i]):
                         #       print "lower",j                
                                i_matrix.append(int(math.ceil(V[j])))
                         elif c[j].compare_boundary(X[i]):
                          #     print "boundary",j
                                averag = (averag+V[j])/2
                                flagg=flagg+1
                if flagg==2:
                        averag=int(math.ceil(averag))          
                        i_matrix.append(averag) 
        # convert back into matrix
        image_matrix=list()
        count=0
        for i in xrange(0,rows):
                tempp=list()
                for j in xrange(0,cols):
                        tempp.append(i_matrix[count])
                        count=count+1
                image_matrix.append(tempp)                
        #image_matrix=change_precision(0,image_matrix)
        image_matrix=np.array(image_matrix).astype('uint8')
        np.savetxt("foo.csv",image_matrix,delimiter=",")
        
