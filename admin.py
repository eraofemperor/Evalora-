from django.contrib import admin

# Register your models here.
from .models import Student, Subject, AnswerSheet, Evaluation, EvaluationDetail


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(AnswerSheet)
class AnswerSheetAdmin(admin.ModelAdmin):
    list_display = ("rollno", "subject", "uploaded_at")


class EvaluationDetailInline(admin.TabularInline):
    model = EvaluationDetail
    extra = 0


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("answer_sheet", "total_marks", "created_at")
    inlines = [EvaluationDetailInline]

