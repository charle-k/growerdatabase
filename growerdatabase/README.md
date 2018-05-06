Setup:

Install the required libraries in requirements.txt.
I have included the sqlite database for demonstration purposes.
One you are able to run the app, you can use the following details to login:

username : admin
password : password1234

Task 1:
I have built a system which allows a user to upload data from CSV File in the specified
format. The data is cleaned, checked for correctness, checked if record does not already exists. You
can test this by using the two file included:
	-> testdata_without_errors.csv
	-> testdata_with_errors.csv


Task 2:
I have intergrated the site with Bulk SMS for it to send messages for those who have registered.
For the function to work, you have to add the username and key to gd/settings.py. it will try to send smses after completion of successful file upload. 
