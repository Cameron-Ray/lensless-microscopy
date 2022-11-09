# In Vivo Lensless Microscopy Using A Raspberry Pi Camera
<p float="left">
  <img src="https://user-images.githubusercontent.com/52524662/200952921-864608d9-aea7-4803-a1cd-15b35a710e47.jpg" width="200"/>
<img src="https://user-images.githubusercontent.com/52524662/200953348-34899cbc-04da-44a0-9559-0e23545206c6.jpg" width="200"/>
<img src="https://user-images.githubusercontent.com/52524662/200953469-280f52cf-3230-4542-96a1-0d1e2e65fc71.jpg" width="200"/>
</p>

## Introduction
This project was completed in the Department of Electrical Engineering at the Univeristy of Cape Town. It was in fulfilment of the degree requirements for BSc Engineering in Mechatronics. This project was supervised by Robyn Verrinder and Dr Mandy Mason.

## Abstract
This thesis investigates the application of lensless microscopy in the field of Mycobacterium tuberculosis drug research. The design of a lensless microscope and supporting hardware was carried out to yield a real-time system for bacterial colony counting and growth rate estimation. The aim of this research was to determine the feasibility of implementing the Sony IMX477 CMOS Image sensor in a lensless microscope configuration. It is assumed that this camera will be more than suitable for this application. This is due to the large FOV and image sensor area. The image sensor was used on the Raspberry Pi High-Quality camera PCB which was connected to a Raspberry Pi 4B for image processing. The Raspberry Pi is also used for interacting with a real-time sample analysis interface. The tools and interfaces were developed using Python and HTML. They are interacted with via a web portal hosted on a Flask server. Backend image processing and computer vision analysis are accomplished by real-time software which implements the HoloPy and OpenCV libraries. It was found after implementing the Raspberry Pi Camera that it is suitable for the application of lensless microscopy. The project was successful overall although minor issues in some subsystems were discovered. This includes the limitations on image reconstruction and the bacteria samples that did not grow within a 24-hour window.

## Report
The report can be found in the root directory of this repository in PDF form.

## Lab Experimentation Image Data
[All Capture Data](https://1drv.ms/u/s!AvPr7PbTZOiUkZAjZgt6-7enE5af2Q?e=uVQeI5)<br>
[First Capture Series](https://1drv.ms/u/s!AvPr7PbTZOiUkZApX0L194BrCGZNiw?e=cQrOnH)<br>
[Second Capture Series](https://1drv.ms/u/s!AvPr7PbTZOiUkZA71zhlhoJr1oHiBg?e=dE6kKt)<br>
[Third Capture Series](https://1drv.ms/u/s!AvPr7PbTZOiUkZBH5JTckxgGo-KhkQ?e=FdoEJh)<br>
[Test Target Captures](https://1drv.ms/u/s!AvPr7PbTZOiUkZBR2AZ5EscuIyGp5A?e=yZcEWd)

## Fusion 360 Models
[Microscope Pi Housing](https://a360.co/3he9QzM)<br>
[Microscope Slide Mount](https://a360.co/3t3Jfbi)

## 3D Printing Assets
All 3D printing assets can be found in this repository under the ```microscope-camera-mount``` folder.
