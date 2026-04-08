## Authorizing your application to use Google's API for account management

This guide details how to retrieve a client_secrets.json file which will inform Google to authorize sign-in through your account. This guide should be followed with the devops account. The client_secrets.json file must be accessible in your application's repository, but it should be kept private.

### Guide
1. Navigate to [https://console.developers.google.com/](https://console.developers.google.com/). Sign-in with your devops Google account.
2. In the 'Credentials' tab, select 'create' to create a project.
3. Fill in the respective fields and then click on 'create'.
4. After your project has been created, navigate to the 'Oauth consent screen'. Fill in the following fields and submit.

- email address: "your account's email address"
- product name shown to users: "whatever you want to call your ImHere implementation"
- homepage URL: "optional"
- product logo URL: "optional"
- privacy policy URL: "optional"
- terms of service URL: "optional"

5. Now navigate to 'Credentials'. Under 'create credentials', select 'OAuth client ID'.
6. Select 'Web application' for application type. Fill in the following fields and create.

- name: "name of your application"
- authorized javascript origins: "leave blank"
- authorized redirect URIs: http://localhost:4156/oauth/callback

7. Click OK on the following OAuth client popup.
8. Click on the name of the client ID that you just created to be redirected to the page you were just at.
9. At the very top, click on 'Download JSON' to download a json file which contains your client's secrets. You can rename this file if you like.
10. This json file must be referenced in your application to authorize the Google API through your devops account.