import pandas as pd
import numpy as np
import os
import shutil
import csv
import sys

dog_breeds = [
    'American Bulldog', 'American Pit Bull Terrier', 'Basset Hound', 'Beagle', 'Boxer', 'Chihuahua', 'English Cocker Spaniel',
    'English Setter', 'German Shorthaired', 'Great Pyrenees', 'Havanese', 'Japanese Chin', 'Keeshond', 'Leonberger',
    'Miniature Pinscher', 'Newfoundland', 'Pomeranian', 'Pug', 'Saint Bernard', 'Samoyed', 'Scottish Terrier',
    'Shiba Inu', 'Staffordshire Bull Terrier', 'Wheaten Terrier', 'Yorkshire Terrier'
]
    
cat_breeds = ['Abyssinian', 'Bengal', 'Birman', 'Bombay', 'British Shorthair', 'Egyptian Mau', 'Maine Coon', 'Persian',
    'Ragdoll', 'Russian Blue', 'Siamese', 'Sphynx'
]

###### create dataframes for cats and dogs with the info from list.txt
def get_species_dataframe(species, path_to_list_file, path_to_images_folder):
    i = 0
    cols = ['image', 'species', 'breed_id']
    cats_or_dogs = pd.DataFrame(columns=cols)
    species_idx = 1 if species == "cat" else 2
    with open(path_to_list_file) as f:
        for i in range(6):
            f, next(f)
        for line in f:
            temp_data = line.replace('\n','').split()
            img_file = path_to_images_folder + temp_data[0] + '.jpg' #image path
            species = temp_data[2] #cat or dog ; 1 or 2
            breed_id = temp_data[3]
            row_series = pd.Series([img_file, species, breed_id], index=cols)
            if int(species) == species_idx: #cat
                cats_or_dogs = cats_or_dogs.append(row_series, ignore_index=True)
    return cats_or_dogs

###### split the species into train and test sets
def get_train_test_species_dfs(species, train_fraction, path_to_list_file, path_to_images_folder, seed):
    species_df = get_species_dataframe(species, path_to_list_file, path_to_images_folder)
    idx = list(species_df.index)
    np.random.seed(seed)
    shuffle_idx = [idx[i] for i in np.random.permutation(len(species_df))]
    n_split = int(len(species_df) * train_fraction)
    train_df = species_df.iloc[shuffle_idx[0:n_split], :]
    test_df = species_df.iloc[shuffle_idx[n_split:], :]
    return train_df, test_df

###### copy and rename file to create the directories
def create_X_Y_dir(species_df, which, species, path_to_annotations_folder):
    species_df.reset_index(inplace=True, drop=True)
    
    # new directory
    new_img_dir = 'segment_data/' + species + '/X_' + which + '/'
    isExist = os.path.exists(new_img_dir)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(new_img_dir)
    else:
        # if a diretory exists empty it since we cannot have files with same name
        shutil.rmtree(new_img_dir)
        os.makedirs(new_img_dir)
        
    # generate label
    generate_labels_file(new_img_dir + "X_" + which + ".txt", species_df)
        
    # new segment directory
    new_segment_img_dir = 'segment_data/' + species + '/Y_' + which + '_segment/'
    isExist = os.path.exists(new_segment_img_dir)
    if not isExist: 
        # Create a new directory because it does not exist 
        os.makedirs(new_segment_img_dir)
    else:
        # if a diretory exists empty it since we can have files with same name
        shutil.rmtree(new_segment_img_dir)
        os.makedirs(new_segment_img_dir)
    
    for i in species_df.index:
        #copy the file
        img_dir = species_df.iloc[i]['image']        
        shutil.copy(img_dir, new_img_dir)

        #rename the file
        dst_file_name = os.path.join(new_img_dir, img_dir.split('/')[1]) 
        new_dst_file_name = os.path.join(new_img_dir,  which + '_' + species + '_' + str(i+1) + '.jpg')
        os.rename(dst_file_name, new_dst_file_name)

        #store corresponding image for Y_segment
        img_name = img_dir.split('/')[1]
        segment_img = img_name.split('.')[0]+'.png'
        segment_img_dir = os.path.join(path_to_annotations_folder + 'trimaps/', segment_img)        
        shutil.copy(segment_img_dir, new_segment_img_dir)

        #rename image for Y segment
        dst_seg_file_name = os.path.join(new_segment_img_dir, segment_img)
        new_seg_dst_file_name = os.path.join(new_segment_img_dir, which + '_' + species + '_segment_'  + str(i+1) + '.png') 
        os.rename(dst_seg_file_name, new_seg_dst_file_name)
        
###### generate labels.txt file that contains the breed of the example
def generate_labels_file(label_dir, species_df):
    with open(label_dir, 'w+', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['#', 'Breed'])
        for i in species_df.index:
            breed_id = species_df.iloc[i]['breed_id']
            breed = dog_breeds[int(breed_id) - 1]
            writer.writerow([i+1, breed])
        
###### make train and test directories and store the images with proper naming convention
def generate_train_test_species(species, train_fraction=0.6, path_to_images_folder="images/", path_to_annotations_folder="annotations/", seed=1):
    path_to_list_file = path_to_annotations_folder + "list.txt"
    train_df, test_df = get_train_test_species_dfs(species, train_fraction, path_to_list_file, path_to_images_folder, seed)
    create_X_Y_dir(train_df, "train", species, path_to_annotations_folder)
    create_X_Y_dir(test_df, "test", species, path_to_annotations_folder)
    
    
###### generate directories for both cats and dogs having common train fraction
def generate_train_test(train_fraction=0.6, path_to_images_folder="images/", path_to_annotations_folder="annotations/", seed=1):
    for spe in ["cat", "dog"]:
        generate_train_test_species(spe, train_fraction, path_to_images_folder, path_to_annotations_folder, seed)

###### if the script is called from command line
if __name__ == '__main__':
    try:
        train_fraction = sys.argv[1]
        path_to_images_folder = sys.argv[2]
        path_to_annotations_folder = sys.argv[3]
        seed = sys.argv[4]
        generate_train_test(train_fraction=0.6, path_to_images_folder="images/", path_to_annotations_folder="annotations/", seed=1)
        print("Directories created successfully")
    except:
        print("Please check if the arguments are consistent")