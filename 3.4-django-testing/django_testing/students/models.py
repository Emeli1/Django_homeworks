from django.db import models
from django.core.exceptions import ValidationError

MAX_STUDENTS_PER_COURSE = 20


class Student(models.Model):

    name = models.TextField()

    birth_date = models.DateField(
        null=True,
    )


class Course(models.Model):

    name = models.TextField()

    students = models.ManyToManyField(
        Student,
        blank=True,
    )

    def clean(self):
        if self.students.count() > MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f'Cannot add more than {MAX_STUDENTS_PER_COURSE} students to a course.')
