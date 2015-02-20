# GBM Regression

library("gbm")
library('caret')
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
## Training Loop
##


train.dfs <- soil.clean(df = full.df, targets = TRUE)
test.predictions <- data.frame(row.names = row.names(test.dfs$wave))  


gbm.objs <- list()
results <- list()
important.vars <- list()
predictions <- data.frame(row.names = row.names(test.dfs$wave))
targets <- colnames(train.dfs$targets)
n.trees <- 50
shrinkage <- .001
interaction.depth = 4
n.pc  = 20
n.train <- ceiling(.85*dim(train.dfs$wave)[1])

par(mfrow=c(2,3))
for (target in c('P')){

  print(target)
  pp <- preProcess(x = train.dfs$wave, method = 'pca',  pcaComp = n.pc)
  gbm.objs[[target]]  <- gbm.fit( x = cbind(predict(object = pp, newdata = train.dfs$wave),train.dfs$spatial),
                                  y = train.dfs$targets[[target]], distribution = 'gaussian', 
                                  interaction.depth = interaction.depth, n.trees = n.trees, nTrain = n.train, shrinkage = shrinkage,
                                  response.name = target, verbose = TRUE )
  plot(sqrt(gbm.objs[[target]]$valid.error), main = target, xlab = 'n trees', ylab = 'RMSE')
 smry <- summary(gbm.objs[[target]] )
 important.vars[[target]] <- smry$var[smry$rel.inf > 0]
#  predictions[target] <- predict(object = gbm.objs[[target]], newdata = test.dfs$wave, 
#                                   n.trees = n.trees)
}


##
## Record results to disk.
##
#save('important.vars', file = './ivars.RData',)

#write.csv(predictions, file = './Data/Preds/GBM-R-preds.csv')


rm(list = ls())
