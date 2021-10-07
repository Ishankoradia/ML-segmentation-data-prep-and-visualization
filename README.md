## Objective
For any Machine learning task, the most important step is to prepare data i.e. train and test directories for the model to train and validate on. This repo exactly does this
for the Oxford-IIIT Pet Dataset (famous cats-dogs dataset) that can be downloaded here https://www.robots.ox.ac.uk/~vgg/data/pets/

## Learning  
My aim behind working this out was to understand the Image Segmentation task and the complexty behind it. And also practise to write a clean and concise code that is easier to debug.

## Challenges
The main challenge I faced was when I was translating the visualization code in julia. It was a little tricky to draw segmentation annotations on the image, it was not as straight forward as it was in python.

## Languages used
- Python 3.8
- Julia 1.6

## How to use
### Segmentation
To directly create train and test directories from command line you can use the command :<br />
`python3 segmentation.py train_fraction path_to_images_folder path_to_annotations_folder seed` or as an example <br />
`python3 segmentation.py 0.6 "images/" "annotations/" 123`


The command above creates directories for cats and dogs with the same fraction (0.6). If there is a need for different train fraction for different species you can open a python IDE and import the segmentation module to use its functions <br />
`>>from segmentation import generate_train_test, generate_train_test_species` <br />
`>>generate_train_test_species(species="cat", train_fraction=0.6, path_to_images_folder="images/", path_to_annotations_folder="annotations/")` <br />
you can also call the common function for the species in this way <br />
`>>generate_train_test(train_fraction=0.6, path_to_images_folder="images/", path_to_annotations_folder="annotations/")` <br />

### Visualization
To see how the segment is drawn I have used interact (python) and manipulate (julia) for better user experience. For these you will need Jupyter or any other IDE that supports these modules. This part is tested on Jupyter. You just need to run the notebooks once you have the kernel setup for python/julia.



