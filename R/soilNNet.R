library("nnet")
library('caret')

setwd('/Users/rileymatthews/Projects/Africa Soil')
source(file = './helpers.R')


##
## Load Data, Clean, & Split
##

full.df <- read.csv(file = './Data/training.csv', header = TRUE, row.names = 'PIDN')
full.test.df <- read.csv(file = './Data/sorted_test.csv', header = TRUE, row.names = 'PIDN')

N <- dim(full.df)[1]
train.prop <- .9
train.idx <- sample(x = 1:N, size = N*train.prop, replace = FALSE)

train.dfs <- soil.clean(df = full.df[train.idx,], targets = TRUE)
val.dfs <- soil.clean(df = full.df[-train.idx,], targets = TRUE)
test.dfs <- soil.clean(df = full.test.df, targets = FALSE)



pp <- preProcess(x = train.dfs$wave, method = c('center', 'scale')) # Just do wave for now

crude.reduction = seq(from = 1, to = dim(train.dfs$wave)[2], by = 4)
X <- predict(object = pp, newdata = train.dfs$wave)[,crude.reduction]
y <- train.dfs$targets$Sand #For now, just do sand.
  
nn.obj <- nnet(x = X, y = y, size = 5, maxit = 10000, decay = 5e-4, MaxNWts = 5000)

val.preds <- predict(object = nn.obj, newdata = predict(object = pp, newdata = val.dfs$wave)[,crude.reduction])
print(rmse(val.preds, val.dfs$targets$Sand))

#test.preds <- predict(object = nn.obj, newdata = predict(object = pp, newdata = test.dfs$wave))


















