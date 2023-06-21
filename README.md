# Global-Vision

GlobalVision is an app that processes an image and recognizes and predicts what's in the picture, and then it says it out loud. GlobalVison uses an API database to process any image and identify it, along with utilizing text-to-speech to say the name of the image out loud. This product is built not only for anyone willing to try this new technology but also especially for those with impaired vision, giving them a chance to see the world. Although GlobalVision is not something that is necessarily ready to be incorporated into the daily lives of blind people, it is a step in the right direction to advocate for those with disabilities and push for positive change utilizing AI technology, giving everyone a chance to see.

this is the back end of the final product it contains the sign-in/sign-up API. which is implemented with the FastAPI Python library. 
this project works directly with the Android app available in this repository: https://github.com/dkaty1/GlobalVisionICS4U




# How to use
**PIP INSTALL requirements.txt**

Run application locally: uvicorn main:app --port 9000 --reload
Open API Specification: http://127.0.0.1:8000/docs <br />

to be able to use this application 
1. add user : 
 curl -X 'POST' \
  'http://127.0.0.1:8000/auth/create/user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "usr2",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "pwd2"
}' <br />

2. generate token for user
curl -X 'POST' 'http://127.0.0.1:8000/auth/token' -H 'accept: application/json' -H 'Content-Type: application/x-www-form-urlencoded' -d 'grant_type=&username=usr1&password=pwd1&scope=&client_id=&client_secret=' 


3. add users resource url use:
POST request on 
  http://127.0.0.1:8000/resourceurl/ 

define body with url_with_query_string in JSON format
{
  "url_with_query_string": "url_with_query_string_malware"
}

Add Bearer Token Authorization Header with User Token 

in case of the wrong token - response 401 - with 
{
  "detail": "Not authenticated"
}


4. check if URL is users URL use 
GET request on  
  http://127.0.0.1:8000/resourceurl/{resource_url_with_query_string}


   Add Bearer Token Authorization Header with User Token 

    in case of the wrong token - response 401 - with 
    {
    "detail": "Not authenticated"
    }

in case not users url - Return response 404 with 
{
    "detail": "ResourceURL not found in Malware DB"
} 

in case not users url - Return response 404 with 
{
    "detail": "ResourceURL not found in Malware DB"
} 

in case users url - return 200 with 
{
    "id": 2,
    "url_with_query_string": "url_with_query_string_malware"
}

# credits 
Authors: Nathaniel Shafran Avshalom, Dev Katyal <br />
ICS4U assignment\
