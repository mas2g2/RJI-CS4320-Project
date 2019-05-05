## 1.  What image classifier technology you used for your projects?

  We are currently using the idealo image quality assessment neural network to do our image rating. We first found this repository from one the the weblinks that Professor Goggins provided at the begining of the semester to a medium.com article that described how they used this system to rate hotel images. This system is built using a convolutional neural network.
  
  Article:
  
  https://medium.com/idealo-tech-blog/using-deep-learning-to-automatically-rank-millions-of-hotel-images-c7e2d2e5cae2
  
  Source Repository:
  
  https://github.com/idealo/image-quality-assessment
  


## 2.  Whether or not you have started to build classifiers off of the pictures from Ed McCain or if you are still using the default example classifiers. Explain the advantages and limitations of your choice.

  We are currently using the default example classifier from the image-quality-assessment repository for our image rating needs. We are continuing to utilize this system, because we lack the time and experience necessary to build our own funcitoning neural network before the end of the semester. This system, while reliable has proven to be very inflexible. We can get a rating for every picture; however, the ratings are not varied and stay within a range of 4-7. We suspect this is because the network has not been trained on enough varied data. After doing more research, we found that the dataset that the model was trained on did not include almost and humans. This poses a great barrier for us. We came up with two solutions: retrain the model or implement a weighted function. As a hotfix, we decided to implemenent a function that will take the predicted aesthetic rating and transform it based on the given rating's distance from 5. This gives us a more varied rating scale but does not fully reflect the image aesthetic scoring. The superior solution would be to retrian the model on our images provided by the Missourian. We have researched on how to do this and found that we need to have the images and their respective labeling file. Gathering the images is very straight forward, as we can mass download them from the links provided by Professor Goggins. However, generating the labels for each image has proven very difficult. No instructions are explicitly provided on how to accomplish this besides a link to an academic paper in one of the closed issues on the repository. Up to this point, we have lacked the time and resources to do further research on labeling, but aim to do so for the next sprint.
  
Issue:

https://github.com/idealo/image-quality-assessment/issues/20

Paper:

http://www.ponomarenko.info/papers/tid2013.pdf
