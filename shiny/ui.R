shinyUI(
  fluidPage(
    titlePanel("Tweets Classifier"),
    fluidRow(
      column(10,
             textInput("text.to.classify", "Write a tweet")
             ),
      column(2,
             submitButton(text = "Classify Party"))
    ),
    fluidRow(verbatimTextOutput("text.class"))
  )
)