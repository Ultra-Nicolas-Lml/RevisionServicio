
# Revision de Estado

Este NB revisa el estado de un servicio y el tiempo en que responde


docker run -d --name jenkinsdem -p 8080:8080 -p 5000:5000 -v /home/ubuntu/Jenkins/jenkins_home:/var/jenkins_home jenkins/jenkins