rm(list=ls())
require(ggplot2)
require(plyr)
require(randomForest)
require(wordcloud)
require(reshape2)

#load the trained classifier and features labels

features <- row.names(importance(final.model))

data <- read.csv('features_and_party_labels_grouped_by_mp.csv')

data <- subset(data, select = c("party",features))


df <- ddply(data,.(party),colwise(sum))

# first remember the names
n <- names(df)

# transpose all but the first column (name)
df<- as.data.frame(t(df[,-1]))
colnames(df) <- n
df$feature <- factor(row.names(df))

str(df) # Check the column types
names(df) <- c("conservative","labour","feature")

df$feature <- mapvalues(df$feature, from = c("number_of.austerity.", "number_of.businesses.",
                                             "number_of.cameron.","number_of.chaos.",
                                             "number_of.conservative.","number_of.crisis.",
                                             "number_of.cuts.","number_of.economy.",
                                             "number_of.end.","number_of.income.",
                                             "number_of.jobs.","number_of.labour.",
                                             "number_of.register.","number_of.scrap.",
                                             "number_of.taxes.","number_of.tories.",
                                             "number_of.unemployment.","number_of.vote."),
                                    to = c("austerity", "businesses",
                                           "cameron","chaos",
                                           "conservative","crisis",
                                           "cuts","economy",
                                           "end","income",
                                           "jobs","labour",
                                           "register","scrap",
                                           "taxes","tories",
                                           "unemployment","vote")
                          )
                        
                    
################ text plot ################ 
#p <- ggplot(df,aes(x = conservative, y = labour, label = feature))  +
#  geom_text(aes(label=feature,position="jitter"),size = 4,angle=45,position = position_jitter(width=5, height=5)) + 
#  coord_trans(xtrans = 'log10',ytrans = 'log10') + theme_bw()
#p

################ bar plot
df <- melt(df)
names(df) <- c("feature","party","feature_count")
#p <- ggplot(df, aes(x = factor(feature), y = feature_count, fill=party)) +
#  geom_bar(stat = "identity",position="dodge") +
#  theme(axis.text.x = element_text(angle = 45, hjust = 1,size=12))
#p

lab <- subset(df,party=="labour")
cons <- subset(df,party=="conservative")

ratio <- data.frame(lab$feature,lab$feature_count/cons$feature_count)
names(ratio) <- c("feature","lab.to.cons")
ratio.df <- arrange(ratio,desc(lab.to.cons))

#map ratio to color
ratio.df$party.color <- unlist(lapply(ratio.df$lab.to.cons,function(x) {if(x < 1) "red" else "blue"}))

################ bubble chart
#,colour=party.color
ratio.df$feature <- reorder(ratio.df$feature, ratio.df$lab.to.cons)
p <- ggplot(data=ratio.df, aes(x=factor(feature), y=lab.to.cons)) +
  geom_point(aes(colour=party.color,size=lab.to.cons)) + 
  geom_point(shape = 1,aes(size=lab.to.cons),colour = "black")+
  geom_abline(intercept = 0, slope = 0) + 
  scale_size_continuous(range=c(8,20)) +
  xlab('keyword') +
  ylab('labour to conservative ratio') +
  #ylab('discriminative power') +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1,size=12),legend.position = "none",
        panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
  #scale_y_continuous(breaks=NULL)
  scale_y_log10(breaks=NULL)
p

