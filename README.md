honeybank
==============
The honeybank is a demo implementation of [Flask-HoneyAuth](https://github.com/prhiggins/Flask-HoneyAuth) that demonstrates developing high-interaction honeypots in Flask using the library.

Build Instructions
------------
To build and run the app using docker, first clone the repository:
```
git clone https://github.com/prhiggins/honeybank.git
```
Then simply build and run the image using the provided Dockerfile:
```
docker build . -t honeybank && docker run -p 5000:5000 honeybank
```

Usage
----------------------------
To authenticate to the app as a regular user, review the `users` dictionary:
```
users = {
        "john": generate_password_hash("hello"),
        "susan": generate_password_hash("bye"),
        "dave": generate_password_hash("realdave")
}
```
To authenticate to the app with a honey token, review the `honey_users` dictionary:
```
honey_users = {
        "dave": generate_password_hash("imnotdave"),
        "alice": generate_password_hash("asdfghj"),
        "winston": generate_password_hash("honeybear")
}
```
Authenticating as a regular user will allow normal transactions. However, authentications with honey tokens will result in redirection to the honey universe, where transactions are separated.
Author
----------------------------
Patrick Higgins (phiggin5@uoregon.edu)
