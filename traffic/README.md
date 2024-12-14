

I used the code in handwriting.py as the framework and adjusted the parameters as below -


1. Set IMG_WIDTH and IMG_HEIGHT to 32 x 32, since the average picture size is around 50 x 50. 32 is a close number that happens to be the power of 2. Also tried 64 x 64 but it didn't work well. I learned that it's better to shrink than expand images so that there isn't new redundant information created

2. The model accuracy is now 5%, which suggests that the pictures were not read correctly. I used interpolation = cv2.INTER_AREA instead of the default INTER_LINEAR for cv2.resize, then the accuracy increased to 20%. I learned that INTER_AREA is the right parameter for image shrinking/decimentation

3. Changed dropped-out rate to 0.3 from 0.5 and reached accuracy of 30%, also experimented with other numbers and found 0.3 to be the proper amount that doesn't cause significant over/underfitting

4. Realized that the images are quite blurry, so set the kernel of filter to 5 x 5 instead of 3 x 3 to capture the features with large frames, the training accuracies attained 88%, also tried 7x7 but the accuracy reduced to 5%

5. Tried increasing filter to 64 from 32, but the accuracy dropped a bit

6. Normalizing pixel values to 0-1 since the original value range is too wide, then accuracy increased to 92%-93%

7. Changed activation function from relu to swish, little difference is made to the accuracy, but I still proceeded with swish since research suggests that it often performs better than relu

8. Applied batch normalization, then accuracy increased to 97%

9. Added another convolutional layer with the same parameters as well as another max pooling layer, then accuracy increased to 98%

10. Tried adjusting the parameters of the second convolution layer, like changing filter to 64 and kernel to 3 x 3 in order to detect more minuscule edges, but no material difference is seen, so I changed them back to the same parameters

11. Added another hidden layer, no difference is made so reverted the adjustment

12. Added another dropout layer, then the accuracy dropped to 98%, suggesting that the model is not sufficiently trained, so I reverted it

13. Increased the number of nodes in the hidden layer from 128 to 256 in order to improve accuracy. Then the training accuracy improved a little bit but test accuracy dropped to 97%, which suggests overfitting, so I reverted the change

14. Increase pool size of the second maxpooling layer from 2x2 to 3x3 in order to attain more regulization effect. This reduced the training accuracy in the first a few epochs, but the testing accuracy is not affected much. I choose to use this since this reduces the risk of overfitting as well as saving computing time and power

Now the test accuracy is between 98.5%-99%. I tried changing some parameters here and there but no material difference is seen.