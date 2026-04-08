ImHere is an attendance-taking application that was created in Prof. Kaiser's 4156 class (Fall 2016). The application prepared for you is a stripped-down, simplistic version of ImHere. Below, we discuss the interface and structure of the modified ImHere.

ImHere was designed to be used in a classroom setting. As such, we categorize our users as either teachers or students. Teachers own a list of classes in which students may be enrolled. Teachers initialize the sign-in process, which students must then take part in, and then teachers terminate that process. Each of the steps of the application are discussed below in more detail.

## Interface

The central idea behind ImHere is that teacher and student interfaces are kept separate and are independent of each other. On both the student and teacher main pages, there is a link to switch to the other account type. If that account has not yet been created, the user will be redirected to the registration page.


### Registration
The application makes use of Google's oauth2 to sign-in and use the application. As such, it is therefore easy to use a Columbia email (and even possible to restrict the application to use only Columbia emails). Upon registration, a user may sign up as a teacher or student account (or even both). Each type of account has a different set of privileges.


### Teacher 
A teacher account is required to create classes and take attendance. The teacher interface will list all the classes being taught by that user. Below each class is an 'open window' button, which will open an attendance window for that class. When a window is opened, a randomly generated code is presented which the students must use to sign into the class. Any time thereafter, the teacher has access to a 'close window' button which will then close that window.

Each class has a 'class page' which can visited by clicking on the class links on the teacher home page. Each class page allows you to add a student to that class, as well as offering the open/close window capability. When students are in the class, students may then be deleted from the class. A roster is presented with each student's name, e-mail, uni, and attendance record.

To add a class, go to the teacher home page and click on 'add a class'. It is also possible to remove classes if at least one class is being taught.


### Student
A student account is required to sign into classes. Each student account has a uni associated with it, which is requested during registration. On the contrary, teachers are not associated with unis.

A student's home page lists all the classes that that student is registered in. To be added into a class, a teacher must supply the uni of the student into their class. Students are unable to add themselves to classes.

When a class has no sign-in window available, the student will not be able to do anything on their homepage. When a sign-in window is available, the student must enter the correct code into the sign-in box and then hit 'submit'. The form is protected against multiple sign-ins/refreshes/bad behavior.


## Structure

ImHere uses the [Flask python microframework](http://flask.pocoo.org/) which is based on [Werkzeug](http://werkzeug.pocoo.org/) and [Jinja2](http://jinja.pocoo.org/docs/2.9/).

Google's oauth2 sign-in uses a 'client secrets' json file to authorize access to Google's API. A Google account must be setup for authorization (this should be done with the devops account). A guide to setting up the oauth2 can be found [here](https://github.com/keirl/coms4156_jumpstart/wiki/google-oauth2).

Persistent data, such as user account, classes, attendance records/sessions, etc. are stored in the Google datastore. ImHere makes calls to the datastore via the 'models' module. Results are parsed in the app-route functions in imhere.py, and thrown to respective html templates where they are formatted with Jinja2.
