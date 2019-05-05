## 1.  What image classifier technology you used for your projects?

  We are currently using the idealo image quality assessment neural network to do our image rating. We first found this repository from one the the weblinks that Professor Goggins provided at the begining of the semester to a medium.com article that described how they used this system to rate hotel images. This system is built using a convolutional neural network.
  
  Article:
  
  https://medium.com/idealo-tech-blog/using-deep-learning-to-automatically-rank-millions-of-hotel-images-c7e2d2e5cae2
  
  Source Repository:
  
  https://github.com/idealo/image-quality-assessment
  


## 2.  Whether or not you have started to build classifiers off of the pictures from Ed McCain or if you are still using the default example classifiers. Explain the advantages and limitations of your choice.

  We are currently using the default example classifier from the image-quality-assessment repository for our image rating needs. We are continuing to utilize this system, because we lack the time and experience necessary to build our own funcitoning neural network before the end of the semester. This system, while reliable has proven to be very inflexible. We can get a rating for every picture; however, the ratings are not varied and stay within a range of 4-7. We suspect this is because the network has not been trained on enough varied data. After doing more research, we found that the dataset that the model was trained on did not include almost and humans. This poses a great barrier for us.
