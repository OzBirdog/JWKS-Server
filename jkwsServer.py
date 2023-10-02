#Author: Oz Birdett (oeb0010)
#Date: 10-1-2023
from flask import Flask, jsonify, request
import jwt
import datetime
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)

private_key = rsa.generate_private_key ( #Generates a RSA private key
    public_exponent = 65537, #Sets public exponent
    key_size = 2048 #Sets key size
)

pemPrivateKey = private_key.private_bytes ( #Converts the private key bytes to PEM
    encoding = serialization.Encoding.PEM, #Sets encoding to PEM format
    format = serialization.PrivateFormat.PKCS8, #Sets format to PKCS8
    encryption_algorithm = serialization.NoEncryption() #Sets it to no encryption
)

pemPublicKey = private_key.public_key().public_bytes ( #Retrieves the public key from the private key
    encoding = serialization.Encoding.PEM, #Sets encoding to PEM
    format = serialization.PublicFormat.SubjectPublicKeyInfo #Sets the format for a public key
)

kid = str(uuid.uuid4())  #Creates unique identifier using universally unique identifier

expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes = 5)  #Sets key expiration to 5 minutes

def getJwks(): #Receives GET requests and returns JKWS
    if datetime.datetime.utcnow() < expiration: #Checks if the expiration has happened
        jwks = { #JKWS dictionary
            "keys": [ #:List of Keys
                {
                    "alg": "RS256", #Algorithm
                    "kty": "RSA", #Key Type
                    "use": "sig",#Use of Key
                    "n": private_key.public_numbers().n, #Modulus component
                    "e": private_key.public_numbers().e, #Public exponent component
                    "kid": kid, #Unique Key Identifier
                }
            ]
        }
        return jsonify(jwks) #Returns a JSON response
    else:
        return "Key expired", 400 #Returns that the key has expired

@app.route('/auth', methods=['POST']) #Listens for POST requests
def authenticate():
    data = request.get_json() #Gets data from POST request
    username = data.get('username') #Gets username from JSON
    password = data.get('password') #Gets password from JSON
    #expiredQuery = 'expired' in request.args #Checks for expired parameter
    
    if username == "userABC" and password == "password123": #Checks username and password (Authentication Logic)
        if datetime.datetime.utcnow() < expiration:
            expiredPayload = { #Payload containing information for expired token
                "sub": username, #Subject of token 
                "exp": int(expiration.timestamp()), #Expiration of token
                "kid": kid  #Key ID of token
            }
            expiredToken = jwt.encode(expiredPayload, pemPrivateKey, algorithm='RS256') #Generates JWT
            return expiredToken, 200 #Return expired token
        else:
            payload = { #Payload containing information for token
                "sub": username, #Subject of token 
                "exp": int(expiration.timestamp()), #Expiration of token
                "kid": kid  #Key ID of token
            }
            token = jwt.encode(payload, pemPrivateKey, algorithm='RS256') #Generates JWT
            return token, 200 #Return token
        
    return "Authentication failed", 401 #Return authentication failed

if __name__ == '__main__': #Check flask app name
    app.run(port=8080) #Run app on port 8080

'''
 Use of ChatGPT in This Assignment
 I used ChatGPT to assist with coding the server as well as the test suite. I started off by asking ChatGPT to help create a JWKS server using flask. 
 From there I looked into how it encrypted the keys using RSA and changed the implementation method. After that I looked into how it made the JWKS
 Dictionary and rewrote the implementation for that. Then I asked ChatGPT how to create a "kid" and used the UUID method that it gave me. I then asked it how 
 to check if a JWKS key was expired before converting it to JSON. I implemented the method it gave me to check for expiration. Then I asked ChatGPT how
 to return both an expired and unexpired signed JWT on a POST request. I then added a way to check for expiration before sending out a signed JWT. Finally, 
 I asked ChatGPT to help create a test suite for my code, that would also give me a percentage of completion. I then made that code into the test suite file 
 I have. That's how I used ChatGPT during this assignment and the questions that I asked throughout to get to my goals.
'''
