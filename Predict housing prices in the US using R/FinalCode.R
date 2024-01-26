# Clear environment and load libraries
rm(list = ls())
library(dplyr)
library(forecast)
library(randomForest)
library(caret)
library(psych)
library(caTools)
library(tidyr)
library(xlsx)
library(ggplot2)
library(mice)
library(lmtest)
library(car)

#Import data
setwd("C:/Users/danie/OneDrive/Documents/dsc520-DD")
original.train <- read.csv("Final Data/train.csv", stringsAsFactors=TRUE)

# Check Dataset
head(original.train)

#it appeared that the dataset contains <NA>, check the proportion of of <NA> in the dataset
colSums(is.na(original.train))

# Replace Null values in all columns with 'NA'

modified.train <- original.train %>%
  mutate_if(is.integer, ~ifelse(is.na(.), 0, .))

# Import and cleaning the test data with the same steps

original.test <- read.csv("Final Data/test.csv", stringsAsFactors=TRUE)
colSums(is.na(original.test))

modified.test <- original.test %>%
  mutate_if(is.integer, ~ifelse(is.na(.), 0, .))

# Now we combine train and test data into 1 file. We can combine using either R or Exel. 

df <- rbind(modified.train, modified.test, stringAsfactors = TRUE)

# set the file path and name
file <- "cleaned_data.csv"

# write the data frame to an csv file
write.csv(df, file)


# Load cleaned dataset
mydf <- read.csv("Final Data/cleaned_data.csv", stringsAsFactors=TRUE)


#Plot variables appeared to be inficient to use

ggplot(mydf, aes(x = Street, fill = Street )) +
  geom_bar() + scale_fill_hue(c = 80)

ggplot(mydf, aes(x = Utilities, fill = Utilities)) +
  geom_bar()+ scale_fill_hue(c = 80)

ggplot(mydf, aes(x = Condition2, fill = Condition2)) +
  geom_bar()+ scale_fill_hue(c = 80)

ggplot(mydf, aes(x = Heating, fill = Heating)) +
  geom_bar()+ scale_fill_hue(c = 80)

ggplot(mydf, aes(x = Alley, fill = Alley)) +
  geom_bar()+ scale_fill_hue(c = 80)

#remove variables
#impute data using mice
#to remove these variables
mydf$Utilities = NULL
mydf$Condition2 = NULL
mydf$Street = NULL
mydf$RoofMatl = NULL
mydf$Heating = NULL
mydf$Alley = NULL
mydf$Alley = NULL
mydf$Id = NULL
#impute missing variables in LotFrontage and GarageAge
## Attaching package: 'mice'
## The following object is masked from 'package:stats':
## filter
## The following objects are masked from 'package:base':
## cbind, rbind
mice.house <- mice(mydf, m=5, maxit=50, method='cart', seed=500)

completedfcombine = complete(mice.house, 5)

colSums(is.na(completedfcombine))

summary(completedfcombine)

#As it is time consuming to run Mice , we will save this dataset into a .csv file to use later
#This avoid running mice repeatedly every time we run this project
write.csv(completedfcombine, "completedf.csv")

completedfcombine <- read.csv("completedf.csv", stringsAsFactors=TRUE)

## MULTIPLE LINEAR REGRESSION AND REGRESSION ASSUMPTION USING ALL VARIABLES

completedfcombine <- completedfcombine %>%
  mutate(across(where(is.numeric), scale))

#multiplereg for whole dataset
multiple_reg <- lm(SalePrice~., data =completedfcombine)
summary(multiple_reg)

# RESET Test for Omitted Variable Test
resettest(multiple_reg, power=2, type="regressor", data = completedfcombine)

#VIF test to detect Multicolinearity 
#vif(multiple_reg)
## we could not run the multicolinearity test due to perfectly correlated variables

