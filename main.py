
from train import *
from classify import *
import sys
import os.path
import csv



def get_filenames():
    """
    Get the filename of training data and classification data
    """
    # Ask user to input the training data filename and classification data file
    # if there is no filename at the biginning
    if len(sys.argv) < 3:
        training_filename = raw_input("Training Filename: ")
        test_filename = raw_input("Test Filename: ")
    # otherwise, read the filenames from the command line
    else:
        training_filename = sys.argv[1]
        test_filename = sys.argv[2]
    def file_exists(filename):
        if os.path.isfile(filename):
            return True
        else:
            print "Error: The file '%s' does not exist." % filename
            return False
    # Print an error and exit execution if there is no target file
    if ((not file_exists(training_filename)) or
        (not file_exists(test_filename))):
        sys.exit(0)
    # Return the filenames of the training and classification data files
    return training_filename, test_filename

def read_in(filename):

    with open(filename, 'r') as fin:
        row = csv.reader(fin)
        data = []   
        for attr in row:
            dic = {}
            i = 0
            length = len(attr)-1
            for element in attr:
                if i==0 or i==2 or i==4 or i==10 or i==11 or i==12:
                    if element==" ?":
                        dic[i]= 0.0
                    else: dic[i]=float(element)
                elif i==length:
                    dic[i]=(element==" <=50K")
                else:
                    if element==" ?":
                        dic[str(i)]=""
                    else:dic[str(i)]=element
                i+=1
            data.append(dic)   
    return data, length

def read_last_coloumn(filename):
    with open(filename, 'r') as fin:
        row = csv.reader(fin)
        dic =[]  
        for attr in row:
            i = 0
            length = len(attr) -1
            for element in attr:
                if i==length:
                    dic.append(element==" <=50K.")
                i += 1
    return dic   
        

if __name__ == "__main__":
    """
    training_filename, test_filename = get_filenames()
    # Input the filename
    training_data, training_length = read_in( training_filename ) 
    
    
    print "------------------------\n"
    print "------- Training -------\n"
    print "------------------------\n"
    print "\n" 

    attr = [0,"1",2,"3",4,"5","6","7","8","9",10,11,12,"13",14]
    #dtree = create_decision_tree(training_data, attr, training_length, dynamic_bounds)

    forest = create_forest(bagging(training_data, 100000, 10000), attr, training_length)         #Two attribute need to be changed here


    training_data = ''
    test_data, test_length = read_in( test_filename )
    print "------------------------\n"
    print "--   Classification   --\n"
    print "------------------------\n"
    print "\n" 
    #classification_result = classify(dtree, test_data)

    classification_result = classify_forest(forest, test_data)
 
    
    print classfication_result
    # Output the classification
    with open('result.csv', 'wb') as result_classify:
        result_file = csv.writer(result_classify)
        for result in classification_result: 
            print result
            result_file.writerow([str(result)])
    
    """
    training_data, training_length = read_in("adult.data.csv")
    attr = [0,"1",2,"3",4,"5","6","7","8","9",10,11,12,"13",14]
    #dtree = create_decision_tree(training_data, attr, 14, dynamic_bounds)
    forest = create_forest(bagging(training_data, 100000, 10000), attr, training_length)    
    test_data, test_length = read_in("adult.test.csv") 
    #classification_result = classify(dtree, test_data)
    classification_result = classify_forest(forest, test_data)
    
    num_row = len(classification_result)
    compare_column = read_last_coloumn("adult.test.csv")
    correct = 0
    for i in range(num_row):
        if classification_result[i] == compare_column[i]:
            correct += 1
    
    print "Accuracy"
    print float(correct)/float(num_row)

    
    
    
    
    
    
    
    

