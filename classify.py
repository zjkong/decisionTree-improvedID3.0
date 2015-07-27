
from train import *

def get_classification(record, tree):
    """
    This function recursively traverses the decision tree and returns a
    classification for the given record.
    """
    # If the current node is a boolean type, then we've reached a leaf node and
    # we can return it as our answer
    if type(tree) == type(True):
       return tree
    
    # Traverse the tree further until a leaf node is found.
    else:    
        attr = tree.keys()[0]
        if type(attr[0])!= type("string"):
            if record[attr[0]] <= attr[1]:
                temp = tree[attr]['left']
                return get_classification(record, temp)
            else:
                temp = tree[attr]['right']
                return get_classification(record, temp)
        else:
            temp = tree[attr][record[attr[0]]]
            return get_classification(record,temp)
 
def classify(tree, data):
    '''
    Returns a list of classifications for each of the records in the data
    list as determined by the given decision tree.
    '''
    classification = []
    
    for record in data:
        classification.append(get_classification(record, tree))

    return classification


def classify_forest(forest, data):
    
    classification = []
    for i in data:
        result = [get_classification(i, tree) for tree in forest] 
        if(result.count(False) >= result.count(True)):
            classification.append(False)
        else:
            classification.append(True)

    return classification
    
