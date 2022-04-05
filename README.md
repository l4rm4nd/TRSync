# TRSync
Django web frontend for [pytr](https://github.com/marzzzello/pytr) to download all Trade Republic depot data.

![image](https://user-images.githubusercontent.com/21357789/161814477-ce72f4b0-a959-491b-a87d-986e3e7aa65f.png)

### How to use

1. Submit your mobile number and PIN code
2. Wait for the 2FA/OTP code sent to your mobile app
3. Submit your 2FA/OTP code and wait. Be patient!
4. Enjoy your whole trading history as one-time download (zip)
5. Optionally upload all PDFs to your personal account on https://www.parqet.com/ for a depot analysis
6. Optionally stargaze this repository to show your affection. I'll be happy ;-)

## Overview of depot data
The following depot data is retrieved:
![image](https://user-images.githubusercontent.com/21357789/161810816-74a130f6-4876-439c-803e-254a5b6b71b2.png)

### Building the docker container manually (recommended)
````
https://github.com/l4rm4nd/TRSync
cd TRSync
sudo docker build -t trsync -f docker/Dockerfile .
````

### Running the docker container (ephemeral, no persisted data)

````
sudo docker run -it --name trsync -p 127.0.0.1:8000:8000 -e SECRET_KEY=<YOUR-SECRET> -e DOMAIN=<DOMAIN-HOSTNAME> trsync:latest
````

If you trust me, please don't, you can use my public repository [l4rm4nd/trsync](https://hub.docker.com/repository/docker/l4rm4nd/trsync/general) on Dockerhub:

````
sudo docker run -it --name trsync -p 127.0.0.1:8000:8000 -e SECRET_KEY=<YOUR-SECRET> -e DOMAIN=<DOMAIN-HOSTNAME> l4rm4nd/trsync:latest
````

### Parameters
Container images are configured using parameters passed at runtime (such as those above). These parameters are separated by a colon and indicate <external>:<internal> respectively. For example, -p 8888:8000 would expose port 8000 from inside the container to be accessible from the host's IP on port 8888 outside the container.

| Parameter  | Function | Details
| ------------- | ------------- | -------------
| -e SECRET_KEY=\<KEY>  | Define a Django secret key | Optional, recommended for production use |
| -e DOMAIN=trsync.example.tld | Domain name used in settings.py for ALLOWED_HOSTS | Optional, recommended for production use |
| -p 8000 | Django web application via UWSGI (HTTP) | Optional, recommended for dev without reverse proxy |

## Disclaimer
I am not affiliated with Trade Republic Bank GmbH. 

This repository is a personal project to conveniently download all Trade Republic depot data.

I am not responsible for any data loss or security incidents. Please spawn a local, private docker instance.

**!! Do not submit credentials on foreign, untrusted sites !!**