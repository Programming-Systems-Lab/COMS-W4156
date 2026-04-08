#### Travis Account (Devops person only)
Go to [Travis CI](https://travis-ci.com/) and sign in with your GitHub.  Only one person on the team needs to do this.  This person must be the owner of the repository.

    cp .travis.yml.ci .travis.yml

Follow their prompts to turn on Travis for this repo (short for repository).  

Test that Travis is working as expected.  Make another change and see whether the build passes.  It normally takes about 5 minutes, so go get a cup of coffee from Blue Java.

Additional guidance on setting up Travis CI for Python is available at [Travis CI](https://docs.travis-ci.com/user/languages/python/).
