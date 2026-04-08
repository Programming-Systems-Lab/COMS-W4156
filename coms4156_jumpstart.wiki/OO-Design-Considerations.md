## General notes on our design

Our class diagrams reflect our conceptual view of the system, and how it should be to follow general OO principles. The existing implementation may deviate slightly in some places.



## Open-closed principle (OCP)

The TA role is a modified Student, with some Teacher-like capabilities. Accordingly, the TA class is a subclass of Student.

Adding the attendance record editing feature does not change any existing responsibilities of Teacher, only adding incremental ones. This is equivalent to adding a new EditingTeacher subclass of Teacher. Since all Teacher's will have this new responsibility, this is equivalent to setting the original Teacher class to be an abstract class.


## Don’t Repeat Yourself principle (DRY)

We chose to violate DRY with regards to the TA Teacher-like capabilities in favor of adhering to OCP and LSP. The TA class should have full inheritance from the Student class, but only some from Teacher. While we could have adhered to DRY by creating a new abstract class with the joint Teacher & TA responsibilities, from which Teacher & TA would both inherit, this would necessarily violate OCP with regards to the Teacher class. Additionally, TA would then have dual inheritance, which seems to violate some interpretations of LSP.

The new attendance edit feature will be constrained to a single class.


## Single Responsibility Principle (SRP)

We ensure all new capabilities are consistent with SRP for their respective classes.

The original implementation seems to violate SRP in a few places, such as "The Student get_secret_and_seid itself" and "The Student insert_attendance_record itself". Both seem like actions the Course class should take.



## Liskov Substitution Principle (LSP)

We ensure TA should and can perform all capabilities of Student, our only strict new subtype.

The same is conceptually true for EditingTeacher and Teacher.