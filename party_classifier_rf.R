rm(list=ls())
require(randomForest)
require(caret)
require(varSelRF)
set.seed(998)

data <- read.csv('features_and_party_labels_grouped_by_mp.csv')
data$party <- factor(data$party)


#eliminate features
rf.vs1 = varSelRF(data[,-390], data[,390], ntree = 3000, ntreeIterat = 1000,
                  vars.drop.frac = 0.2)

#subset on remaining features
data <- subset(data, select = c("party",rf.vs1$selected.vars))

#prepare for test/train split for caret
inTraining <- createDataPartition(data$party, p = 0.75, list = FALSE)
training <- data[inTraining, ]
testing <- data[-inTraining, ]

#resampling
boot.control <- trainControl(method = "boot632",classProbs = TRUE)
cv.control <- trainControl(method="cv",number=10,repeats=5)

#training
rf.model <- train(party~.,data=training,
                method="rf",
                trControl = boot.control,
                ntree=3000,
                prox=TRUE,
                allowParallel=TRUE
                )

#extract final model and test
final.model <- rf.model$finalModel

predictions <- predict(final.model, newdata = testing)
conf <- confusionMatrix(predictions,testing$party)
print(conf)


#dump the importance and write to file for later analysis and visualization
#df.rfImportance <- data.frame(importance(final.model))
#write.table(df.rfImportance,file="rf_party_classifier_importances.csv")

#serialize the final model
#save(final.model, file = "rf_party_classifier.rda")




###some other importance plots
# varImpPlot(rf, sort = TRUE, class ="labour", type = 1)
# varImpPlot(rf, sort = TRUE, class ="conservative", type = 1) 
# partialPlot(rf, data, contains.tories.,"labour",main="For the labour category")
# partialPlot(rf, data, contains.tories.,"conservative",main="For the conservative category")
# 
# importance(rf,type=1,scaled=TRUE)

