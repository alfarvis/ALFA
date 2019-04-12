# 
<img src="https://github.com/alfarvis/ALFA/blob/master/ALFA.png" width="300"/>
Alfa is a natural language interpreter for Artificial Intelligence.
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

# Stuff you might be looking for

   * [Installing ALFA](#H1)
   * [Run ALFA](#H2)
   * [Tutorials](#H3)
   * [Example Notebooks](#H4)

<h1 id="H1"> Installation </h1>
Step 1: Install anaconda [distribution](https://www.anaconda.com/enterprise/?gclid=Cj0KCQjwlv_XBRDrARIsAH-iRJRs4Z2f4a9RqhkFkI3xryMwrPEOknxk3OOhNbrk9GqYmaj00kL3XUMaAik1EALw_wcB).

Step 2: Download [ALFA](https://github.com/alfarvis/ALFA/archive/master.zip).

Alternatively, you can also clone the git [repository](https://github.com/alfarvis/ALFA)

Step 3: Unzip ALFA 

### Windows
Step 4: Open Anaconda Prompt from Start Menu

Step 5: Navigate to the directory where ALFA was downloaded 

	cd [path where ALFA was unzipped]

Step 6: Type the following command

	conda env create -f environment.yaml
	
Once all the packages are installed, you can close the window. 

### Linux/macOS
Step 4: Open terminal 

Step 5: Type the following command

	conda env create -f environment.yaml
	
<h1 id="H2"> Running ALFA </h1>

Navigate to the directory where ALFA was downloaded

### Windows

Double click on the file named ALFA_WIN

### Linux/macOS

Open terminal and type the following commands

	conda activate Alfarvis
	python ./qt_run.py

<h1 id="H3"> Tutorials </h1>
To learn more about ALFA, visit our [wiki](https://github.com/Alfarvis/ALFA/wiki)

<h1 id="H4"> Notebooks </h1>
Checkout some of the ALFA [notebooks](https://github.com/Alfarvis/ALFA/wiki/notebooks) demonstrating codes written in ALFA for analyzing different datasets.
