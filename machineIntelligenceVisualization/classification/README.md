# MIVision - Classification Visualization

## MIVision ToolKit

AMD MIVision is a comprehensive set of help tools for neural net creation, development, training and deployment. The ToolKit provides you with help tools to design, develop, quantize, prune, retrain, and infer your neural network work in any framework. The ToolKit is designed help you deploy your work to any AMD or 3rd party hardware, from embedded to servers.

MIVision ToolKit provides you with tools for accomplishing your tasks throughout the whole neural net life-cycle, from creating a model to deploying them for your target platforms.

## Usage
* Script
````
python machineIntelligenceVisualization/classification/generate-visualization.py
````
* Inputs
````
-i [input Result CSV File - required]
-d [input Image Directory - required]
-l [input Label File - required]
-h [input Hierarchy File - optional]
-o [output Directory - required]
-f [output file name - required]
-m [neural net model name - optional]
````

## List of Features Available in this release

* Overall Summary
* Graphs
* Hierarchy
* Labels
* Image Results
* Compare
* Help

### Overall Summary

This section summarizes the results for the current session, with information on the dataset and the model. The section classifies the dataset into images with or without ground truth and only considers the images with ground truth for analysis to avoid skewing the results.

The summary calculates all the metrics to evaluate the current run session, helps evaluate the quality of the data set, accuracy of the current version of the model and links all the high level result to individual images to help the user to quickly analyze and detect if there are any problems.

The summary also timestamps the results to avoid confusion with different iterations.

### Graphs

The graph section allows the user to visualize the dataset and model accurately. The graphs can help detect any anomalies with the data or the model from a higher level. The graphs can be saved or shared with others.
Hierarchy

This section has AMD proprietary hierarchical result analysis. Please contact us to get more information.

### Labels

Label section is the summary of all the classes the model has been trained to detect. The Label Summary presents the highlights of all the classes of images available in the database. The summary reports if the classes are found or not found.

Click on any of the label description and zoom into all the images from that class in the database.

### Image Results

The Image results has all the low level information about each of the individual images in the database. It reports on the results obtained for the image in the session and allows quick view of the image.
Compare

This section compares the results of a database or the model between different sessions. If the database was tested with different models, this section reports and compares results among them.
