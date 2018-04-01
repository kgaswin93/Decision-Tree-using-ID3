import utilities
import random
nodeNames = []
pruneAccuracy = []
def make_tree(instances, instance_classes, attr, data, node_label):
    avgClassValue = float(utilities.avgClassValue(instance_classes))
    if avgClassValue > 0 and avgClassValue < 1 and len(attr) > 0 :
        max_attr = ''
        max_IG = -999
        max_child_instances = []
        for attr_value in attr[:] :
            parent_entropy = utilities.getEntropy(instance_classes)
            child = utilities.getChildInstances(data,attr_value,instances,instance_classes)
            left_child_entropy = utilities.getEntropy(child[0][1])
            right_child_entropy = utilities.getEntropy(child[1][1])
            length_left_child = len(child[0][0])
            length_right_child = len(child[1][0])
            length_parent = len(instances)
            IG = parent_entropy - ( ((length_left_child/length_parent)*left_child_entropy) + ((length_right_child/length_parent)*right_child_entropy) )
            if IG >= max_IG :
                max_IG = IG
                max_attr = attr_value
                max_child_instances = child
        parent = utilities.Node(None,None,None,None,None,None)
        parent.instances = instances
        parent.instance_classes = instance_classes
        parent.attr = max_attr
        attr = list(attr)
        attr.remove(max_attr)
        parent.left = make_tree(max_child_instances[0][0],max_child_instances[0][1],attr,data, (2*node_label))
        parent.right = make_tree(max_child_instances[1][0], max_child_instances[1][1], attr, data, ((2*node_label)+1))
        parent.label = node_label
        return parent
    else:
        parent = utilities.Node(None,None,None,None,None,None)
        parent.instances = instances
        parent.instance_classes = instance_classes
        parent.label = node_label
        if len(attr) == 0 :
            if avgClassValue >= 0.5 :
                parent.attr = 1
            else:
                parent.attr = 0
        else:
            parent.attr = int(avgClassValue)
        return parent
    return 0

def make_random_tree(instances, instance_classes, attr, data, node_label):
    avgClassValue = float(utilities.avgClassValue(instance_classes))
    if avgClassValue > 0 and avgClassValue < 1 and len(attr) > 0 :
        attr_value = attr[random.randint(0,len(attr)-1)]
        child = utilities.getChildInstances(data, attr_value, instances, instance_classes)
        parent = utilities.Node(None,None,None,None,None,None)
        parent.instances = instances
        parent.instance_classes = instance_classes
        parent.attr = attr_value
        attr = list(attr)
        attr.remove(attr_value)
        parent.left = make_random_tree(child[0][0],child[0][1],attr,data, (2*node_label))
        parent.right = make_random_tree(child[1][0], child[1][1], attr, data, ((2*node_label)+1))
        parent.label = node_label
        return parent
    else:
        parent = utilities.Node(None,None,None,None,None,None)
        parent.instances = instances
        parent.instance_classes = instance_classes
        parent.label = node_label
        if len(attr) == 0 :
            if avgClassValue >= 0.5 :
                parent.attr = 1
            else:
                parent.attr = 0
        else:
            parent.attr = int(avgClassValue)
        return parent
    return 0

def printTree(node, indent):
    parent = utilities.Node(None,None,None,None,None,None)
    parent = node
    print("| " * indent, end="")
    if isPureNode(parent.left) :
        print(parent.attr, ' = 0 : ',parent.left.attr)
    else:
        print(parent.attr, ' = 0 : ')
        printTree(parent.left, indent + 1)
    print("| " * indent, end="")
    if isPureNode(parent.right) :
        print(parent.attr,' = 1 : ', parent.right.attr)
    else:
        print(parent.attr,' = 1 : ')
        printTree(parent.right, indent + 1)

def isPureNode(node):
    parent = utilities.Node(None, None, None, None, None, None)
    parent = node
    return (type(parent.attr) is int )

def countNonPureNodes(node):
    if (isPureNode(node)) :
        return 0
    else:
        return (countNonPureNodes(node.left)+countNonPureNodes(node.right)+1)

def countPureNodes(node):
    if (isPureNode(node)) :
        return 1
    else:
        return (countPureNodes(node.left)+countPureNodes(node.right))

def countNodes(node):
    if (isPureNode(node)) :
        return 1
    else:
        return (countNodes(node.left)+countNodes(node.right)+1)

def countNodesAfterPruning(node,label):
    if (isPureNode(node) or node.label in label) :
        return 1
    else:
        return (countNodesAfterPruning(node.left,label)+countNodesAfterPruning(node.right,label)+1)

def countPureNodesAfterPruning(node,label):
    if (isPureNode(node) or node.label in label) :
        return 1
    else:
        return (countPureNodesAfterPruning(node.left,label)+countPureNodesAfterPruning(node.right,label))

def getNodesToBePruned(node, maxPruneNodes, accuracy, parent, data):
    if not(isPureNode(node)):
        if isPureNode(node.left) and isPureNode(node.right) :
            tempAccuracy = utilities.getTempPruneAccuracy(parent, data, node.label)
            if accuracy < tempAccuracy :
                if len(nodeNames) < maxPruneNodes :
                    nodeNames.append(node.label)
                    pruneAccuracy.append(tempAccuracy)
                else:
                    if min(pruneAccuracy) < tempAccuracy :
                        for i in range(0,maxPruneNodes): #optimize it later
                            if pruneAccuracy[i] == min(pruneAccuracy) :
                                pruneAccuracy[i] = tempAccuracy
                                nodeNames[i] = node.label
        else:
            getNodesToBePruned(node.left,maxPruneNodes, accuracy, parent, data)
            getNodesToBePruned(node.right,maxPruneNodes, accuracy, parent, data)

def getSumDepths(node,depth,sum_depth):
    if (isPureNode(node)) :
        sum_depth+=depth
        return sum_depth
    else:
        sum_depth = getSumDepths(node.left,depth+1,sum_depth)
        sum_depth = getSumDepths(node.right,depth+1,sum_depth)
        return sum_depth