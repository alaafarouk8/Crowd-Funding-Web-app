# Crowd-Funding-Web-app
Crowdfunding is the practice of funding a project or venture by raising small amounts of money from a large number of people, typically via the Internet. Crowdfunding is a form of crowdsourcing and alternative finance. In 2015, over US$34 billion was raised worldwide by crowdfunding. (From Wikipedia​ ) The aim of the project​ : Create a web platform for starting fundraise projects in Egypt.

# create databse and user 
sudo -i -u postgres
psql
create user funduser with password '123'
alter user funduser with superuser;
grant all privileges on database fund to funduser;
\q
psql -h localhost -U funduser fund
