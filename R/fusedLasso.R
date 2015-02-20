###
### Soil Project: Fused Lasso Model
###

library('genlasso')
library('caret')
source(file = './helpers.R')


##
## Load Data, Clean, & Split
##


setwd('/Users/rileymatthews/Projects/Africa Soil')

full.df <- read.csv(file = './Data/training.csv', header = TRUE, row.names = 'PIDN')
full.test.df <- read.csv(file = './Data/sorted_test.csv', header = TRUE, row.names = 'PIDN')

set.seed(1234)

N <- dim(full.df)[1]
train.prop <- .9
train.idx <- sample(x = 1:N, size = N*train.prop, replace = FALSE)

train.dfs <- soil.clean(df = full.df[train.idx,], targets = TRUE)
val.dfs <- soil.clean(df = full.df[-train.idx,], targets = TRUE)
test.dfs <- soil.clean(df = full.test.df, targets = FALSE)


# Make folds
k = 5
kfolds <- createFolds(y = train.dfs$targets$Ca, k = k)


targets <- colnames(train.dfs$targets)
D <- getD1dSparse(dim(train.dfs$wave)[2])
rmse.results
for (target in targets){
  
  for (fold in kfolds){
    #preprocess?
    fit <- genlasso(train.dfs$targets[[target]], as.matrix(train.dfs$wave[fold,]), D, approx = FALSE, maxsteps = 2000, minlam = 1e-4,
                    rtol = 1e-07, btol = 1e-07, eps = 1e-4, verbose = FALSE,
                    svd = FALSE) 
  
    for () { #Predict validation set for each alpha on the path
    
      
    
    }
  
  # compute rmse for each alpha,
  }
  
}
