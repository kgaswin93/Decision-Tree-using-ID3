import pandas
import tree
import utilities
import sys
training_data_file_path = sys.argv[1]
vaildation_data_file_path = sys.argv[2]
testing_data_file_path = sys.argv[3]
pruning_factor = float(sys.argv[4])
training_data = pandas.read_csv(training_data_file_path)
validation_data = pandas.read_csv(vaildation_data_file_path)
testing_data = pandas.read_csv(testing_data_file_path)
column_list = training_data.columns.values
attr = column_list[:-1]
classname = column_list[-1]
instance_classes = utilities. getInstanceClasses(training_data,classname)
instances = utilities. getInstances(training_data)
validation_instances = utilities. getInstances(validation_data)
validation_column_list = validation_data.columns.values
validation_attr = column_list[:-1]
testing_instances = utilities. getInstances(testing_data)
testing_column_list = testing_data.columns.values
testing_attr = column_list[:-1]
node_label = 1
parent = tree.make_tree(instances, instance_classes, attr, training_data, node_label)
print('Decision Tree : ')
tree.printTree(parent,0)
#Pre Prune Accuracy
print('-------------------')
print('Pre-Pruned Accuracy')
print('-------------------')
print('Number if Training instances = ',len(instances))
print('Number if Training attributes = ',len(attr))
print('Total number of nodes in the tree = ', tree.countNodes(parent))
print('Number of leaf nodes in the tree = ', tree.countPureNodes(parent))
print('Accuracy of the model on the training dataset : ',round(utilities.getAccuracy(parent,training_data)*100,2),'%')
print('')
print('Number if Validation instances = ',len(validation_instances))
print('Number if Validation attributes = ',len(validation_attr))
prePruneAccuracy = utilities.getAccuracy(parent,validation_data)
print('Accuracy of the model on the validation dataset before pruning : ', round(prePruneAccuracy*100,2),'%')
print('')
print('Number if Testing instances = ',len(testing_instances))
print('Number if Testing attributes = ',len(testing_attr))
print('Accuracy of the model on the testing dataset before pruning : ',round(utilities.getAccuracy(parent,testing_data)*100, 2),'%')
#pruning
maxPruneNodes = int(round(pruning_factor * tree.countNonPureNodes(parent),0))
tree.getNodesToBePruned(parent, maxPruneNodes, prePruneAccuracy, parent, validation_data)
nodesToBePruned = tree.nodeNames
#Post Prune Accuracy
print('--------------------')
print('Post-Pruned Accuracy')
print('--------------------')
print('Number if Training instances = ',len(instances))
print('Number if Training attributes = ',len(attr))
print('Total number of nodes in the tree = ', tree.countNodesAfterPruning(parent,nodesToBePruned))
print('Number of leaf nodes in the tree = ', tree.countPureNodesAfterPruning(parent,nodesToBePruned))
print('Accuracy of the model on the training dataset after pruning : ',round(utilities.postPruningAccuracy(parent, training_data, nodesToBePruned)*100,2),'%')
print('')
print('Number if Validation instances = ',len(validation_instances))
print('Number if Validation attributes = ',len(validation_attr))
print('Accuracy of the model on the validation dataset after pruning : ', round(utilities.postPruningAccuracy(parent, validation_data, nodesToBePruned)*100,2),'%')
print('')
print('Number if Testing instances = ',len(testing_instances))
print('Number if Testing attributes = ',len(testing_attr))
print('Accuracy of the model on the testing dataset after pruning : ',round(utilities.postPruningAccuracy(parent, testing_data, nodesToBePruned)*100, 2),'%')


print('--------------------')
print('Bonus Part')
print('--------------------')
random_tree = tree.make_random_tree(instances, instance_classes, attr, training_data, node_label)
print('')
print('Tree Parameters')
print('---------------')
print('Total number of nodes in the random tree = ', tree.countNodes(random_tree))
print('Average Depth of random tree : ',round((tree.getSumDepths(random_tree,0,0)/tree.countPureNodes(random_tree)),2))
print('Total number of nodes in the ID3 based Decision tree = ', tree.countNodes(parent))
print('Average Depth of ID3 based Decision tree : ',round((tree.getSumDepths(parent,0,0)/tree.countPureNodes(parent)),2))
print('')
print('Accuracy')
print('--------')
print('Accuracy of the model on the validation dataset using ID3 : ', round(prePruneAccuracy*100,2),'%')
for i in range(1,6):
    random_tree = tree.make_random_tree(instances, instance_classes, attr, training_data, node_label)
    print('Iteration ',i,' : ')
    print('Accuracy of the model on the training dataset : ', round(utilities.getAccuracy(random_tree, validation_data) * 100, 2), '%')


input('press Enter to exit')