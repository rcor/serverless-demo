#import magic
#from io import BytesIO
import json
import base64
import cgi
import time
import boto3
import os

def uploadToS3(event):
   client = boto3.client('s3')
   filename = time.strftime("%Y%m%d-%H%M%S")+'.jpeg'
   print(event['body-json'])
   obj=event['body-json'].replace('data:image/jpeg;base64','')
   client.put_object(Body=base64.b64decode(obj),ContentType='image/jpeg', Bucket=os.environ['bucketDestino'], Key=filename)
   return filename;

def compare_faces(filename,threshold=80):
	rekognition = boto3.client("rekognition", os.environ['region'])
	response = rekognition.compare_faces(
	    SourceImage={
			"S3Object": {
				"Bucket": os.environ['bucketDestino'],
				"Name": filename
			}
		},
		TargetImage={
			"S3Object": {
				"Bucket": os.environ['BucketConMiCara'],
				"Name": os.environ['persona']
			}
		},
	    SimilarityThreshold=threshold,
	)
	return response['FaceMatches']

def lambda_handler(event, context):
   filename=uploadToS3(event)
   match = compare_faces(filename)
   print (match)
   result=match[0]['Similarity']>=90
   return ({
     "statusCode": 200, 
     "headers": {"Content-Type": "application/json"},
     "body": result
   })
