my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb

def divideset(rows,column,value):
    if isinstance(value,int) or isinstance(value,float):
        split_function = lambda row: row[column]>=value
    else:
        split_function = lambda row: row[column]==value

    set1=[row for row in rows if split_function(row)]
    set2=[row for row in rows if not split_function(row)]
    return (set1, set2)

def uniquecounts(rows):
    classcounts = {}
    for row in rows:
        # we care about the last column, the class column
        theclass = row[len(row)-1]
        if theclass not in classcounts: classcounts[theclass]=0
        classcounts[theclass]+=1
    return classcounts

def entropy(rows):
    from math import log
    log2=lambda x: log(x)/log(2)
    classcount = uniquecounts(rows)
    entropy = 0.0
    for theclass in classcount.keys():
        p = float(classcount[theclass])/len(rows)
        entropy -= p*log2(p)
    return entropy

def buildtree(rows,scoref=entropy):
    if len(rows)==0: return decisionnode()

    # Set up some variables to track the best split
    lowest_impurity = scoref(rows)
    best_split = None
    best_sets = None
    
    column_count = len(rows[0])-1

    for col in range(0,column_count):
        # Generate the list of different values in this column
        column_values = {}
        for row in rows: column_values[row[col]] = 1
        # Now divide the rows up for each value in this column
        for value in column_values.keys():
            (set1,set2) = divideset(rows,col,value)
            exp_impurity = float(len(set1))/len(rows) * scoref(set1) + float(len(set2))/len(rows) * scoref(set2)
            if exp_impurity < lowest_impurity and len(set1)>0 and len(set2)>0:
                lowest_impurity = exp_impurity
                best_split = (col,value)
                best_sets = (set1,set2)

    if lowest_impurity < scoref(rows):
        trueBranch = buildtree(best_sets[0],scoref)
        falseBranch = buildtree(best_sets[1],scoref)
        return decisionnode(col=best_split[0],value=best_split[1],
                            tb=trueBranch, fb=falseBranch)
    else:   
        return decisionnode(results=uniquecounts(rows))

def printtree(tree, indent='  '):
    if tree.results != None:
        print tree.results
    else:
        print str(tree.col) + ':' + str(tree.value) + '?'

        print indent+'T->',
        printtree(tree.tb, indent+'  ')
        print indent+'F->',        
        printtree(tree.fb, indent+'  ')        

#print divideset(my_data,2,'yes')
print uniquecounts(my_data)
print entropy(my_data)
tree = buildtree(my_data)
printtree(tree)