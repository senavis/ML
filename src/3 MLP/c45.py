from numpy import *
from math import *

class LearnItem:
	def __init__(self, attrs, class_n):
		self.At = attrs
		self.Class_N = class_n

	def __str__(self):
		return str(self.At) + " " + str(self.Class_N)

class TreeNode:
	Count = 0
	def __init__(self, st):
		TreeNode.Count += 1
		self.ID = TreeNode.Count
		self.Set = st
		self.Left = None
		self.Right = None
		self.DivValue = 0.0
		self.AttrNum =  0

	def setValues(self, attr_n, div_val, left, right):
		self.Left = left
		self.Right = right
		self.DivValue = div_val
		self.AttrNum = attr_n

def freq(all_set, class_n):
	if len(all_set) == 0: return 0.0
	frec = 0.0
	for s in all_set:
		if s.Class_N == class_n: frec += 1
	return frec / len(all_set)

def info(st, class_count):
	inf = 0
	for i in range(class_count):
		prob = freq(st, i)
		if prob > 0:
			inf = inf + log(prob, 2) * prob
	return -inf

def learn(node, class_n):
	if len(node.Set) == 0: print "Fuck"
	learn_set = node.Set
	def_class = learn_set[0].Class_N
	bb = True
	for li in learn_set:
		bb = bb and (li.Class_N == def_class)

	if bb:
		#print 'Shut up!', len(learn_set)
		return
	dim = learn_set[0].At.shape[0]
	inf = info(learn_set, class_n)

	max_info = -1000.0
	max_left = []
	max_right = []
	max_at = 0
	max_div_val = 0.0

	for i in range(dim):
		reduct = [li.At[i] for li in learn_set]
		reduct = sorted(reduct)

		for k in range(1, len(reduct)):
			left = []
			right = []

			mid_val = (reduct[k-1] + reduct[k]) / 2

			for d in range(len(reduct)):
				if learn_set[d].At[i] > mid_val:
					right.append(learn_set[d])
				else:
					left.append(learn_set[d])

			info_x = info(left, class_n) * len(left) / len(learn_set) + info(right, class_n) * len(right) / len(learn_set)
			max_info_cand = inf - info_x
			#print max_info_cand
			if max_info_cand > max_info:
				max_info = max_info_cand
				max_left = left
				max_right = right
				max_at = i
				max_div_val = mid_val

	if len(max_left) > 0: node.Left = TreeNode(max_left)
	if len(max_right) > 0: node.Right = TreeNode(max_right)
	node.DivValue = max_div_val
	node.AttrNum = max_at

	#print max_info, max_at, max_div_val
	#print '***************************'

	if len(max_left) > 0 and len(max_right) > 0:
		if len(max_left) > 1:
			learn(node.Left, class_n)

		if len(max_right) > 1:
			learn(node.Right, class_n)


def classify(tree_node, item):
	if tree_node.Left == None and tree_node.Right == None: return tree_node.Set[0].Class_N
	#print 'item[%d] > %f' % (tree_node.AttrNum, tree_node.DivValue)
	if item.At[tree_node.AttrNum] > tree_node.DivValue:
		return classify(tree_node.Right, item)
	else:
		return classify(tree_node.Left, item)


def draw_tree(tree_root):
	import pygraphviz as pgv
	G = pgv.AGraph()

	def walk_draw_tree(g, tree_node, parent):
		g.add_node(tree_node.ID)
		if parent != None:
			g.add_edge(parent.ID, tree_node.ID)

		nd = g.get_node(tree_node.ID)
		if tree_node.Left == None and tree_node.Right == None:
			nd.attr['label'] = 'Class #%d' % (tree_node.Set[0].Class_N)
			nd.attr['color'] = 'green'
			return

		nd.attr['label'] = 'd[%d] <= %f' % (tree_node.AttrNum, tree_node.DivValue)
		nd.attr['shape'] = 'box'
		nd.attr['color'] = 'blue'

		if tree_node.Left != None: walk_draw_tree(g, tree_node.Left, tree_node)
		if tree_node.Right != None: walk_draw_tree(g, tree_node.Right, tree_node)

		return

	walk_draw_tree(G, tree_root, None)

	G.draw('tree.png', prog='dot')

def load_ion():
	f = open("ionosphere.data", "rt")
	vecs = []
	count = 0;
	for l in f:
		spl = l.split(',')
		if len(spl) < 3: continue
		if spl[34] == 'g\n': cls = 0
		else: cls = 1

		vec = array( [float(s) for s in spl[0:34]] )
		vecs.append(LearnItem(vec, cls))
		count += 1
	f.close()
	return vecs

def load_iris():
	f = open("iris.data", "rt")
	vecs = []
	count = 0;
	for l in f:
		spl = l.split(',')
		if len(spl) < 3: continue
		cls = 0
		if count < 50:
			cls = 0
		elif count < 100:
			cls = 1
		else:
			cls = 2
		vec = array( [float(s) for s in spl[0:4]] )
		vecs.append(LearnItem(vec, cls))
		count += 1
	f.close()
	return vecs

def load_wine():
	f = open("wine.data", "rt")
	vecs = []
	count = 0;
	for l in f:
		spl = l.split(',')
		if len(spl) < 3: continue
		cls = 0

		if count < 59:
			cls = 0
		elif count < 129:
			cls = 1
		else:
			cls = 2

		vec = array( [float(s) for s in spl[0:34]] )
		vecs.append(LearnItem(vec, cls))
		count += 1
	f.close()
	return vecs

#data_set = load_wine()

#data_set = load_iris()

data_set = load_ion()
tree_root = TreeNode(data_set)

#print freq(data_set, 0)
#print info(data_set, 3)
print learn(tree_root, 2)

#print classify(tree_root, LearnItem(array([5.1, 3.5, 1.4, 0.2]), 0))
#print classify(tree_root, LearnItem(array([6.0, 2.7, 5.1, 1.6]), 0))
#print classify(tree_root, LearnItem(array([6.7, 2.5, 5.8, 1.8]), 0))
count = 0

#print count, classify(tree_root, data_set[186]), data_set[186]
for ds in data_set:
	cls = classify(tree_root, ds)
	if cls != ds.Class_N: print 'Error'
	print count, classify(tree_root, ds), ds.Class_N
	count += 1

#draw_tree(tree_root)

print TreeNode.Count