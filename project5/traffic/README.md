For this project, I experimented with different neural network architectures to find a balance between accuracy and training time. My first attempt used only one convolutional layer followed by a pooling layer and a dense output layer. While the model was able to learn some patterns, the accuracy was not very high and the results were inconsistent across different runs.

To improve the model, I added a second convolutional layer with more filters. This helped the network learn more detailed features from the traffic sign images and noticeably improved the accuracy. I also added a hidden dense layer with 128 neurons to allow the model to learn more complex relationships between extracted features.

During testing, I noticed that the model could easily overfit the training data. To reduce overfitting, I added a Dropout layer with a rate of 0.5 before the output layer. After adding dropout, the model generalized better and achieved better performance on the testing data.

I also tried a few different layer combinations. Simpler models trained quickly but produced lower accuracy, while larger models increased training time without providing a significant improvement in results. The final architecture provided a good balance between performance and efficiency.

The final model consists of two convolutional layers, two max-pooling layers, one dense hidden layer, a dropout layer, and a softmax output layer with 43 units. This architecture achieved approximately 96% test accuracy while maintaining relatively fast training times. Overall, adding the second convolutional layer and the dropout layer had the biggest positive impact on performance.
