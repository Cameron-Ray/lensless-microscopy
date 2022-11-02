import os
import holopy as hp
import numpy as np
from holopy.core.io import load_image, get_example_data_path, save_image
from holopy.core.io.vis import save_plot
from holopy.propagation import ps_propagate
from scipy.ndimage import center_of_mass
from trollimage.xrimage import XRImage

# imagepath = '/home/pi/microscope/backgrounds/test.jpg'
# bgpath = '/home/pi/microscope/backgrounds/test.jpg'
# L = 0.053 # distance from light source to screen/camera
# cam_spacing = 155e-8 # linear size of camera pixels
# mag = 1 # magnification
# npix_out = 1020 # linear size of output image (pixels)
# zstack = np.arange(1.08e-3, 1.18e-3, 0.01e-3) # distances from camera to reconstruct
# print(cam_spacing)

# holo = hp.load_image(imagepath, spacing=cam_spacing, illum_wavelen=660e-9, medium_index=1) # load hologram
# bg = hp.load_image(bgpath, spacing=cam_spacing) # load background image
# holo = hp.core.process.bg_correct(holo, bg+1, bg) # subtract background (not divide)
# beam_c = center_of_mass(bg.values.squeeze()) # get beam center
# out_schema = hp.core.detector_grid(shape=npix_out, spacing=cam_spacing/mag) # set output shape

# recons = ps_propagate(holo, zstack, L, beam_c, out_schema) # do propagation
# # print(abs(recons[:,350:550,450:650]))
# save_plot("test.jpg", abs(recons[1,350:550,450:650])) # display result

imagepath = '/home/pi/microscope/backgrounds/test.jpg'
bgpath = '/home/pi/microscope/backgrounds/test.jpg'


L = 0.0407 # distance from light source to screen/camera
cam_spacing = 12e-6 # linear size of camera pixels
mag = 1 # magnification
npix_out = 480 # linear size of output image (pixels)
# zstack = np.arange(1.08e-3, 1.18e-3, 0.01e-3) # distances from camera to reconstruct
zstack = 1

holo = hp.load_image(imagepath, spacing=cam_spacing, illum_wavelen=660e-9, medium_index=1.53) # load hologram
bg = hp.load_image(bgpath, spacing=cam_spacing) # load background image
holo = hp.core.process.bg_correct(holo, bg+1, bg) # subtract background (not divide)
beam_c = center_of_mass(bg.values.squeeze()) # get beam center
out_schema = hp.core.detector_grid(shape=npix_out, spacing=cam_spacing/mag) # set output shape

recons = ps_propagate(holo, zstack, L, beam_c, out_schema) # do propagation

for i in range(len(abs(recons[:,1,1]))):
    im_to_save = XRImage(abs(recons[i,:,:]))
    im_to_save.pil_save("output" + str(i) + ".jpg")
    # save_image("output" + str(i) + ".tiff", abs(recons[i,:,:])) # display result
