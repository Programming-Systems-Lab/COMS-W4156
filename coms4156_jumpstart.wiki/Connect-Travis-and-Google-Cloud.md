You are going to follow the guides from [Travis CI](https://docs.travis-ci.com/user/deployment/google-app-engine/) and [Google Cloud](https://cloud.google.com/solutions/continuous-delivery-with-travis-ci).  Information on the Travis CI tool is available [here](https://blog.travis-ci.com/2013-01-14-new-client/).

You will use the two certificates from Google Cloud to work with Travis, an API key `api_key.py` and a secret key `client_secrets_oauth.json`.  Neither should go into your repo unencrypted.  

Assuming you installed Ruby earlier, simply call `sudo gem install travis`

Login to Travis with your GitHub account.
    
	travis login --org

Switch to the continuous deployment `.travis.yml`

	cp .travis.yml.google .travis.yml

Tar your credentials into a single file:

	tar -czf credentials.tar.gz cred.json api_key.py client_secrets_oauth.json

Encrypt your credentials in your Git directory.  

	travis encrypt-file credentials.tar.gz

Travis will give you a line like `openssl ...  ` edit `.travis.yml` to set up continuous deployment by adding that line in place of the the existing lines.  Change `project: google_cloud_project_id` to the proper name.

Commit changes to you Git repo.

	git add credentials.tar.gz.enc .travis.yml
	git commit -m "Added keys for Google App deployment"
	git push

Verify that everything is working as expected.  Look at the Travis CI log, make a small change to the application and make sure it ended up there.
