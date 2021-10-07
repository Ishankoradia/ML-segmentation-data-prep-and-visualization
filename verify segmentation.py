import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from segmentation import generate_train_test, generate_train_test_species
import os
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets


def count_imgs(img_dir):
    return (len([name for name in os.listdir(img_dir)]) - 1)

def generate_img_paths(species, which, path_to_segment_data):
    PATH_X = os.path.join(path_to_segment_data, species+"/", "X_"+which+"/")
    PATH_Y = os.path.join(path_to_segment_data, species+"/", "Y_"+which+"_segment/")
    return PATH_X, PATH_Y

def draw_segmentation(img_x, img_y, t):
    img_x = cv2.imread(img_x)
    img_y = cv2.imread(img_y)
    img_x[np.where((img_y[:, :, 0] == 3) & (img_y[:, :, 1] == 3) & (img_y[:, :, 2] == 3))] = (255, 0, 0)
    plt.axis('off')
    plt.title(t)
    plt.imshow(img_x)   

def plt_species_imgs(species, which, path_to_segment_data="segment_data/"):
    PATH_X, PATH_Y = generate_img_paths(species, which, path_to_segment_data)
    no_of_imgs = count_imgs(PATH_X)
    def interact_with_imgs(i, PATH_X=fixed(PATH_X), PATH_Y=fixed(PATH_Y), species=fixed(species), which=fixed(which)):
        img_x = PATH_X + which + '_' + species + '_'+ str(i) + '.jpg'
        img_y = PATH_Y + which + '_' + species + '_segment_' + str(i) + '.png'
        title = which + '_' + species + '_'+ str(i)
        draw_segmentation(img_x, img_y, title)
    interact(interact_with_imgs, i=(1, no_of_imgs, 100))

def main():
    interact(plt_species_imgs, species=["cat", "dog"], which=["train", "test"])

main()


############################ julia
# using Images
# using Plots
# using Random: randperm
# using Random
# using Interact


# function count_imgs(img_dir)
#     return (length([name for name in readdir(img_dir)]) - 1)
# end

# function generate_img_paths(species::String, which, path_to_segment_data)
#     PATH_X = joinpath(path_to_segment_data, species * "/", "X_" * which * "/")
#     PATH_Y = joinpath(path_to_segment_data, species * "/", "Y_" * which * "_segment/")
#     return PATH_X, PATH_Y 
# end

# function draw_segmentation(img_x, img_y, t)
#     img_x = load(img_x)
#     img_y = load(img_y)
#     img_y_vec = vec(reinterpret(UInt8, img_y))
#     h, w = size(img_y, 1), size(img_y, 2)
#     x_vec_coor = Vector{Int64}() 
#     x_coor = Vector{Int64}()
#     y_coor = Vector{Int64}() 
    
#     for ii in 1:size(img_y_vec, 1)
#         if img_y_vec[ii, 1] == 3
#             append!(x_vec_coor, ii)
#         end
#     end

#     for k in x_vec_coor
#         if k % h == 0 # the index is divisble by row count
#             row = h
#             col = Int(k / h)
#         else
#             row = Int(k % h)
#             col = Int(floor(k / h)) + 1
#         end
#         img_x[row, col, :] .= RGB(1.0, 0.0, 0.0)
#     end
#     plot(img_x, title = t, axis=false, ticks=false)    
# end

# function plt_species_imgs(species::String, which::String, path_to_segment_data::String)
#     PATH_X, PATH_Y = generate_img_paths(species, which, path_to_segment_data)
#     no_of_imgs = count_imgs(PATH_X)
#     @manipulate for i in 1:100:no_of_imgs
#         img_x = PATH_X * which * '_' * species * "_" * string(i) * ".jpg"
#         img_y = PATH_Y * which * "_" * species * "_segment_" * string(i) * ".png"
#         title = which * "_" * species * "_" * string(i)
#         draw_segmentation(img_x, img_y, title)
#     end
# end

# function main()
#     @manipulate for species in ["cat", "dog"]
#         @manipulate for which in ["train", "test"]
#             plt_species_imgs(species, which, "segment_data/")
#         end
#     end
# end