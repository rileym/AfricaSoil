# Soil Property Prediction

This repository archives of my work for the Kaggle's [Africa Soil Property Prediction Contest](https://www.kaggle.com/c/afsis-soil-properties). The files are in more or less the same state as they were the day the competition ended. I [placed tenth](https://www.kaggle.com/c/afsis-soil-properties/leaderboard). 

***You can view any IPython notebook file ***(`.ipynb`)***) through [nbviewer](http://nbviewer.ipython.org/github/rileym/AfricaSoil/tree/master/).***

####Overview of Competition

 The goal of the competition was to predict five (real-valued) characteristics of a soil sample from that sample's IR spectroscopy measurements and a small number other features.  It is simplest to think of the competition as five separate (or at least I chose too treat each response separately) regression problems.
	
####The Predictor Variables

 * The features are split between spectral data (the large majority of the features) and background data, which record the soil’s location, depth, etc.
 * The spectral data is high dimensional
 * The spectral data is functional data, and therefore there's lots of autocorrelation

####What I Tried

#####Preprocessing

* Standardization of the input
* Correlation filtering of the input
* A home-brew filter/dim-reduction scheme that tried to find representative (by local auto-correlation) frequencies 
* Transformations of the response 
 * Log 
 * [Inverse hyperbolic sine](http://mathworld.wolfram.com/InverseHyperbolicSine.html)
			
#####Models/Function Classes

 * Linear:
  * Lasso
  * Ridge
  * Elastic-Net
  * Supervised Principle Components
  * Fussed Lasso -- I had high hopes for this one! :'-(
		
* Non-linear:
 * SVR (with various kernels)
 * GBM
 * kNN (only after dim-reduction)
			
#####Post-processing
 * Before scoring
  * Inverse transformations of the response (if transformed originally)
  * Truncation at max or min values
 * After scoring
  * Model averaging (I did not get a change to could build a proper meta-model)


####What Worked & General Observations

As one would expect, different combinations of approaches worked to different effect on the different response variables. In the end ridge regression and support vector regression performed best.

* Ridge regression was relatively successful in predicting all the response variables; ridge regression models with various preprocessing and post processing procedures were weighted into the final predictions for every response variable. For a few (not all) of the response variables, correlation filtering in combination with ridge regression significantly improved the generalization error. The degree of that improvement was sensitive to the level of filtering, and I tuned that level where appropriate. 
* Support vector regression models with various kernels were relatively successful in predicting some but not all of the response variables.
* Certain response variables benefitted from log transformations or inverse hyperbolic sine transformations (and, in turn, the their associated inverse transformations *before* scoring)
* A couple of the response variables seemed to have a natural minimum value, and performance improved when I truncated the predictions at that natural minimum. I only thought of this at the last minute, so while I truncated the relevant predictions and saw improvement, ideally I would have incorporated the truncation into the CV process, since the optimal model parameters might well be different truncation is included in the fitting procedure.
* The `P` response variable was by far the hardest to predict. I imagine that the final rankings in the competition closely track the degree to which a contestant managed to predict `P`. The distribution of the `P` values is very skewed, with most values clustered near a minimum value, while a smaller number of samples reach values orders of magnitude larger. So the challenge was to predict these outliers, or at least minimize the outliers’ havoc.
* Probably *because* of `P`'s long tail and unpredictability it was particularly important to ignore the public leaderboard and trust the internal CV scores. Kaggle’s public leaderboards are calculated on a small part of the hold-out set, in this case about a tenth the size of both the training data and the hold-out set. Thus a good or bad score on the public leaderboard was overly sensitive to a few outliers.