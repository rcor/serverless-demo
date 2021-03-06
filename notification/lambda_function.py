from botocore.vendored import requests
import json
import boto3
import os

def detect_faces(bucket, key, attributes=['ALL'], region=os.environ['region']):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_faces(
	    Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
	    Attributes=attributes,
	)
	return response['FaceDetails']




def lambda_handler(event, context):
    print( event)
    subject =event['Records'][0]['Sns']['Subject']
    message=event['Records'][0]['Sns']['Message']
    messageJson=json.loads(message)
    eventName=messageJson['Records'][0]['eventName']
    url="https://hips.hearstapps.com/ghk.h-cdn.co/assets/17/40/3200x4799/labrador-retriever.jpg"
    messageR=''
    url="https://hips.hearstapps.com/ghk.h-cdn.co/assets/17/40/3200x4799/labrador-retriever.jpg"
    if (eventName=="ObjectCreated:Put"):
        bucketName=messageJson['Records'][0]['s3']['bucket']['name']
        key=messageJson['Records'][0]['s3']['object']['key']
        messageR += "Object:"+key
        url="http://"+bucketName+".s3-website-"+os.environ['region']+".amazonaws.com/"+key
        for face in detect_faces(bucketName, key):
        	messageR += "\nFace ({Confidence}%)".format(**face)
        	# emotions
        	for emotion in face['Emotions']:
        		 messageR += "\n {Type} : {Confidence}%".format(**emotion)
        	# facial features
        	for gender in face['Gender']:
        	    messageR+=gender
            
        
        postData = {
            'channel': os.environ['canal'],
            'username': 'SNS ',
            'text': '*' + os.environ['nombre'] +'* :bug:',
            'icon_emoji': ':bug:',
            'attachments':[
                {
                    'color': 'warning',
                    'text': messageR,
                    'image_url':url
                }
            ]
        };
        url=os.environ['webhook']
        r = requests.post(url,json=postData,headers={'Content-Type': 'application/json'})
        print(r.status_code, r.reason)
