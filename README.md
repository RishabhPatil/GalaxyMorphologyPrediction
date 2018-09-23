# GalaxyMorphologyPrediction

Final year (Senior year) project during my undergraduate degree<br />
Classification of galaxies into 37 classes for  using.

Inspired by this paper: https://arxiv.org/abs/1503.07077<br />
Kaggle Competition: https://www.kaggle.com/c/galaxy-zoo-the-galaxy-challenge

## Rotation
The orientation of the galaxy in a image should not affect the classification. Same image is rotated to generate multiple times to eleminated the bias caused by its rotational orientation.

## Old Localization 
Majority of pixels in every image are dark, add no value to the features, we can localize the object in each image to increase the information/pixels ratio.<br />
![Galaxy Localization](https://media.giphy.com/media/cJ5t5JToCnpRftBbdq/giphy.gif)
