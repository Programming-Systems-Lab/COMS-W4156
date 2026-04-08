The application presented to you is functional but minimalistic. Below are some ideas to get you started in thinking about how the barebones application can be extended.

### App-specific suggestions
- Enhance the class page such that teachers can add more information about their course. Be able to modify this page in the future, and allow students to view this page in their own interface.
- Allow classes to have TA's, which teachers can add and which have the same permissions as a teacher. Potentially have different sets of permissions that can be granted to different TA's.
- Add customization to the secret code that is generated with each sign-in window. Allow a teacher to create their own code, or even create no code at all which just requires students to hit a sign-in button as opposed to entering a code and signing in.
- Add ability to set a custom expiration datetime for each session. Currently the session expiration is defaulted to 24 hours after opening.
- Display more information to teachers and students about attendance records. When did they happen, which ones were attended/missed? 
- Allow teachers to modify attendance records directly inside the app.
- Create a communication portal for students and teachers to communicate with one another. This could allow students to request an attendance record to be approved/dropped.
- Allow teachers to import students through csv files instead of adding them individually. 

### General app suggestions
- Theme the app in such a way that it is applicable to a more specific use case than general attendance-taking. Add features that apply to your new domain.
- Pair attendance-taking with a new functionality, and allow these two functionalities to communicate with each other inside your app. *Think of all the features within Courseworks
- Use some javascript/CSS in your app to make it appear more modern. (This will require more research and may be hack-y in a way. [This source may be useful](https://realpython.com/blog/python/flask-by-example-integrating-flask-and-angularjs/).)
- Change the structure of teacher/student separation. Implement a new design which will better suit the cases of having teacher-only, student-only, and dual teacher/student accounts.
- Optimize the way communication is handled with the Google datastore.