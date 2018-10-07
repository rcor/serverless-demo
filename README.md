# Descripcion 
 El siguiente ejemplo consiste en una aplicacion que permite subir fotos a un bucket de s3, ademas permite notificar a la aplicacion slack sobre el contenido de la fotografia subida 
# Requerimientos
 * Acceso a una cuenta de AWS [link](https://aws.amazon.com/free/)
 * Slack con permisisos de administrador [Slack](https://slack.com/)
 * Tener instalado y configurado [Incomming Webhooks](https://api.slack.com/incoming-webhooks) en slack 
# Arquitectura
![Arquitectura](https://content.screencast.com/users/rcor_cr/folders/Jing/media/c4705ef3-18cd-40c5-beed-8ec456117c1d/2018-10-06_2039.png)
# Pasos
Primero lo primero ingresar a la consola de aws 
## Permisos y Roles
Crear varios roles rol dentro del servicio AIM
* UploadToS3Role con los permisos: 
  * AmazonS3FullAccess
  * AmazonRekognitionFullAccess
  * AWSLambdaBasicExecutionRole
![UploadToS3Role](https://content.screencast.com/users/rcor_cr/folders/Jing/media/c197ce77-e17c-4f42-9dec-3de4b8e53aad/2018-10-06_2054.png)
* SlackRole
  * AmazonRekognitionFullAccess
  * AWSLambdaBasicExecutionRole
![SlackRole](https://content.screencast.com/users/rcor_cr/folders/Jing/media/4a69efaa-d211-417f-9aff-cee450668544/2018-10-06_2103.png)

## Lambda
Crear dos funciones lambda from scratch 
* UploadToS3Lambda 
* SlackNotificationLambda
![Lambda](https://content.screencast.com/users/rcor_cr/folders/Jing/media/12fc4e0b-0d69-4877-bf0e-c7e97d1a62a5/2018-10-06_2139.png)
Las funciones deben de tener las siguientes caracteristicas 
* Runtime "Python 3.6"
* Role "Choose an Existing Role"
* La funcion UploadToS3Lambda debe tener el role **UploadToS3Role**
* La funcion SlackNotificationLambda debe tener el role **SlackRole**

### UploadToS3Lambda
Copiar el contenido del archivo uploadToS3/lambda_function.py dentro del editor de texto. 
Agregar las siguientes *Environment variables*
Variables | Valor
------------ | -------------
BucketConMiCara | nombre_cara  ( bucket donde vamos a poner nuestra foto)
bucketDestino | nombre_destino ( Donde vamos a guardar las fotos que se suben)
persona| selfie.jpg ( foto con la que vamos a comparar)
region| deberiamos trabajando en **us-east-1** (Region donde estamos trabajando)

### SlackNotificationLambda
Copiar el contenido del archivo notification/lambda_function.py dentro del editor de texto. 
Agregar las siguientes *Environment variables*
Variables | Valor
------------ | -------------
region|deberiamos trabajando en **us-east-1** (Region donde estamos trabajando)
nombre| nuestro nombre
canal| canal donde vamos a publicar
webhook| el webhook obtenido por [Incomming Webhooks](https://api.slack.com/incoming-webhooks) 

## SNS
## Buckets


## API Gateway
## Cloudfront

