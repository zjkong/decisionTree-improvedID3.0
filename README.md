# decisionTree-improvedID3.0
predicted results with improved ID3.0 algorithm
1 This project contains 5 files: adult.data, adult.test, classify.py, main.py, train.py.
2 adult.data and adult.test can be opened with excel, the rest of files can be opened with python IDLE,
  if you haven't installed python, go to https://www.python.org/downloads/ and download it.
  (version 2.x.x is most suitable to this project and version 3.x.x may cause some errors while running)
3 According to extract the data from adult.data, I implemented several decision trees forming a forest to 
  predict results in adult.test and output accuracy of prediction.
4 In train.py method create_forest is used to create decision trees.
  classify.py received decision trees from train.py and classify each records from adult.test.
  main.py 
5 Through running main.py, it could predict results in 2 minutes and output accuracy at last. In main.py, by
  changing parameters in bagging function, the number of decision trees as well as the number of data is
  used to create a decision tree will be changed.
6 Usually code finishes running in 2 minutes and output results with at most 85% accuracy.
  The reason why this algorithm is much faster is because not all data is used to create only one decision
  tree, meanwhile a forest can provide accurate results due to probability theory.
