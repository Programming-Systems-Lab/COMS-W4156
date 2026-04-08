# COMS W4156 Individual Assignment 1

For this assignment you will be building a very simple HTTP REST API that returns information about the amount of garbage collected throughout New York City during September 2011.
This data is provided through [NYC Open Data](https://data.cityofnewyork.us/Environment/DSNY-Collection-Tonnages/ewtv-wftx) and can be accessed using the Socrata Open Data (SODA) API using resource key `ewtv-wftx`.
Your API will need to answer four questions:

* How many tons of refuse were collected during the month in a given burough and community district?
    * `/refuse/<burough>/<community district>/`
* How many tons of paper were collected during the month in a given burough and community district?
    * `/paper/<burough>/<community district>/`
* How many tons of metal, glass, and plastic (MGP) were collected during the month in a given burough and community district?
    * `/mgp/<burough>/<community district>/`
* What is the total amount garbage, refuse + paper + MGP, collected during the month for the community districts that have been queried.
    * `/total/`

## Technical Requirements
* You are required to use implement your API using [Java Play 2.3.4](http://www.playframework.com/).
    * This requires Java 7. If you see the error ` Unsupported major.minor version 51.0` then you are using a version of java tht is too old.
* You should use the routes file in this repository for your project.
* To answer question 4 you must record each call to the API.
You should log this in a database. You may use SQLite or an in memory database such as H2.
* Your application should handle invalid data such as a community district that does not exist by returning `0`.
* You may use external libraries and they should be included in your deliverable as a managed or unmanaged dependency.
    * Suggestion: `https://github.com/socrata/soda-java`
* We suggest that you use the simple socrata [filter queries](http://dev.socrata.com/docs/filtering.html)
    * To find information about community district 3 in Manhattan you can use the following URL: `http://data.cityofnewyork.us/resource/ewtv-wftx\?communitydistrict\=3\&borough\=Manhattan`
* The python script in this repository will let you test your project.
The data included will not be the data we use to test the project.
Note that this is the script but not the same data that we will use to test your projects.
This will allow you to easily test your projects.
* The burough will be `brooklyn`, `manhattan`, `bronx`, `queens`, or `statenisland`
* You may not predownload any data. Doing so will result in failure.
* In the event of any error return `0`.

## Grading
Students will fall into one of 3 categories: pass, borderline, or fail.
Students passing the assignment will be allowed to enroll in the class.
Students in the borderline category will be allowed to enroll in the class if there is room after all passing students have enrolled.
Students failing the assignment will not be allowed to enroll in the class.
We will have a higher passing standard for those wishing to waive the class and there is no borderline for waiver students.

* Score >= 95% - Waiver Pass
* Score >= 90% - Class Pass
* 90 > Score >= 80 - Class Borderline
* 80 > Score - Class Fail

## Submission
In class students will submit the assignment through CourseWorks.
Waiver students will submit via email to the TA.

## Waiver Specific Instructions (Not Class Students)
Students that have previously taken a software engineering class may be allowed to waive the class.
Students wishing to waive the class have two extra deliverables in addition to the programming assignment.
You must submit unit tests and corresponding test coverage metrics for this assignment, and you must submit structural and behavioral diagrams of your design.

## Note for Students with Industry Experience
Students with sufficient documented industrial software engineering experience, but no prior formal software engineering course for the waiver, will be allowed to count COMS W6123 (Programming Environments and Software Tools), offered in Spring 2015, towards the software systems track requirements in lieu of 4156 if they achieve a B+ or higher in 6123.
These students must also complete the waiver version of this preliminary assignment.


