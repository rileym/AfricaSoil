#AfricaSoil


These files make archive most of my work for the Kaggle's [Africa Soil Property Prediction Contest](https://www.kaggle.com/c/afsis-soil-properties). I ended up [placing tenth](https://www.kaggle.com/c/afsis-soil-properties/leaderboard). I didn't write the files with their presentation in mind. To view an IPython notebook (.ipynb), use [nbviewer](http://nbviewer.ipython.org/github/rileym/AfricaSoil/tree/master/). 

####Overview of competition:

 The goal of the competition was to predict the level soil sample's  of five different soil characteristics using the infrared spectroscopy measurements. In simplified terms, the competition is five separate (or at least I chose too treat each response separately) regression problems.
	
####Observations about the dataset:

 * The data is high dimensional
 * It is split between spectral data and background data (about location, soil depth, etc.)
 * The spectral data is functional data, and so lots of autocorrelation

####What I tried:

#####Preprocessing:

* Standardization of the input
* Correlation filtering on the input
* A home-brew filter/dim-reduction scheme that tried to find representative (by local auto-correlation) frequencies 
* Transformations of the response 
 * Log 
 * [Inverse hyperbolic sine](http://mathworld.wolfram.com/InverseHyperbolicSine.html)
			
#####Models/Function Classes:

 * Linear:
  * Lasso
  * Ridge
  * Elastic Net
  * Supervised Principle Components
  * Fussed Lasso
		
* Non-linear:
 * SVM (Regression, with kernels)
 * GBM
 * kNN (After dim-reduction)
			
#####Post-processing:
 * Before scoring
  * Inverse transformations of the response (if transformed originally)
  * Truncation at max or min values
 * After scoring
  * Model averaging (didn't get to a full meta model)


####What worked:

As one would expect, different approaches and models worked to different effect on the different response variables. In the end ridge regression and support vector regression performed best.

* Ridge regression was relatively successful in predicting all the response variables; ridge regression models with various preprocessing and post processing procedures were weighted into the final predictions for every response variable. For a few (not all) of the response variables, correlation filtering in combination with ridge regression significantly improved the generalization error. The degree of that improvement was sensitive to the level of filtering, so I tuned the level where appropriate. 
* Support vector regression models with various kernels were successful with some but not all of the response variables.
* Certain response benefitted from log transformations or inverse hyperbolic sine (and their corresponding inverse transformation before scoring in the CV)
* A couple of the response variables seemed to have a natural minimum value, and performance improved when I truncated the predictions at that natural minimum. I only thought of this at the last minute, so while I truncated the relevant predictions and saw improvement, ideally I would have incorporated the truncation into the CV process, since 
* The `P` response variable was by bar the hardest to predict. I imagine that the final rankings in the competition track how well `P` was predicted. The distribution of the `P` values was very skewed, with most values clustered near a minimum value, and a few samples sprinkled in a couple orders of magnitude larger. So the challenge was to predict this outliers, or at least minimize the loss.
* Probably *because* of `P`'s long tail and unpredictability it was particularly important to ignore the public leaderboard and trust the internal CV scores. The public leaderboard was calculated on a small part of the hold-out set about a tenth the size of the training data. Thus a good or bad score on the public leaderboard was very sensitive to whether one's model missed a very small number of outlying `P` observations that happen to be in that particular subsection of the hold-out set.
