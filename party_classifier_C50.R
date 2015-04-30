rm(list=ls())
require(randomForest)
require(caret)
require(varSelRF)
set.seed(998)

data <- read.csv('features_and_party_labels_grouped_by_mp.csv')
data$party <- factor(data$party)



#subset on remaining features
features <- c("number_of.austerity.","number_of.businesses.","number_of.cameron." ,"number_of.chaos.",
              "number_of.conservative.","number_of.crisis.","number_of.cuts.","number_of.economy.", 
              "number_of.end.","number_of.income.","number_of.jobs.","number_of.labour.",     
              "number_of.register.","number_of.scrap.","number_of.taxes.","number_of.tories.",     
              "number_of.unemployment.","number_of.vote."
              )
data <- subset(data, select = c("party",features))

#prepare for test/train split for caret
inTraining <- createDataPartition(data$party, p = 0.75, list = FALSE)
training <- data[inTraining, ]
testing <- data[-inTraining, ]


#resampling and hyperparameters
boot.control <- trainControl(method = "boot632",classProbs = TRUE)
cv.control <- trainControl(method="cv",number=10,repeats=5)

C50.grid <- expand.grid(.trials = 1,
                        .model = "rules",
                        .winnow =  FALSE
                        )

#training
C50.model <- train(party ~., data = training,
                   method='C5.0',
                   trControl = boot.control,
                   tuneGrid = C50.grid
                   )

#extract final model and test
final.model <- C50.model$finalModel

predictions <- predict(final.model, newdata = testing)
conf <- confusionMatrix(predictions,testing$party)
print(conf)


#serialize the final model
save(final.model, file = "C50_party_classifier.rda")
