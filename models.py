from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class AnswerSheet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    rollno = models.CharField(max_length=20)
    file = models.FileField(upload_to="answersheets/", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # show file name + roll number + subject
        file_name = self.file.name.split('/')[-1] if self.file else "No file"
        return f"{file_name} ({self.rollno} - {self.subject.name})"


class Evaluation(models.Model):
    answer_sheet = models.ForeignKey(AnswerSheet, on_delete=models.CASCADE)
    evaluator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Eval: {self.answer_sheet} - Marks: {self.total_marks}"

class EvaluationDetail(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="details")
    question_number = models.IntegerField()
    mark = models.FloatField(default=0)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Q{self.question_number}: {self.mark} marks"
