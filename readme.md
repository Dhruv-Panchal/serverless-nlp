# Understanding the News: A Sentiment Analysis Model

News is important for a number of reasons within a society. Mainly to inform the public about events that are happening around them and that may affect them. 
***But what if these news channels that we religiously follow are biased, and we only get out half the sentiment? What if different news articles give out different sentiments and you are left confused at the end?*** 
And, If we were under the impression that the mainstream media is unbiased and committed to reporting “just the facts,” then the media spectacle in recent days should disabuse us of that outdated notion that the news is objective and unbiased.

In this project, we aim to present the users an unbiased view on the news around us. We fetch articles from **one or more news sources** and assess the **sentiment of each article presenting a larger picture of the tone of the article** without the need for dwelling deeper into each article for understanding the sentiment.

## Architecture


## Getting Started
These instructions will get you a copy of the project up and running on your Local Environment using Cloud Infrastructure 
```
git clone www.github.com/kashishshah881/serverless-nlp
```

### Prerequisites

- Python3.7
- GCP Account (Google cloud platform)
- Docker
- Streamlit

### Setup:

This project has folders that has all the files required for setting up the cloud infrastructure and 

1. For setting up the environment, we need to login to the GCP Console.
2. Create two Pub/Sub topics. 
3. Create a BigQuery dataset and a table with the schema.Note: *The column names are Case Sensitive*
| Column Name   | Variable Type |
| ------------- | ------------- |
| query         | STRING        |
| source        | STRING        |
| category      | STRING        |
| title         | STRING        |
| text          | STRING        |
| Sentiment     | STRING        |
| Magnitude     | STRING        |
| Name          | STRING        |
 
 
 
 
 
 
 schema name: schema type
    query: string
    source : string
    category : string
    title : 
    text
    sentiment

Config Files:

line 100: Guardian-data: 1st Pub/sub
line 70: Clean-data : 2nd pub/Sub
Streamlit: line 29: Cloud function 1 url(trigger)

Config foldfer: add credential file key.json


### Test cases:
Test cases 
-  



### Building and deploying custom ML Models on GCP AI Hub



## Built with

- Kashish Shah - Design, Architect and Deployment - [Linkedin](https://www.linkedin.com/in/shah-kashish/)
- Manogana Mantripragada - Machine Learning Engineer - [Linkedin](https://www.linkedin.com/in/manogna-mantripragada/)
- Dhruv Panchal - Frontend - [Linkedin](https://www.linkedin.com/in/panchaldhruv/)

## License

This project is licensed under the Commons Clause License - see the [LICENSE.md](https://commonsclause.com/) file for details.

## Acknowledgements
