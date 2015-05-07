# capgemini_twitter_mps
 - A Python project to analyse tweets from UK mps in the run-up to the 2015 election. Part of the capgemini hack day in May 2015. We ended up focusing on building a classifier to discriminate betweeen Labour and Conservative politicians based on features of their tweets. We aggregated the tweets by MP and settled on features being counts over certain keywords (which appear in the file 'political_keywords.txt'). The classifier achieved accuracy of over 95% and we published a blog post on the Capgemini network appearing here 
https://www.uk.capgemini.com/blog/business-analytics-blog/2015/05/a-uk-party-political-classifier-based-on-mps-tweets-by-vasilis

- The twitter ids of the MP where obtained from http: //tweetminster.co.uk/mps which was scraped with 'scraper.py' resulting in the files 'conservative_mp_twitter_ids.csv','labour_mp_twitter_ids.csv','libdem_mp_twitter_ids.csv'

- Using the id csvs the tweets where obtained with 'get_tweets_TwitterAPI.py' and stored in the files 'conservative_tweets.csv','labour_tweets.csv','libdem_tweets.csv'

- Using the file 'make_features_for_predictive_models.py 'the tweets where then interogated for keywords appearing in 'politial_keywords.txt' and feature/target vectors created (these are not stored here for size considerations).

- Predictive models where created with 'party_classifier_rf.R' and 'party_classifier_C50.R'. The trained classifiers where serialized as 'rf_party_classifier.rda' and 'C50_party_classifier.rda'

- Exploratory data analysis of the tweets and visualizations of the classifier output where done in 'tweets_EDA.R','visualize_imp_features.R' which generate various word clouds, time series and other plots some of which are commited to this repo.




