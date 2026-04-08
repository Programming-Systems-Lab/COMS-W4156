You can integrate GitHub into Slack so that you see all commits.  You can do the same with [Travis builds](https://docs.travis-ci.com/user/notifications/#Configuring-slack-notifications).  

The Google Cloud app is pretty good and allows you to see the console from your phone.  Can be helpful if you are helping someone debug. 

Use tail to look at App Engine logs: `gcloud app logs tail -s default`.

Create separate production and testing projects.  Use Travis to deploy under a different project name with a different set of keys.  Have everyone else work under another project.  Recommended after a couple of weeks.

Run Prospector, [http://prospector.landscape.io/en/master/](http://prospector.landscape.io/en/master/), on the code for static analysis.

    pip install prospector

Google Cloud Datastore has an emulator that can be used during development and testing.  It is very easy to [setup](https://cloud.google.com/datastore/docs/tools/datastore-emulator).
