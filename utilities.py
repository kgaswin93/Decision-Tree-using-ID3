import math
import random
import tree
class Node:
    def __init__(self, instances, instance_classes, attr, left, right, label):
        self.instances = instances
        self.instance_classes = instance_classes
        self.attr = attr
        self.left = left
        self.right = right
        self.label = label

def getInstanceClasses(training_data,classname):
    instance_classes = []
    for class_value in training_data[str(classname)]:
        instance_classes.append(class_value)
    return instance_classes

def getInstances(training_data):
    instances = []
    for index, row in training_data.iterrows():
        instances.append(index)
    return instances

def getEntropy(instance_classes):
    p,np = 0,0
    total_length = len(instance_classes)
    entropy_value = 0
    for value in instance_classes[:] :
        if value > 0 :
            p+=1
        else:
            np+=1
    #print(p,np,total_length)
    if p>0 :
        ep = -1*(p/total_length)*math.log((p/total_length),2)
    else:
        ep = 0
    if np>0 :
        enp = -1*(np/total_length)*math.log((np/total_length),2)
    else:
        enp = 0
    entropy_value = (ep + enp)
    return entropy_value

def getChildInstances(data,attr_value,instances,instance_classes):
    left_child = []
    left_child_classes = []
    right_child = []
    right_child_classes = []
    attr_instances = []
    for value in data[str(attr_value)]:
        attr_instances.append(value)

    for (instance, class_value) in zip(instances, instance_classes):
        if attr_instances[instance]>0 :
            right_child.append(instance)
            right_child_classes.append(class_value)
        else :
            left_child.append(instance)
            left_child_classes.append(class_value)
    left = [left_child,left_child_classes]
    right = [right_child,right_child_classes]
    return [left,right]

def avgClassValue(instance_classes):
    if len(instance_classes) > 0 :
        sum = 0
        for class_value in instance_classes[:] :
            sum+=class_value
        return (sum/len(instance_classes))
    else:
        return random.randint(0,1)

def getAccuracy(node, data):
    p = 0
    temp = Node(None,None,None,None,None,None)
    instances = []
    for index, row in data.iterrows():
        instances.append(index)
    column_list = data.columns.values
    classname = column_list[-1]
    instance_classes = []
    for class_value in data[str(classname)]:
        instance_classes.append(class_value)
    for i in range(0,len(instances)) :
        temp = node
        while not(tree.isPureNode(temp)):
            if(data[temp.attr][i] > 0):
                temp = temp.right
            else:
                temp = temp.left
        if temp.attr == instance_classes[i] :
            p+=1
    return (p/len(instances))

def getTempPruneAccuracy(node, data, label):
    p = 0
    temp = Node(None,None,None,None,None,None)
    instances = []
    for index, row in data.iterrows():
        instances.append(index)
    column_list = data.columns.values
    classname = column_list[-1]
    instance_classes = []
    for class_value in data[str(classname)]:
        instance_classes.append(class_value)
    for i in range(0,len(instances)) :
        temp = node
        while not(tree.isPureNode(temp)):
            if temp.label == label:
                break
            else:
                if(data[temp.attr][i] > 0):
                    temp = temp.right
                else:
                    temp = temp.left
        if temp.label == label :
            avgValue = avgClassValue(temp.instance_classes)
            if (instance_classes[i] and avgValue >= 0.5) or (not(instance_classes[i]) and avgValue < 0.5) :
                p+=1
        else:
            if temp.attr == instance_classes[i] :
                p+=1
    return (p/len(instances))

def postPruningAccuracy(node, data, label):
    p = 0
    temp = Node(None,None,None,None,None,None)
    instances = []
    for index, row in data.iterrows():
        instances.append(index)
    column_list = data.columns.values
    classname = column_list[-1]
    instance_classes = []
    for class_value in data[str(classname)]:
        instance_classes.append(class_value)
    for i in range(0,len(instances)) :
        temp = node
        while not(tree.isPureNode(temp)):
            if temp.label in label:
                break
            else:
                if(data[temp.attr][i] > 0):
                    temp = temp.right
                else:
                    temp = temp.left
        if temp.label in label :
            avgValue = avgClassValue(temp.instance_classes)
            if (instance_classes[i] and avgValue >= 0.5) or (not(instance_classes[i]) and avgValue < 0.5) :
                p+=1
        else:
            if temp.attr == instance_classes[i] :
                p+=1
    return (p/len(instances))