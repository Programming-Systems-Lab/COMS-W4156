#### Setup Google Cloud Account (Everyone)
Create a Google Cloud account using your Columbia account at [https://cloud.google.com/](https://cloud.google.com/)
> Author's note: Easier to get academic credits, etc. if linked to you columbia.edu account.

#### Create a Google Cloud Project (Only one person)
Create a new project, say COMS4156.  The name does not really matter.  They will give you a cute name from your project name, e.g. "astute-anagram-165723".

#### Add other users to the Google Cloud Project (Only Devops person)
The first step after setting up your project is make it available to everyone on the team.  Go to the Google Cloud Dashboard, [https://console.cloud.google.com/home/dashboard](https://console.cloud.google.com/home/dashboard), then "IAM & Admin" then ["IAM"](https://console.cloud.google.com/iam-admin/iam/project).  Click on "+Add" and add your other team members.  For role, add them as "Project" > "Owner".

#### Run the Google Cloud Tutorial (Everyone)
Navigate to [https://cloud.google.com/appengine/](https://cloud.google.com/appengine/) and follow their "My First App Tutorial."  It will help you understand how app engine works.

Additional information is here: [Google](https://cloud.google.com/appengine/docs/standard/python/getting-started/python-standard-env) and [QuickStart](https://cloud.google.com/appengine/docs/standard/python/quickstart).

#### Setup Google Cloud SDK App Engine (Everyone)
Setup the Google Cloud SDK on your virtual machine:

    gcloud init

Google will have you sign into your Google account.  Use the one with which you signed up for Google Cloud.

* Select your project.
* `Do you want to configure Google Compute Engine (https://cloud.google.com/compute) settings (Y/n)` **Y**
* `Which Google Compute Engine zone would you like to use as project default?` 16 (us-east1-c)
* `Which Google Compute Engine region would you like to use as project default?` 6 (us-east1)


We've setup the configuration files: `app.yaml` and `appengine_config.py`.  If you do more advanced functionality, you may need to change `app.yaml` and Google's docs are good at describing the various settings.  `appengine_config.py` just tells App Engine where to look for libraries.  Speaking of which...

#### Configure ImHere for your Project (Only One Person)
You will need to edit two files from the repo with the name of your project.  Change from `test-4156` to your Google Cloud project name (the funny one Google gave you.)
    
    models/model.py
    config.py

Add these to your repo, commit, and push to GitHub.  Everyone else should pull the changes.

#### Download your Google Cloud Certificates (Everyone)
You will need to download two certificates and a key from Google Cloud:
    
    client_secrets_oauth.json
    cred.json
    api_key.py

##### Certificate 1: OAuth2 Certificate
This guide details how to retrieve a `client_secrets_oauth.json` file which will inform Google to authorize sign-in through your account. The `client_secrets_oauth.json` file must be accessible in your application's repository, but it should be kept private.  Everyone can either create their own certificate or one person can do it can give them to everyone.  **Save to your local Git directory, but do not add to the repo.  This file is part of the default .gitignore, so just don't override the .gitignore.**

1. Navigate to [https://console.developers.google.com/](https://console.developers.google.com/) then choose "Credentials".
2. After your project has been created, navigate to the 'Oauth consent screen'. Fill in the following fields and submit.

- email address: "your account's email address"
- product name shown to users: "whatever you want to call your ImHere implementation"
- homepage URL: "optional"
- product logo URL: "optional"
- privacy policy URL: "optional"
- terms of service URL: "optional"

3. Now navigate to 'Credentials'. Under 'Create credentials', select 'OAuth client ID'.
4. Select 'Web application' for application type. Fill in the following fields and create.

- name: "name of your application"
- authorized javascript origins: "leave blank"
- authorized redirect URIs: `http://localhost:4156/oauth/callback` and `https://test-4156.appspot.com/oauth/callback` where `test-4156` is replaced by your project name.

5. Click OK on the following OAuth client popup.
6. Click on the name of the client ID that you just created to be redirected to the page you were just at.
7. At the very top, click on 'Download JSON' to download a json file which contains your client's secrets. This needs to be renamed `client_secrets_oauth.json`.

##### Certificate 2: Service Key
Turn on [“Google App Engine Admin API”](https://console.developers.google.com/apis/).  Click on Dashboard and the "+Enable API."then search for `Google App Engine Admin API`.  Click on Enable at the top.

Go to “Credentials”, click “Create Credentials” and “Service account key”, select "Google App Engine Service Key", finally click “JSON” to download the your Service Account JSON file.  Rename to `cred.json`. **Save to your local Git directory, but do not add to the repo.  This file is part of the default .gitignore, so just don't override the .gitignore.**

    export GOOGLE_APPLICATION_CREDENTIALS=cred.json

##### Certificate (sort of) 3: API Key

Go to “Credentials”, click “Create Credential” and “API key” and copy to your clipboard.  Click on "Restrict Key" and restrict the API key to an HTTP referrer `www.travis-ci.org`. (This keeps people from hijacking your website.) Rename `api_key.py.sample` in the repo to `api_key.py`.  Within `api_key.py`, change `'YOU-API-KEY'` to the API key from Google Cloud.  *Be sure to keep the quotes around the key*.  **Save to your local Git directory, but do not add to the repo.  This file is part of the default .gitignore, so just don't override the .gitignore.** 

#### Deploy the Application
You'll need to install the libraries again to put them in the right place for App Engine (`lib/`).  `env/lib` has these files plus many more.  This will only need to be run initially and then whenever a new module is added.

    pip install -t lib -r requirements.txt

Now deploy the application to App Engine.

    gcloud app deploy

Verify that it is deployed by 

    gcloud app browse

We strongly recommend that you browse the App Engine docs to get a feel for what is happening under the hood.

