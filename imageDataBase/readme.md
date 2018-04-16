# Steps to Resize and extract tags from any image data base

## Dependencies

### Linux
- python
- pil
- exiftool
````
sudo apt install libimage-exiftool-perl
sudo apt-get install python-pip
sudo apt-get install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev
sudo pip install pil
````
Fix all file names in the inpt image folder by running the following command inside the image folder

````
ls | cat -n | while read n f; do mv "$f" "file-$n.jpg"; done
````
### Windows
- python
- pil
- exiftool
- qawk

## Step 1

run step-1.py to resize and rename your image to the required width and height, also allows padding to keep the image resolution
````
python step-1.py 	-d [input image directory] --- required 
			-o [output image directory] --- required (valid dir)
			-f [new image file name] --- required 
			-w [resize width] --- optional
			-h [resize height] --- optional
			-p [padding value] --- optional
````

this script will resize and rename all your images and put them in the output folder you created.


## Step 2

run step-2.py to extract all the tags and output a text file with image name and all the tags associated with the image
````
python step-2.py    -d [input image directory] --- required 
                    -f [tag_file_name.txt] --- required 
````
this script will output a CSV format image name & tags. The output file will be CSV_tag_file_name.txt

	output example --	imagename.JPEG, tench, Tinca tinca	(fileName.JPEG,tags)


## Step 3

run step-3.py to create a usable image validation .txt with image name and class number
````
python step-3.py -l [label.txt with 1000 labels without synset numbers] --- required (script-labels.txt from this project)
                 -t [CSV_tag_file_name.txt] --- required (output from step 2)
````
this script will generate an annie inference app usable data on the cmd/terminal use  >> to val.txt for output

	output example --	imagename.JPEG 0	(fileName.JPEG Label)
