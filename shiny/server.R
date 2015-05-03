require(randomForest)
require(caret)
require(tm)
load("rf_party_classifier.rda")
keywords <- unname(sapply(final.model$xNames,
                          function(x){unlist(strsplit(x, "\\."))[2]}))
tf <- rep(0, length(keywords))
names(tf) <- keywords

predict.string <- function (text){
  tmp <- termFreq(PlainTextDocument(text))
  tf[which(keywords %in% names(tmp))]  <- tmp[names(tmp) %in% keywords]
  if(sum(tf) == 0){return(NULL)}
  else({return(as.character(predict(final.model, newdata = tf)))})
}

shinyServer(function(input, output) {
  output$text.class <- renderText(predict.string(input$text.to.classify))
})