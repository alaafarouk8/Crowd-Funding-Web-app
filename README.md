# Crowd-Funding-Web-app
Crowdfunding is the practice of funding a project or venture by raising small amounts of money from a large number of people, typically via the Internet. Crowdfunding is a form of crowdsourcing and alternative finance. In 2015, over US$34 billion was raised worldwide by crowdfunding. (From Wikipedia​ ) The aim of the project​ : Create a web platform for starting fundraise projects in Egypt.

# create database and user 
- pip install django==3.2.10
- pip3 install djangorestframework
- pip install django-mathfilters
- pip install psycopg2
- sudo -i -u postgres
- psql
- create database fund
- create user funduser with password '123'
- alter user funduser with superuser;
- grant all privileges on database fund to funduser;
- \q
- psql -h localhost -U funduser fund
- psql -h localhost -U funduser fund
- djangorestframework-3.13.1

#API links:
projrcts: http://127.0.0.1:8000/fundapiprojectListView/
users: http://127.0.0.1:8000/usersusersListView/


