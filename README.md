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

| Variables | Valor  |
|-----------------|--------------------------------------------------------------------------|
| BucketConMiCara | nombre_cara  ( bucket donde vamos a poner nuestra foto) |
| bucketDestino | nombre_destino ( Donde vamos a guardar las fotos que se suben) |
| persona | selfie.jpg ( foto con la que vamos a comparar) |
| region | deberiamos trabajando en **us-east-1** (Region donde estamos trabajando) |

### SlackNotificationLambda
Copiar el contenido del archivo notification/lambda_function.py dentro del editor de texto. 
Agregar las siguientes *Environment variables*
| Variables | Valor  |
|-----------|---------------------------------------------------------------------------------------|
| webhook | el webhook obtenido por [Incomming Webhooks](https://api.slack.com/incoming-webhooks) |
| canal | canal donde vamos a publicar |
| nombre | nuestro nombre |
| region | deberiamos trabajando en **us-east-1** (Region donde estamos trabajando) |

## SNS
El siguiente paso, es crear un topic dentro del servicio SNS con el nombre de **SlackNotification**
![SNS](https://content.screencast.com/users/rcor_cr/folders/Jing/media/4032902a-7452-4262-b51a-5dbe03f00dae/2018-10-06_2154.png)
Despues ingresarmos al *topic* y creamos una subcripcion apuntando al lambda **SlackNotificationLambda** 
![Subscription](https://content.screencast.com/users/rcor_cr/folders/Jing/media/51e10c48-0f03-442e-b11a-3c8c06683575/2018-10-06_2157.png)

Agregar dentro dentro del policy del topic 
![Update policy](https://content.screencast.com/users/rcor_cr/folders/Jing/media/a3502267-e0dc-4801-be44-aa1161781f7f/2018-10-06_2233.png)
Se debe tener cuidado al modificar este json
![Advance View](https://content.screencast.com/users/rcor_cr/folders/Jing/media/5c917c8e-60d8-40bd-a96d-717293ed9afc/2018-10-06_2232.png)

```json
{
      "Sid": "_s3",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "SNS:Publish",
      "Resource": "[ARN DEL TOPICO]",
      "Condition": {
        "StringEquals": {
          "aws:SourceArn": "arn:aws:s3:::nombre_destino"
        }
      }
}
```

## Buckets
Vamos a crear 3 buckets en la misma region (cambiar nombre por SU nombre ej )
* nombre_destino (ejemplo juliobarboza_destino)
  * Dentro del bucket vamos al tab *properties* y lo habilitamos como *Static website hosting*
![bucket website](https://content.screencast.com/users/rcor_cr/folders/Jing/media/6254c2af-0cd4-4832-bd4b-45b173face60/2018-10-06_2206.png)
  * Dentro del tab *Permissions* -> * Bucket policy * agregamos el siguiente permiso
  ![bucket policy](https://content.screencast.com/users/rcor_cr/folders/Jing/media/3d466842-7f0f-4884-b877-edab8ecfedca/2018-10-06_2236.png)
 ```json
 {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::nombre_destino/*"
        }
    ]
}
 ```
 Ahora agregamos la notificacion al topic de SNS, nos dirigimos dentro del bucket *Properties* -> *Events* -> *Add Notification*. Seleccionamos el evento *put* y buscamos el topic que creamos 
 
 ![Evento](https://content.screencast.com/users/rcor_cr/folders/Jing/media/4af8684a-d36d-4ef8-92d6-7776004c11ee/2018-10-06_2239.png)
 


* nombre_cara (ejemplo juliobarboza_cara)
* nombre_website (ejemplo juliobarboza_website)
  * Dentro del bucket vamos al tab *properties* y lo habilitamos como *Static website hosting*
![bucket website](https://content.screencast.com/users/rcor_cr/folders/Jing/media/6254c2af-0cd4-4832-bd4b-45b173face60/2018-10-06_2206.png)
  * Dentro del tab *Permissions* -> * Bucket policy * agregamos el siguiente permiso
  ![bucket policy](https://content.screencast.com/users/rcor_cr/folders/Jing/media/3d466842-7f0f-4884-b877-edab8ecfedca/2018-10-06_2236.png)
 ```json
 {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::nombre_destino/*"
        }
    ]
}
 ```

## API Gateway
## Cloudfront

