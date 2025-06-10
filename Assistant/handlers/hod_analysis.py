# analysis/hod_analysis.py


from users.models import HodProfile, TeacherProfile, StudentProfile
from assessments.models import TestResult
from collections import defaultdict
from attendence.models import Attendance

def get_hod_performance(user):
    try:
        hod = HodProfile.objects.get(user=user)
    except HodProfile.DoesNotExist:
        return {"error": "HOD profile not found."}

    department = hod.department

    # Step 1: Get all teachers and students in this department
    teachers = TeacherProfile.objects.filter(department=department)
    students = StudentProfile.objects.filter(department=department)

    # Step 2: Get all subjects taught by these teachers
    subjects = set()
    for teacher in teachers:
        subjects.update(teacher.subjects.all())

    # Step 3: Get all test results written by students in this department for those subjects
    test_results = TestResult.objects.filter(
        student__in=students,
        test__subject__in=subjects
    )

    # Subject performance tracking
    subject_scores = defaultdict(lambda: {"scored": 0, "total": 0, "count": 0})

    for result in test_results:
        subject = result.test.subject.name
        subject_scores[subject]["scored"] += result.marks_obtained
        subject_scores[subject]["total"] += result.test.max_marks
        subject_scores[subject]["count"] += 1

    # Step 4: Prepare subject performance analysis
    department_performance = {
        subject: {
            "accuracy": round((data["scored"] / data["total"]) * 100, 2) if data["total"] else 0,
            "tests_taken": data["count"]
        }
        for subject, data in subject_scores.items()
    }

    # Teacher performance analysis
    teacher_performance = {}
    for teacher in teachers:
        teacher_subject_scores = defaultdict(lambda: {"scored": 0, "total": 0, "count": 0})

        # Step 5: For each teacher, get the test results of their subjects
        for subject in teacher.subjects.all():
            teacher_test_results = TestResult.objects.filter(test__subject=subject, student__in=students)
            for result in teacher_test_results:
                teacher_subject_scores[subject.name]["scored"] += result.marks_obtained
                teacher_subject_scores[subject.name]["total"] += result.test.max_marks
                teacher_subject_scores[subject.name]["count"] += 1

        # Prepare teacher performance report
        teacher_performance[teacher.teacher_id] = {
            subject: {
                "accuracy": round((data["scored"] / data["total"]) * 100, 2) if data["total"] else 0,
                "tests_taken": data["count"]
            }
            for subject, data in teacher_subject_scores.items()
        }

    return {
        "department": department.name,
        "department_performance": department_performance,
        "teacher_performance": teacher_performance
    }



def get_hod_advice(user):
    performance = get_hod_performance(user)

    if "error" in performance:
        return performance["error"]

    department_advice = []
    # Department performance feedback
    for subject, data in performance["department_performance"].items():
        if data["accuracy"] < 50:
            department_advice.append(f"{subject}: {data['accuracy']}% (Needs Improvement)")
        elif data["accuracy"] >= 70:
            department_advice.append(f"{subject}: {data['accuracy']}% (Good)")
        else:
            department_advice.append(f"{subject}: {data['accuracy']}% (Average)")

    teacher_advice = []
    # Teacher performance feedback
    for teacher_id, teacher_data in performance["teacher_performance"].items():
        for subject, data in teacher_data.items():
            if data["accuracy"] < 50:
                teacher_advice.append(f"Teacher {teacher_id} - {subject}: {data['accuracy']}% (Needs Improvement)")
            elif data["accuracy"] >= 70:
                teacher_advice.append(f"Teacher {teacher_id} - {subject}: {data['accuracy']}% (Good)")
            else:
                teacher_advice.append(f"Teacher {teacher_id} - {subject}: {data['accuracy']}% (Average)")

    # Combine department and teacher advice
    return (
        "Department performance feedback:\n" + "\n".join(department_advice) +
        "\n\nTeacher performance feedback:\n" + "\n".join(teacher_advice)
    )


# New function for attendance analysis
def get_hod_attendance_summary(user):
    try:
        hod = HodProfile.objects.get(user=user)
    except HodProfile.DoesNotExist:
        return {"error": "HOD profile not found."}

    department = hod.department

    # Get all students and teachers in the department
    students = StudentProfile.objects.filter(department=department)
    teachers = TeacherProfile.objects.filter(department=department)

    # Step 1: Get student attendance records for the department
    student_records = Attendance.objects.filter(
        student__department=department,
        student__isnull=False
    ).select_related('student__user', 'subject')

    student_attendance = defaultdict(lambda: {"present": 0, "total": 0})
    for record in student_records:
        key = record.student.user.username
        student_attendance[key]["total"] += 1
        if record.present:
            student_attendance[key]["present"] += 1

    student_summary = [
        f"- {username}: {data['present']} / {data['total']} ({round((data['present'] / data['total']) * 100, 2)}%)"
        for username, data in student_attendance.items() if data["total"] > 0
    ]

    # Step 2: Get teacher attendance records for the department
    teacher_records = Attendance.objects.filter(
        teacher__department=department,
        teacher__isnull=False
    ).select_related('teacher__user', 'subject').distinct()

    teacher_attendance = defaultdict(lambda: {"present": 0, "total": 0})
    for record in teacher_records:
        key = record.teacher.user.username
        teacher_attendance[key]["total"] += 1
        if record.present:
            teacher_attendance[key]["present"] += 1

    teacher_summary = [
        f"- {username}: {data['present']} / {data['total']} ({round((data['present'] / data['total']) * 100, 2)}%)"
        for username, data in teacher_attendance.items() if data["total"] > 0
    ]

    return {
        "student_attendance": student_summary,
        "teacher_attendance": teacher_summary
    }