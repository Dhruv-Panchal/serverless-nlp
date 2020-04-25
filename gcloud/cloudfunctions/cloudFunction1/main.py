import json
import requests
from datetime import date, timedelta
import datetime
from google.cloud import pubsub
import time
publish_client = pubsub.PublisherClient()
API_ENDPOINT = 'http://content.guardianapis.com/search'
MY_API_KEY = '9d65d521-8676-4067-b0d8-c82ab599c38a'

#start_date = date(2020, 4, 10)
#end_date = date(2020,4, 16)
#dayrange = range((end_date - start_date).days+1)


my_params = {
    'q':"",
    'from-date': "",
    "order-by":"newest",
    'to-date': "",
    'show-fields': 'body',
    'page-size': 200,
    'api-key': MY_API_KEY
}


def main_stream(request):
    content = request.json
    print(content)
    raw_keyword = content['keyword']
    if " " in raw_keyword:
        keyword = raw_keyword.replace(" ","%20")
    else:
        keyword = raw_keyword

    sdy = content['sdy'] 
    sdm = content['sdm'] 
    sdd = content['sdd'] 
    edy = content['edy'] 
    edm = content['edm'] 
    edd = content['edd'] 
    print(" SDY.   " ,sdy)
    start_date = datetime.date(sdy, sdm, sdd)
    print("START DATE.  ",start_date)
    end_date = datetime.date(edy, edm, edd)
    dayrange = range((end_date - start_date).days+1)
    my_params['q'] = keyword
    for daycount in dayrange:
        print(daycount)
        dt = start_date + timedelta(days=daycount)
        datestr = dt.strftime('%Y-%m-%d')
        fname = str(my_params['q'])+ "-" + datestr + '.json'
        # then let's download it
        print("Downloading", datestr)
        all_results = []
        my_params['from-date'] = datestr
        my_params['to-date'] = datestr
        current_page = 1
        total_pages = 1
        
        while current_page <= total_pages:
            print("...page", current_page)
            my_params['page'] = current_page
            time.sleep(1)
            resp = requests.get(API_ENDPOINT, my_params)
            data = resp.json()
            print(data['response']['total'])
            all_results.extend(data['response']['results'])
            print("Data coming till here!!!")
            for articleinfo in data['response']['results']:
                date = articleinfo['webPublicationDate'][:10]
                source = 'guardian'
                category = articleinfo['sectionName']
                title = articleinfo['webTitle']
                content = articleinfo['fields']['body']
                print("CONTENT"+content)
                put_to_stream(date,source,category,title,content,raw_keyword)
            current_page += 1
            total_pages = data['response']['pages']
        print("Writing to", fname)
        file_data = json.dumps(all_results, indent=4)
    return 'working'



def put_to_stream(newsDate, newSource, newsCategory,newsTitle,newsContent,newskeyword):
    payload = {
                
                'date': str(newsDate),
                'source': newSource,
                'category': newsCategory,
                'title': newsTitle,
                'text': newsContent,
                'query' : newskeyword

              }
    print("#########################")
    print(payload)
    bytes_payload = json.dumps(payload).encode('utf-8') 
    topic = <$Enter your pub/sub topic here>
    put_response = publish_client.publish(topic, bytes_payload)
    print(put_response)