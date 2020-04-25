# Understanding the News: A Sentiment Analysis Model

News is important for a number of reasons within a society. Mainly to inform the public about events that are happening around them and that may affect them. 
***But what if these news channels that we religiously follow are biased, and we only get out half the sentiment? What if different news articles give out different sentiments and you are left confused at the end?*** 
And, If we were under the impression that the mainstream media is unbiased and committed to reporting “just the facts,” then the media spectacle in recent days should disabuse us of that outdated notion that the news is objective and unbiased.

In this project, we aim to present the users an unbiased view on the news around us. We fetch articles from **one or more news sources** and assess the **sentiment of each article presenting a larger picture of the tone of the article** without the need for dwelling deeper into each article for understanding the sentiment.

## Architecture
<img src="https://github.com/kashishshah881/serverless-nlp/blob/master/img/arch.jpeg">

## Getting Started
These instructions will get you a copy of the project up and running on your Local Environment 
```
git clone www.github.com/kashishshah881/serverless-nlp
```
### Documentation: 
For Claat Documentation: [here](https://docs.google.com/document/d/1nqC3kqwIQBxHA7GCg8Wy516HHWqfMBf-7XVf9iy_HM4/edit?usp=sharing)

### Prerequisites

- Python3.7
- GCP Account (Google cloud platform)
- Docker
- Streamlit

### Setup:

This project has folders that has all the files required for setting up the cloud infrastructure and 

1. For setting up the environment, we need to login to the GCP Console.
2. Create two Pub/Sub topics. 
3. Create a BigQuery dataset and a table with the schema. Note: *The column names are Case Sensitive but the order doesnt matter.*

| Column Name   | Variable Type |
| ------------- | ------------- |
| date          | STRING        |
| query         | STRING        |
| source        | STRING        |
| category      | STRING        |
| title         | STRING        |
| text          | STRING        |
| Sentiment     | STRING        |
| Magnitude     | STRING        |
| Name          | STRING        |
| Organization  | STRING        |
| Location      | STRING        |
| Other         | STRING        |
 
 4. Change the Pubsub Topic Name [Here](https://github.com/kashishshah881/serverless-nlp/blob/master/gcloud/cloudfunctions/cloudFunction1/main.py#L100) to First Pubsub Topic
 
 5. Run ```gcloud functions deploy main_stream --runtime python37 --trigger-http``` on CLI inside the folder
 
 6. Change the Pubsub Topic Name [Here](https://github.com/kashishshah881/serverless-nlp/blob/master/gcloud/cloudfunctions/cloudFunction2/main.py#L70) to Second Pubsub Topic
 
 7. Run ```gcloud functions deploy hello_pubsub --runtime python37 --trigger-topic <Enter First Topic Name Here>``` on CLI inside the folder
 
 8. Setup a Pubsub To Google BigQuery Dataflow Job from [here](https://github.com/kashishshah881/serverless-nlp/blob/master/gcloud/dataflow/pubsubToBigQuery.java#L93) or Follow Steps [here](https://cloud.google.com/dataflow/docs/guides/templates/provided-streaming#cloudpubsubsubscriptiontobigquery)
 
 9. Setup a Pubsub to Google Datastore Dataflow Job. Follow Steps [here](https://cloud.google.com/dataflow/docs/guides/templates/provided-streaming#cloudpubsubtogcstext)
 
 10. Change the url on the frontend [here](https://github.com/kashishshah881/serverless-nlp/blob/master/frontend/main.py#L29)
 
 11. Create *config/key.json. key.json is the key downloaded from gcloud account. 
 To Download the file Follow [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)
 
 12. Run ```docker build .``` inside Frontend Folder
 13. Deploy the application on Kubernetes. Follow [here](https://codeburst.io/getting-started-with-kubernetes-deploy-a-docker-container-with-kubernetes-in-5-minutes-eb4be0e96370)
 

## Built with

- Kashish Shah - Design, Architect and Deployment - [Linkedin](https://www.linkedin.com/in/shah-kashish/)
- Manogana Mantripragada - Machine Learning Engineer - [Linkedin](https://www.linkedin.com/in/manogna-mantripragada/)
- Dhruv Panchal - Frontend - [Linkedin](https://www.linkedin.com/in/panchaldhruv/)

## License

This project is licensed under the Commons Clause License - see the [LICENSE.md](https://commonsclause.com/) file for details.

## Acknowledgements
1. https://imadelhanafi.com/posts/bigquery_dashboard/
2. https://www.oodlestechnologies.com/blogs/The-importance-of-Test-Case-In-Software-Testing/
3. https://towardsdatascience.com/game-of-thrones-twitter-sentiment-with-keras-apache-beam-bigquery-and-pubsub-382a770f6583
4. https://www.edureka.co/blog/test-case-in-software-testing/

