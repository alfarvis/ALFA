# ALFA
Alfa is a natural language interpreter for Artificial Intelligence  
Alfa allows us to explore big datasets and run complex machine learning algorithms using plain old English !!!

## Here is an example code written in ALFA
	Load training data
	Find the top 10 classification predictors
	Train a SVM model using these top 10 predictors
	Find the best algorithm among SVM, random forest, and decision tree using 10 fold cross validation
	Train the best algorithm on my training dataset

	Load the test dataset
	Run the best algorithm on the test dataset
	Plot the ROC curve and the confusion matrix for the results
	Save  

# Installation
Step 1: Install anaconda [distribution](https://www.anaconda.com/enterprise/?gclid=Cj0KCQjwlv_XBRDrARIsAH-iRJRs4Z2f4a9RqhkFkI3xryMwrPEOknxk3OOhNbrk9GqYmaj00kL3XUMaAik1EALw_wcB).
Step 2: Download [ALFA](https://github.com/alfarvis/ALFA/archive/master.zip) 
You can also clone the git [repository](https://github.com/alfarvis/ALFA)
Step 3: Unzip ALFA 

### Windows
Step 2: Open Anaconda Prompt from Start Menu

Step 3: Navigate to the directory where ALFA was downloaded 

	cd [path where ALFA was unzipped]

Step 4: Type the following command

	conda env create -f environment.yaml
	
Once all the packages are installed, you can close the window. 

### Linux/macOS
Step 2: Open terminal 

Step 3: Type the following command

	conda env create -f environment.yaml
	
# Running ALFA



### Windows

Navigate to the directory where ALFA was downloaded

Double click on the file named ALFA_WIN

### Linx/macOS

Open terminal and type the following commands

	conda activate Alfarvis
	python ./qt_run.py

# Tutorials
To learn more about Alfa, visit our [wiki](https://github.com/Alfarvis/ALFA/wiki)
