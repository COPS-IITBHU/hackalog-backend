# Hackalog-Backend

## Instructions for setting up this project
* Fork and clone the project in your device.
* `pipenv shell`(If you're not aware of what pipenv, have look at [this blog](https://realpython.com/pipenv-guide/)).
* `pipenv install`

#### Creating and securing firebase credentials
Below steps talk about creating and securing your firebase admin credentials, this step needs to be
done only once for setting up your `.env` file.
* Go to [Firebase console](https://console.firebase.google.com/project/_/settings/serviceaccounts/adminsdk) and create a firebase project.
* In firebase console go to **settings > [Service accounts](https://console.firebase.google.com/project/_/settings/serviceaccounts/adminsdk)**
* Click Generate New Private Key, then confirm by clicking Generate Key.
* Save the Json file containing key details, with name `firebase_admin.json` in same level directory as manage.py.
* Open a file named `encrypt_credentials.py` already present in same directory, and **edit the password(line: 6) you want to use for encryption**.
**Note:** You are advised to use long and random password, as you do not need to remember it after that.
* Run `python encrypt_credentials.py` to encrypt your Json file. This will generate a file named `firebase_admin.aes` and will also print `FIREBASE_DECRYPT_SIZE` in the output.
* Create a file named `.env` and copy contents into it from another file named `template_env` which is already present.
* In your `.env` file put the value of `FIREBASE_DECRYPT_KEY` as the password you used for encryption, and `FIREBASE_DECRYPT_SIZE` as the number generated in output that came after encrypting the file.
* Undo the changes you made to encrypt_credentials.py(that is again make the password as `please-use-a-long-random-password`), **otherwise your encryption key(password) will become public**.

You have successfully created required environment variables.

* Now you can apply the migrations and start the server
