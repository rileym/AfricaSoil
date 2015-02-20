##
## Helper Functions
##

# Clean the soil data (drop carbon columns, split in useful ways)
soil.clean <- function(df, targets=FALSE){
  
  clean.dfs <- list()
  
  columns <- colnames(df)
  
  wave.cols <- 1:which(columns == 'm599.76')
  wave.df <- df[,wave.cols]
  carbon.cols <- which(columns == 'm2379.76'):which(columns == 'm2352.76')
  clean.dfs[['wave']] <- wave.df[,-carbon.cols]
  
  spatial.cols <- which(columns == 'BSAN'):which(columns == 'Depth')
  clean.dfs[['spatial']] <- df[,spatial.cols]
  
  if (targets) {
    clean.dfs[['targets']] <- df[,-c(wave.cols, spatial.cols)] 
  }
  
  return(clean.dfs)
}



# Metrics
mse <- function(y.pred, y.obs){  return( mean((y.pred-y.obs)^2) )  }
rmse <- function(y.pred, y.obs){  return( sqrt(mse(y.pred, y.obs)) )  }