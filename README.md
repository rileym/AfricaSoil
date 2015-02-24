#AfricaSoil


These files make up a most of my work for the Kaggle's [Africa Soil Property Prediction Contest](https://www.kaggle.com/c/afsis-soil-properties). I didn't write the files with their presentation in mind, so they may seem messy to an outside mind. I ended up [placing tenth](https://www.kaggle.com/c/afsis-soil-properties/leaderboard) of of about one thousand competitors.

####Overview of competition:

	The goal of the competition was to predict the level soil sample's  of five different soil characteristics using the infrared spectroscopy measurements. In simplified terms, the competition is five separate (or at least I chose too treat each response separately) regression problems.
	
####Observations about the dataset:

	-The data is high dimensional
	-It is split between spectral data and background data (about location, soil depth, etc.)
	-The spectral data is functional data, and so lots of autocorrelation

####What I tried:

	-Preprocessing:
		-Standardization of the input
		-Correlation filtering on the input (at different levels, in combination with standardization)
		-A home-brew filter/dim-reduction scheme that tried to find representative (by local auto-correlation) frequencies 
		-Transformations of the response 
			-log (w/ small translation because of negative values)
			-inverse hyperbolic tangent
			
	-Models/Function Classes:
		Linear:
			-Lasso
			-Ridge
			-Elastic Net
			-Supervised Principle Components
			-Fussed Lasso
		
		Non-linear:
			-SVM (Regression, with kernels)
			-GBM
			-kNN
			
	-Post-processing:
	
		-Inverse transformations of the response (if transformed originally)
		-Truncation at max or min values
		-Model averaging (didn't get to a full meta model)


What worked:

As one would expect, different approaches and models worked differently wi
-I was excited about the fussed also, but the model is new and the only implementation (in R) I found just could not handle the high dimensionality. 
-depended on the response variable
	-correlation filtering worked
	-truncatoin works
-Really a few need to focus on
-trusting internal CV, not overfitting to leaderboard
-some hard to predict outliers that can skew the model or the score

Lessons Learned


Mention 

-Initial Exploration
-RR
-SVR


-soilTuningTools
-soilCleanTools
-Final state of notebooks, some I would use as templates to experiment, so no an exhaustive record of what I did
-exploration and observations
-fitting to the leaderboard
-P, thinking carefully about the CV scores when there'€™s rare but powerful outliers.
