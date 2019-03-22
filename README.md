# ObjectBoundingBoxDetection

This project was part of Flipkart Grid Challenge : Bounding Box Detection

Given the image training dataset with coordinates of bounding box annotated, model is trained to output bounding box on new images.

Tools and Frameworks used :
Keras

Libraries used:
pandas
numpy
cv2

Approach:
Stacked multiple convolutional layers to extract features , flattened it and passed it through
a dense layer to get 4 unit output vector

Future Target:
Change evaluation metrics to incorporate accuracy with respect to iou calculations.
