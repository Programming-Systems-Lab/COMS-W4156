Follow steps 1 through 3 on [Using sonarqube.com with Travis CI](https://docs.travis-ci.com/user/sonarqube/#Inspecting-code-with-the-SonarQube-Scanner) to obtain an encrypted authentication token and your project's organization.

In your `travis.yml` file uncomment the `addons` section to enable sonarqube. Be sure to also uncomment `sonar-scanner` in the `script` section. Fill in the `organization` and `secure` sections with the organization name and encrypted authentication token you obtained above. 

In your `sonar-project.properties` file update the `sonar.projectKey` with a key of your choice and the `sonar.projectName`.

Whenever a build is performed on Travis, sonarqube will run. You can see the results by logging in to [sonarqube.com](https://sonarqube.com) with your GitHub account and finding your project.  

