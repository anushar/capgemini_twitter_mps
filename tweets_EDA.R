rm(list=ls())
require(ggplot2)
require(tm)
require(plyr)

labour <- read.csv("labour_tweets.csv")
conservative <- read.csv("conservative_tweets.csv")

labour <- subset(labour, select = c(created_at,favorite_count,retweet_count,user))
conservative <- subset(conservative, select = names(labour))

labour$party <- "labour"
conservative$party <- "conservative"

#convert to datetime
labour$created_at <- strptime(labour$created_at, "%Y-%m-%d %H:%M:%S")
conservative$created_at <- strptime(conservative$created_at, "%Y-%m-%d %H:%M:%S")

labour$date <- as.Date(labour$created_at)
labour$time <- format(labour$created_at,"%H:%M:%S")

conservative$date <- as.Date(conservative$created_at)
conservative$time <- format(conservative$created_at,"%H:%M:%S")

parties <- rbind(labour,conservative)
parties <- subset(parties, select = -created_at)
parties$date <- as.POSIXct(strptime(parties$date, "%Y-%m-%d"))

rm(labour)
rm(conservative)



tweet.count <- ddply(parties,.(date,party), summarize, freq=length(date))

p <- ggplot(tweet.count, aes(x = as.Date(date), y = freq, colour = party)) + geom_line() +
  scale_x_date() + xlab("Day") + ylab("Daily tweets") + theme_bw()
p








tweet.count <- tweet.count[complete.cases(tweet.count),]

tweet.count <- tweet.count[-c(127,128),]

p <- ggplot(tweet.count, aes(x = date, y = freq, colour = party)) + geom_line() +
    scale_x_date() + xlab("") + ylab("Daily tweets") + theme_bw()
p

######### count the mean number of likes per day per party and plot
mean.likes <- ddply(parties,.(date,party), summarize, mf=length(date))