#define intercept-only model
intercept_only <- lm(SalePrice ~ 1, data=completedfcombine)
#define model with all predictors
reg_model <- lm(SalePrice ~ ., data=completedfcombine)
#perform forward stepwise regression
forward <- step(intercept_only, direction='forward', scope=formula(reg_model), trace=0)
#view results of forward stepwise regression
forward$anova

#view final model
forward$coefficients

###BACKWARD STEPWISE SELECTION

#perform backward stepwise regression
backward <- step(reg_model, direction='backward', scope=formula(reg_model), trace=0)
#view results of backward stepwise regression

backward$anova

#view final model

backward$coefficients

##MULTIPLE LINEAR REGRESSION ON SELECTED VARIABLES - CHECK REGRESSION ASSUMPTION

#create a dataframe for variable selection
finaldf <- completedfcombine %>% select(LotArea,LandContour,BldgType,OverallQual,OverallCond
                                        ,MasVnrType,MasVnrArea,ExterQual,BsmtQual,BsmtFinType1,BsmtFinSF1,
                                        TotalBsmtSF,Electrical,GrLivArea,KitchenAbvGr,KitchenQual,TotRmsAbvGrd,
                                        Functional,Fireplaces,GarageType,GarageFinish,GarageCars,WoodDeckSF,
                                        ScreenPorch,MiscVal,MoSold,SaleCondition,SalePrice)
summary(finaldf)
#multiple regression after the variable selection
multiple_reg2 <- lm(SalePrice~., data=finaldf)
summary(multiple_reg2)

# RESET Test for Omitted Variable Test
resettest(multiple_reg2, power=2, type="regressor", data = finaldf)
## 
## RESET test
## 
## data: multiple_reg2
## RESET = 11.747, df1 = 16, df2 = 2799, p-value < 2.2e-16
#VIF test to detect Multicolinearity 
##vif(multiple_reg2)

## Random Forest 

#import completedcombine data set (to avoid running mice all over again)
mydf <- read.csv("completedf.csv", header = TRUE, stringsAsFactors = TRUE)
data <- mydf %>% mutate(across(where(is.numeric), scale))
#data partition
#select seed to make the random selection repeatable 
set.seed(123)
#randomly divided the data into 2 parts: train and test. 
#Train dataset has 70% of the original data, test dataset has 30% of the original data
ind <- sample(2, nrow(data), replace = TRUE, prob = c(0.7, 0.3))
train <- data[ind==1,]
test <- data[ind==2,]
#2034 observations in train data, 848 observations in test dataset
#RANDOM FOREST
#start with the basic random forest model. Using train data set to build a model. 
set.seed(222)
rf <- randomForest(SalePrice~., data=train,
                   importance = TRUE)
rf
#error rate of random forest
#as the number of trees increase, the out of bag error decrease. 
#however, the error is not improved after 120 trees.
#hence, instead of 500 trees, number of trees will be changed to 120
plot(rf, main = 'Random Forest Error Rate')

#tune mtry
set.seed(123)
t<- tuneRF(train[,-73], train[,73],stepFactor = 0.5,
           plot = TRUE,
           ntreeTry = 300,
           trace = TRUE,
           improve = 0.05)
print(t)
#as shown in the graph, the Out Of Bag Error is lowest when mtry=48
#hence, we adjust the original df to 300 trees and 48 variables each split
set.seed(222)
rf_new <- randomForest(SalePrice~., data=train, ntree =300,
                       mtry = 48,
                       importance = TRUE,
                       proximity = TRUE)
print(rf_new)

#plot feature importance
importance(rf)
varImpPlot(rf)

#prediction - test data
set.seed(222)
predict_test <- predict(rf_new, test)
# Performance evaluation using r-squared and RMSE
actual <- test$SalePrice
predicted <- predict_test
R2 <- 1 - (sum((actual-predicted)^2)/sum((actual-mean(actual))^2))
R2
caret::RMSE(predict_test,test$SalePrice)
summary(test$SalePrice)
