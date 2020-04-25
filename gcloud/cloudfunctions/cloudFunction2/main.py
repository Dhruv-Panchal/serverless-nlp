import base64
import re
import googleapiclient.discovery
from googleapiclient import discovery
import json
import time
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import storage
import logging
from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()
# Instantiates a client
from google.cloud import pubsub
publish_client = pubsub.PublisherClient()
client = language.LanguageServiceClient()
regex = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')



def hello_pubsub(event,context):

    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    project = <$Enter project id here>
    region = 'us-central1'
    model = 'sentiment_model2'
    version='v_1'
    pubsub_message = base64.b64decode(event['data'])
    pubsub_message = pubsub_message.decode('utf-8')
    pubsub_message = json.loads(pubsub_message)
    print("----Event----", event)
    print(pubsub_message)
    #print("---Keys---", pubsub_message.keys())
    text = pubsub_message['text']
    clean_text = re.sub(regex, '', text)
    pubsub_message['text'] = clean_text
    document = types.Document(
        content=clean_text,
        type=enums.Document.Type.PLAIN_TEXT)
    encoding_type = enums.EncodingType.UTF32
    # Detects the sentiment of the text
    time.sleep(1)
    analys = client.analyze_sentiment(document=document)
    entity = client.analyze_entities(document=document,encoding_type=encoding_type)
    payload_entity = {'LOCATION':[],'NAME':[],'OTHER':[],'ORGANIZATION':[]}
    for ent in entity.entities:
            ent_name = ent.name
            entity_type = enums.Entity.Type(ent.type).name
            if entity_type in payload_entity:
                arr = payload_entity.get(entity_type)
                arr.append(ent.name)
                payload_entity[entity_type] = arr
            else:
                payload_entity[entity_type] = [ent_name]

    
    sentiment = analys.document_sentiment
    pubsub_message['Sentiment'] = sentiment.score
    pubsub_message['Magnitude'] = sentiment.magnitude
    pubsub_message['Location'] = str(payload_entity['LOCATION'])[2:-2]
    pubsub_message['Name'] = str(payload_entity['NAME'])[2:-2]
    pubsub_message['Other'] = str(payload_entity['OTHER'])[2:-2]
    pubsub_message['Organization'] = str(payload_entity['ORGANIZATION'])[2:-2]
    bytes_payload = json.dumps(pubsub_message).encode('utf-8') 
    topic = <$Enter your pub/sub topic here>
    put_response = publish_client.publish(topic, bytes_payload)
