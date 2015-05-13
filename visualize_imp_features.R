rm(list=ls())
require(ggplot2)
require(plyr)
require(randomForest)
require(wordcloud)
require(reshape2)

#load the trained classifier and features labels
load("rf_party_classifier.rda")
features <- row.names(importance(final.model))


features <- c("number.of.austerity.","number.of.businesses.","number.of.cameron.","number.of.chaos.",       
"number.of.conservative.","number.of.crisis." ,"number.of.cuts.","number.of.economy.",  
"number.of.end.","number.of.income.","number.of.jobs.","number.of.labour.",      
"number.of.register.","number.of.scrap.","number.of.taxes.","number.of.tories.",      
"number.of.unemployment.","number.of.vote.")


data <- read.csv('features_and_party_labels_grouped_by_mp.csv')

data <- subset(data, select = c("party",features))

df <- ddply(data,.(party),colwise(sum))

# transpose all but the first column (name)
df<- as.data.frame(t(df[,-1]))

df$feature <- factor(row.names(df))

str(df) # Check the column types
names(df) <- c("conservative","labour","feature")

df <- subset(df, df$feature %in% c("number.of.austerity.", "number.of.businesses.",
                                   "number.of.cameron.","number.of.chaos.",
                                   "number.of.conservative.","number.of.crisis.",
                                   "number.of.cuts.","number.of.economy.",
                                   "number.of.end.","number.of.income.",
                                   "number.of.jobs.","number.of.labour.",
                                   "number.of.register.","number.of.scrap.",
                                   "number.of.taxes.","number.of.tories.",
                                   "number.of.unemployment.","number.of.vote."))

df$feature <- mapvalues(df$feature, from = c("number.of.austerity.", "number.of.businesses.",
                                             "number.of.cameron.","number.of.chaos.",
                                             "number.of.conservative.","number.of.crisis.",
                                             "number.of.cuts.","number.of.economy.",
                                             "number.of.end.","number.of.income.",
                                             "number.of.jobs.","number.of.labour.",
                                             "number.of.register.","number.of.scrap.",
                                             "number.of.taxes.","number.of.tories.",
                                             "number.of.unemployment.","number.of.vote."),
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
ratio.df$party.color <- unlist(lapply(ratio.df$lab.to.cons,function(x) {if(x < 1) "#d50000" else "#0087dc"}))

################ bubble chart
#,colour=party.color
ratio.df$feature <- reorder(ratio.df$feature, ratio.df$lab.to.cons)
p <- ggplot(data=ratio.df, aes(x=factor(feature), y=lab.to.cons)) +
  geom_point(aes(colour=party.color,size=10)) + 
  geom_point(shape = 1,aes(size=10),colour = "black")+
  geom_abline(intercept = 0, slope = 0) + 
  scale_size_continuous(range=c(8,20)) +
  xlab('keyword') +
  ylab('labour to conservative ratio') +
  #ylab('discriminative power') +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1,size=12),legend.position = "none",
        panel.grid.major = element_blank(), panel.grid.minor = element_blank()) +
  #scale_y_continuous(breaks=NULL)
  scale_y_log10(breaks=c(0.1,0.25,0.5,1,2.5,5,10))
p

################ treemap
require(treemap)
require(portfolio)

df$party.color <- unlist(lapply(df$party,function(x) {if(x == "labour") "#d50000" else "#0087dc"}))

treemap(df,index=c("feature","party"),vSize="feature_count",type="color",vColor="party.color",
        algorithm="pivotSize",fontsize.labels=c(12,0),border.col=c("#FFFFFF","#000000"),
        border.lwds=c(4,0),bg.labels = 0,fontfamily.labels="mono",title="")