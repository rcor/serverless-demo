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
| BucketConMiCara | nombre.cara  ( bucket donde vamos a poner nuestra foto) |
| bucketDestino | nombre.destino ( Donde vamos a guardar las fotos que se suben) |
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
          "aws:SourceArn": "arn:aws:s3:::nombre.destino"
        }
      }
}
```

## Buckets
Vamos a crear 3 buckets en la misma region (cambiar nombre por SU nombre ej )
* nombre.destino (ejemplo juliobarboza_destino)
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
            "Resource": "arn:aws:s3:::nombre.destino/*"
        }
    ]
}
 ```
 Ahora agregamos la notificacion al topic de SNS, nos dirigimos dentro del bucket *Properties* -> *Events* -> *Add Notification*. Seleccionamos el evento *put* y buscamos el topic que creamos 
 
 ![Evento](https://content.screencast.com/users/rcor_cr/folders/Jing/media/4af8684a-d36d-4ef8-92d6-7776004c11ee/2018-10-06_2239.png)
 


* nombre.cara (ejemplo juliobarboza_cara)
* nombre.website (ejemplo juliobarboza_website)
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
            "Resource": "arn:aws:s3:::nombre.destino/*"
        }
    ]
}
 ```

## API Gateway
* Ahora vamos al servicio de *Api Gateway* y creamos un nuevo API
![crear api](https://content.screencast.com/users/rcor_cr/folders/Jing/media/e6eb2aba-10ec-46cc-9148-87df8cc403b0/2018-10-06_2300.png)
* Creamos un metodo de tipo post y asociamos el Lambda que hemos creado *UploadToS3Lambda* al metodo
![Asociar lambda](https://content.screencast.com/users/rcor_cr/folders/Jing/media/06462a5b-8629-4af2-b808-add72d8a0356/2018-10-06_2301.png)

* Habilitamos el CORS para evitar problemas de dominio 
![enable cors](https://content.screencast.com/users/rcor_cr/folders/Jing/media/23688726-2e2f-40ed-9305-2768cbb96062/2018-10-06_2304.png)

* Ahora deployamos el api, vamos a crear un stage en el proceso
![Deploy](https://content.screencast.com/users/rcor_cr/folders/Jing/media/fff15b0a-14c8-433d-9a1e-cd5d0516d2d9/2018-10-06_2305.png)

* Con esto tenemos la URL del api gateway
![Api gateway](https://content.screencast.com/users/rcor_cr/folders/Jing/media/66776665-e101-4d06-9b25-13fbd8b06627/2018-10-06_2310.png)

Modificamos la linea 158 del archivo front/index.html con el endpoint
## Cloudfront

Ahora subimos el archivo index.html al bucket *nombre_website*. Despues vamos a crear la distribucion 
![Crear distribucion](https://content.screencast.com/users/rcor_cr/folders/Jing/media/3a4b9a3f-c90b-4e6a-b252-ec5c86a41407/2018-10-06_2314.png)

Seleccionamos el origen del CDN
![](https://content.screencast.com/users/rcor_cr/folders/Jing/media/9469eb00-2581-45e2-8b05-ed2deb9c5198/2018-10-06_2315.png)

Ponemos el archivo index.html para que rediriga 
![](https://content.screencast.com/users/rcor_cr/folders/Jing/media/2ae2db11-0996-46ff-971f-79d1098f810d/2018-10-06_2317.png)

Cuando hemos terminado estos pasos, va a tardar un par de minutos en deployar y vamos a tener un sitio hospeado en s3 con cloudfront

En el panel de cloudfront vamos a tener la URL por la cual vamos a acceder a probar 


