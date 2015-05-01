rm(list=ls())
require(ggplot2)
require(wordcloud)
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



######## count and plot the tweets by day and party ########
tweet.count <- ddply(parties,.(date,party), summarize, freq=length(date))

######## remove NA and final incomplete day
tweet.count <- tweet.count[complete.cases(tweet.count),]
tweet.count <- tweet.count[-c(127,128),]

p <- ggplot(tweet.count, aes(x = as.Date(date), y = freq, colour = party)) + geom_line() +
  scale_x_date() + xlab("Day") + ylab("Daily tweets") + theme_bw()
p


######### count the median number of likes per day per party and plot
engagement.summaries <- ddply(parties,.(date,party), summarize,
                           median.fc=median(favorite_count),
                           median.rtc=median(retweet_count),
                           mean.fc=mean(favorite_count),
                           mean.rtc=mean(retweet_count),
                           q50.fc = quantile(favorite_count,probs=0.5,na.rm=TRUE),
                           q50.rtc = quantile(retweet_count,probs=0.5,na.rm=TRUE)
                           )

p <- ggplot(engagement.summaries, aes(x = as.Date(date), y = mean.fc, colour = party)) + geom_line() +
  scale_x_date() + xlab("Day") + ylab("Daily mean favourite count") + theme_bw()
p

p <- ggplot(engagement.summaries, aes(x = as.Date(date), y = mean.rtc, colour = party)) + geom_line() +
  scale_x_date() + xlab("Day") + ylab("Daily mean retweet count") + theme_bw()
p

######### compute histograms of tweet posts by user

######### compute wordcloud with word size prop to user number of posts
tweet.stats.by.user <- ddply(parties,.(user,party), summarize, freq=length(user),
                             mean.fav=sum(favorite_count)/length(user),
                             mean.rt=sum(retweet_count)/length(user),
                             median.fav=median(favorite_count),
                             median.rt=median(retweet_count)
                             )



#tweet.count.by.user$color <- lapply(function(x) {if(x == "labour") "red" else "blue"},tweet.count.by.user$user)

#map the mps to blue or red color
tweet.stats.by.user$color <- unlist(lapply(tweet.stats.by.user$party,function(x) {if(x == "labour") "red" else "blue"}))

#there are a couple of NA users
tweet.stats.by.user <- tweet.stats.by.user[complete.cases(tweet.stats.by.user),]

#do some wordclouds
size <- tweet.stats.by.user$median.rt

wordcloud(tweet.stats.by.user$user,
          size,
          rot.per=0.0,
          colors=tweet.stats.by.user$color,
          scale=c(2,1),  
          max.words = 20
          )





######### get the top ten in count,likes,retweets

#compare Cameron and Miliband
top.dudes <- subset(tweet.stats.by.user,user  %in% c('@Ed_Miliband','@David_Cameron'))