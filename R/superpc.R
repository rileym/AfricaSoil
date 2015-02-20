##
## Supervised Priciple Components
##

library("superpc")
source(file = './helpers.R')

##
## Load Data, Clean, & Split
##

setwd('/Users/rileymatthews/Projects/Africa Soil')
full.df <- read.csv(file = './Data/training.csv', header = TRUE, row.names = 'PIDN')
full.test.df <- read.csv(file = './Data/sorted_test.csv', header = TRUE, row.names = 'PIDN')

N <- dim(full.df)[1]
train.prop <- .9
train.idx <- sample(x = 1:N, size = N*train.prop, replace = FALSE)

train.dfs <- soil.clean(df = full.df[train.idx,], targets = TRUE)
val.dfs <- soil.clean(df = full.df[-train.idx,], targets = TRUE)

test.dfs <- soil.clean(df = full.test.df, targets = FALSE)

##
## Approximate Optimal Parameters (numer of components, threshold)
## 

# (A little awkward because superpc isn't very customizable and the documentation is unclear and incomplete)

opt.thresh <- list()
opt.n.components <- list()
best.rmse <- list()

thresh.mult <- 1.03 #Don't make this too large
n.thresh.scope <- 2
max.components = 3

targets <- colnames(train.dfs$targets)
par(mfrow=c(ceiling(length(targets)/3),3))
for (target in targets){

  data.train.obj <- list(x=t(train.dfs$wave),y=train.dfs$targets[[target]]) 
  fit <- superpc.train(data = data.train.obj, type = 'regression')
  print(paste('Beginning', target, 'superpc.cv...')) ########## Delete
  cv.obj <- superpc.cv(fit = fit, data = data.train.obj, n.components = max.components) #why not just do val?
  superpc.plotcv(cv.obj, main=target)
  
  # Use hueristic to choose best threshold
  opt.thresh[target] <- cv.obj$thresholds[which.max(cv.obj$scor[1,])]
  print(paste('superpc Threshold: ', opt.thresh[target]))
  # Use validation
  data.val.obj <- list(x=t(val.dfs$wave), y=val.dfs$targets[[target]])
  
  best.thresh <- NA
  best.n.components <- NA
  best.performance <- Inf
  thresholds <- opt.thresh[[target]]*thresh.mult^(-n.thresh.scope:n.thresh.scope)
  for (n.comps in 1:max.components){
    
    for(thresh in thresholds){
    
      pred.obj <- superpc.predict(fit, data.train.obj, data.val.obj, threshold=thresh, 
                                n.components= n.comps, prediction.type="continuous")
      y.predicted <- pred.obj$v.pred.1df
      y.obs <- data.val.obj$y
      cur.rmse <- rmse(y.predicted, y.obs)
      
      if (cur.rmse < best.performance){
        
        best.thresh <- thresh
        best.n.components <- n.comps
        best.performance <- cur.rmse
        
      } 
    }
  }
  
  opt.thresh[target] <- best.thresh
  opt.n.components[target] <- best.n.components
  best.rmse[target] <- best.performance
    
}


##
## Use Best Parameters to Predict Test (could have done this in the above loop, but so cluttered! :-)
##


train.dfs <- soil.clean(df = full.df, targets = TRUE)
test.predictions <- data.frame(row.names = row.names(test.dfs$wave))  

for (target in targets){
  
  data.train.obj <- list(x=t(train.dfs$wave),y=train.dfs$targets[[target]]) 
  data.test.obj <- list(x = t(test.dfs$wave), y = NULL)
  fit <- superpc.train(data = data.train.obj, type = 'regression')
  y.preds <- superpc.predict(fit, data = data.train.obj, newdata = data.test.obj, threshold = opt.thresh[[target]], 
                            n.components = opt.n.components[[target]], prediction.type="continuous")
  test.predictions[[target]] <- y.preds$v.pred.1df
  
}

##
## Record results to disk.
##

# write.csv(test.predictions, file = './Data/Preds/superpc-preds.csv')
# write.csv(data.frame(best.rmse), file = './Data/Preds/superpc-rmse.csv')


