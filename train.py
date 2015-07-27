import math
import random
import sys
import collections
sys.setrecursionlimit(100000)

def majority_value(data, target_attr):
    """
    Creates a list of all values in the target attribute for each record
    in the data list object, and returns the value that appears in this list
    the most frequently.
    """
    return most_frequent([record[target_attr] for record in data])

def most_frequent(lst):
    """
    Returns the item that appears most frequently in the given list.
    """
    lst = lst[:]
    highest_freq = 0
    most_freq = None

    for val in unique(lst):
        if lst.count(val) > highest_freq:
            most_freq = val
            highest_freq = lst.count(val)
            
    return most_freq

def unique(lst):
    """
    Returns a list made up of the unique values found in lst.  i.e., it
    removes the redundant values in lst.
    """
    unique_lst = []

    # Cycle through the list and add each value to the unique list only once.
    for item in lst:
        if unique_lst.count(item) <= 0:
            unique_lst.append(item)
            
    # Return the list with all redundant values removed.
    return unique_lst

def get_values(data,attr):
    """
    Return a list which has unduplicable value of attribute in data records
    """
    data = data[:]
    return unique([record[attr] for record in data])

def eliminate_redundance(data, attributes, target_attr):
    """
    eliminate the attributes with only one value
    """

    temp_attributes = []
    # Return if there is only one column in the data
    if len(data) == 1:
       return (data, attributes)

    # Get the attributes list which is deleted later
    for attr in attributes:
        if attr != target_attr:
           vals = [record[attr] for record in data]
           if vals.count(vals[0]) == len(vals):
              temp_attributes.append(attr)
    
    # Delete attributes and build a new data copy to return avoiding mutation
    data = [{key:value for (key,value) in record.items() if key not in temp_attributes} for record in data]

    for x in temp_attributes:
        attributes.remove(x)
       
    return (data, attributes)  
             
def choose_attribute(data, attributes, target_attr, fitness):
    """
    Cycles through all the attributes and returns the attribute with the
    highest information gain (or lowest entropy).
    """
    best_attr = None
    best = (0, 0.0)  

    for attr in attributes:
        if attr!= target_attr:
            if type(attr)!=type("str"):
                best_temp = fitness(data, attr, target_attr)
                if best_temp[1] >= best[1]:
                    best = best_temp
                    best_attr = attr
            else: 
                best_temp = gain(data, attr, target_attr)
                if best_temp[1] >= best[1]:
                    best = best_temp
                    best_attr = attr
     
        
   
    print (best_attr, best)            
    return (best_attr, best[0])

def gain(data, attr, target_attr):
    """
    Calculates the information gain(reduction in entropy) that would 
    result by splitting the data on the chosen attribute(for uncontinuous
    string)
    
    """
    val_freq = {}
    sub_entropy = 0.0
    # Calculate the frequency of each of the values in the target attribute
    for record in data:
        if (val_freq.has_key(record[attr])):
            val_freq[record[attr]] += 1.0
        else: 
           val_freq[record[attr]] =1.0
        
    # Calculate the the increasing entropy value according to attr
    # Using entropy method to calculate the entropy of a attribute which has the same value
    
    for key in val_freq.keys():
        probability = val_freq[key]/sum(val_freq.values())
        sub_data = [record for record in data if record[attr]==key]
        sub_entropy += probability * entropy(sub_data,target_attr)
        
    # Substract the entropy of the chosen attribute from the entropy of the
    # whole data set with respect to the target attribute and return it
    return ('empty', entropy(data,target_attr)-sub_entropy)  
    
    
def get_examples_continuous(data, attr_tuple):
    """
    Returns a list of all the records in <data> with the value of <attr>
    matching the given value.
    """
    lst1 = []
    lst2 = []     
   
    for record in data:
        if record[attr_tuple[0]] <= attr_tuple[1]:
           lst1.append({key:value for (key,value) in record.items() if key != attr_tuple[0]})
        else:
           lst2.append({key:value for (key,value) in record.items() if key != attr_tuple[0]})
    
    return (lst1, lst2)                  
       
def get_examples_string(data,attr,value):
    """
    Returns a list of all the records in <data> with the value of <attr>
    Matching the given value
    
    """
    data = data[:]
    rtn_lst = []
    
    if not data:
        return rtn_lst
    else:
        rtn_lst = [{key:value for (key,value) in record.items() if key != attr} for record in data if record[attr] == value]
        return rtn_lst    
    

