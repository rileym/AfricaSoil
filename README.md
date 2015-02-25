#AfricaSoil


These files make up a most of my work for the Kaggle's [Africa Soil Property Prediction Contest](https://www.kaggle.com/c/afsis-soil-properties). I didn't write the files with their presentation in mind, so they may seem messy to an outside mind. I ended up [placing tenth](https://www.kaggle.com/c/afsis-soil-properties/leaderboard) of of about one thousand competitors.

-note structure of repository
-soilClean
-soilTune
-Final state of notebooks, some I would use as templates to experiment, so no an exhaustive record of what I did

####Overview of competition:

 The goal of the competition was to predict the level soil sample's  of five different soil characteristics using the infrared spectroscopy measurements. In simplified terms, the competition is five separate (or at least I chose too treat each response separately) regression problems.
	
####Observations about the dataset:

 *The data is high dimensional
 *It is split between spectral data and background data (about location, soil depth, etc.)
 *The spectral data is functional data, and so lots of autocorrelation

####What I tried:

#####Preprocessing:

*Standardization of the input
*Correlation filtering on the input (at different levels, in combination with standardization)
*A home-brew filter/dim-reduction scheme that tried to find representative (by local auto-correlation) frequencies 
*Transformations of the response 
*log (w/ small translation because of negative values)
*[inverse hyperbolic sine](http://mathworld.wolfram.com/InverseHyperbolicSine.html)
			
*Models/Function Classes:
 *Linear:
  *Lasso
  *Ridge
  *Elastic Net
  *Supervised Principle Components
  *Fussed Lasso
		
*Non-linear:
 *SVM (Regression, with kernels)
 *GBM
 *kNN (After dim-reduction)
			
*Post-processing:
 *Before scoring
  *Inverse transformations of the response (if transformed originally)
  *Truncation at max or min values
 *After scoring
  *Model averaging (didn't get to a full meta model)


####What worked:

As one would expect, different approaches and models worked to different effect on the different response variables. In the end ridge regression and support vector regression performed best.

*Ridge regression was relatively successful in predicting all the response variables; ridge regression models with various preprocessing and post processing procedures were weighted into the final predictions for every response variable. For a few (not all) of the response variables, correlation filtering in combination with ridge regression significantly improved the generalization error. The degree of that improvement was sensitive to the level of filtering, so I tuned the level where appropriate. 
*Support vector regression models with various kernels were successful with some but not all of the response variables.
*Certain response benefitted from log transformations or inverse hyperbolic sine (and their corresponding inverse transformation before scoring in the CV)
*A couple of the response variables seemed to have a natural minimum value, and performance improved when I truncated the predictions at that natural minimum. I only thought of this at the last minute, so while I truncated the relevant predictions and saw improvement, ideally I would have incorporated the truncation into the CV process, since 

spefici for p, 
-depended on the response variable
	-correlation filtering worked
	-truncatoin works
-trusting internal CV, not overfitting to leaderboard
-fitting to the leaderboard
-P, thinking carefully about the CV scores when there'€™s rare but powerful outliers.
