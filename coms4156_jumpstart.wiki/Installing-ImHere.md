#### Setup GitHub.com Account (Everyone)
Create a GitHub [account](https://github.com/), if you don't already have one.  
> In the future, you may want to sign up for the [Student Developer Pack](https://education.github.com/pack), but you don't need it for this class.

Create and install SSH keys on your machine using this [guide.](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#platform-linux) You will need to do this for you new Virtual Machine.

Install SSH keys on GitHub using this [guide.](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/#platform-linux)

#### Fork coms4156_jumpstart Repository (Only the Devops person)
Go to [coms4156_jumpstart](https://github.com/gailkaiser/coms4156_jumpstart) and click the Fork button in the upper right hand side.

#### Add collaborators to GitHub (Only the Devops person)
Add your teammates to your GitHub account.  Directions are available at [GitHub.com](https://help.github.com/articles/inviting-collaborators-to-a-personal-repository/).  In short, from the repo home page, go to "Settings", then "Collaborators" add their accounts.

#### Clone coms4156_jumpstart Repository (Everyone)

Clone the repository to your local machine, using the proper account.

    git clone git@github.com:*your_account*/coms4156_jumpstart.git
    cd coms4156_jumpstart

#### Verify GitHub is configured correctly (Everyone)
If you have never run the `git push` on this (virtual) machine to GitHub you will get a prompt to set up your configuration:

    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"
    git config --global push.default matching

Make a change.  Edit `README.md` to include your name and team name.  If you don't have a favorite text editor, run `nano README.md`, edit ctrl-x to quit.  Then go pick a favorite text editor, like vi, vim, gedit, sublime, etc. and learn how to use it. 

    git add README.md
    git commit -m "Added my name to the README file."
    git push

Verify that your change to the README shows up on GitHub.com.

#### Creating a virtualenv
Before running or deploying this application, install `virtualenv`.  The step is optional but it helps manage your python dependencies.  More information is [here](https://virtualenv.pypa.io/en/stable/installation/)

    virtualenv env
    source env/bin/activate

If everything worked you will see `(env)` before your command prompt, e.g. 

    (env) user@vm4156:~/coms4156_jumpstart

Everytime you want to work on your Flask application, you will need to run `source env/bin/activate`.  When you done working on the app you run `deactivate`.

#### Python Dependencies
Before running or deploying this application, install the dependencies using [pip](http://pip.readthedocs.io/en/stable/):
 
    pip install -r requirements.txt

Check that Flask is listed
    
    pip list

    apiclient (1.0.3)
    appdirs (1.4.3)
    cachetools (2.0.0)
    click (6.7)
    dill (0.2.6)
    enum34 (1.1.6)
    Flask (0.12.1)
    future (0.16.0)
    futures (3.1.1)
    gapic-google-cloud-datastore-v1 (0.15.3)
    google-auth (1.0.0)
    google-auth-httplib2 (0.0.2)
    google-cloud-core (0.24.1)
    google-cloud-datastore (1.0.0)
    google-gax (0.15.11)
    googleapis-common-protos (1.5.2)
    grpcio (1.3.0)
    httplib2 (0.10.3)
    itsdangerous (0.24)
    Jinja2 (2.9.6)
    MarkupSafe (1.0)
    oauth2client (3.0.0)
    packaging (16.8)
    pip (9.0.1)
    ply (3.8)
    proto-google-cloud-datastore-v1 (0.90.4)
    protobuf (3.3.0)
    pyasn1 (0.2.3)
    pyasn1-modules (0.0.8)
    pyparsing (2.2.0)
    requests (2.13.0)
    rsa (3.4.2)
    setuptools (35.0.2)
    six (1.10.0)
    urllib3 (1.21.1)
    Werkzeug (0.12.1)
    wheel (0.29.0)

`requirements.txt` holds a list of all Python dependencies.  If later you add additional python packages, you need update the file.  The shorthand for doing this is `pip freeze > requirements.txt`.  Both Google Cloud and Travis CI use `requirements.txt`.

#### Test the local environment
Run the Flask application 
    
    export FLASK_APP=imhere/imhere.py
    flask run --host=0.0.0.0 --port=4156

Navigate to the local web site at [http://127.0.0.1:4156/](http://127.0.0.1:4156/) in you virtual machine.  (Click on the mouse icon and then select web browser.)

We created a script to run the above two lines, `./flask_start.sh`.

Congratulations! You have a webapp up and running, but it won't really work without Google Cloud. :(
