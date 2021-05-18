# Hackalog-Backend

## Instructions for setting up this project
* Fork and clone the project in your device.
* `pipenv shell`
* `pipenv install`

#### Creating and securing firebase credentials
Below steps talk about creating and securing your firebase admin credentials, this step needs to be
done only once for setting up your `.env` file.
* Go to [Firebase console](https://console.firebase.google.com/project/_/settings/serviceaccounts/adminsdk) and create a firebase project.
* In firebase console go to **settings > [Service accounts](https://console.firebase.google.com/project/_/settings/serviceaccounts/adminsdk)**
* Click Generate New Private Key, then confirm by clicking Generate Key.
* Securely store the JSON file containing the key. Encrypt your Json file containing key using steps code given below:
* **Below code will generate a file named `firebase_admin.aes`, so if you already have this file(as it was present earlier on the repo) you may delete that file and then run below code.**.

```python
import pyAesCrypt
bufferSize = 64 * 1024
password = "please-use-a-long-and-random-password"
# encrypt
# Here firebase_admin.json is the name of Json file you get from from firebase.
pyAesCrypt.encryptFile("firebase_admin.json", "firebase_admin.aes", password, bufferSize)
```
* Keep this `firebase_admin.aes` file inside the project at `manage.py` level.
* At the same directory level create a file named `.env` and put contents into it by copying from another file named `template_env` which is already present.
* In your `.env` put value of `FIREBASE_DECRYPT_KEY` as the password you used for encrypting.

You have successfully created required environment variables.

* Now you can apply the migrations and start the server