def entropy(data, target_attr):
    """
    Calculates the entropy of the given data set for the target attribute.
    """
    val_freq = {}
    data_entropy = 0.0

    # Calculate the frequency of each of the values in the target attr
    for record in data:
        if (val_freq.has_key(record[target_attr])):
            val_freq[record[target_attr]] += 1.0
        else:
            val_freq[record[target_attr]] = 1.0

    # Calculate the entropy of the data for the target attribute
    for freq in val_freq.values():
        data_entropy += (-freq/len(data)) * math.log(freq/len(data), 2) 
        
    return data_entropy
    
            
def dynamic_bounds(data, attr, target_attr):
    """
    Use dynamic bounds to calculate the entropy for each bound in the same
    column.
    """
    # Caculating dynamic bounds to decrease the branches of the trees
    
    temp_entropy = {}
                
    # Get the subset of the data corresponding to the given attribute
    
    data_subset = [record[attr] for record in data]
    data_subset.sort()
    data_subset.reverse()
    unique_data = unique(data_subset)
    length = float(len(data_subset))

    for val in unique_data:
        less_counter = length - data_subset.index(val)
        greater_counter = float(data_subset.index(val)) 
        if(less_counter != 0.0):
            t = (-less_counter/length) * math.log(less_counter/length, 2)
        if(greater_counter != 0.0):
            t += (-greater_counter/length) * math.log(greater_counter/length, 2)
        if t != 0.0: 
           temp_entropy[val] = t    

   
    seperatePoint = max(temp_entropy.iteritems(), key=lambda x:x[1])[0]
   
    lst1,lst2 = get_examples_continuous(data,(attr,seperatePoint))
    probability= float(len(lst1))/float((len(lst1)+len(lst2)))
   
    totalGain = entropy(data,target_attr) - probability*entropy(lst1,target_attr) - (1-probability)*entropy(lst2,target_attr)
    if(totalGain < 0):
       totalGain = 0.0 
    
    return (seperatePoint,totalGain)          




def create_decision_tree(data, attributes, target_attr, fitness_func):
    """
    Returns a new decision tree based on the examples given.
    """
    data_tuple = eliminate_redundance(data, attributes, target_attr)
    data = data_tuple[0]
    attributes = data_tuple[1]  
    vals = [record[target_attr] for record in data]
    default = majority_value(data, target_attr)    

    if not data or (len(attributes) - 1) <= 0:
       print default
       return default
    
    elif vals.count(vals[0]) == len(vals):
       return vals[0]

    else:
        # Choose the next best attribute to best classify our data
        best = choose_attribute(data, attributes, target_attr, fitness_func)
        tree = {best:collections.defaultdict(lambda: default)}
        
        # when the data attribute is continuous
        
        if (best[1]!="empty"):
        
            # Create a new decision tree/sub-node for each of the values in the
            # best attribute field
            subdataset_tuple = get_examples_continuous(data, best)
            subattr = [attr for attr in attributes if attr != best[0]]
            subtree1 = create_decision_tree(
                    subdataset_tuple[0],
                    subattr,
                    target_attr,
                    fitness_func)
            subtree2 = create_decision_tree(
                    subdataset_tuple[1],
                    subattr,
                    target_attr,
                    fitness_func)
            
            tree[best]['left'] = subtree1
            tree[best]['right'] = subtree2
            
        # when the data attribute is not continuous(string)    
        else: 
            for val in get_values(data,best[0]):
                # Create a subtree to the current value under the "best" field
                subtree = create_decision_tree(
                    get_examples_string(data,best[0],val),
                    [attr for attr in attributes if attr!=best[0]],
                    target_attr, fitness_func)
                
                tree[best][val] = subtree
                    
    return tree


def bagging(training_data, num_vertical, num_rows ):

    #list of the rows used to create smaller decision tree
    sub_dtree = []
    # Total number of subtrees
    num_subtrees = ( num_vertical / num_rows ) + 1
    for k in range(0, num_subtrees):
        sub_dtree.append(random.sample(training_data, num_rows))

    return sub_dtree      



def create_forest(training_data_lst, attributes, target_attr):

    #list of decision tree 
    forest = []
    j=0
    for i in training_data_lst:
        print j
        forest.append(create_decision_tree(i, attributes, target_attr, dynamic_bounds))
        j+=1
    return forest

