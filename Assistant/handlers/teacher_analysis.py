# analysis/teacher_analysis.py

from users.models import TeacherProfile
from assessments.models import TestResult
from collections import defaultdict

def get_teacher_performance(user):
    try:
        teacher = TeacherProfile.objects.get(user=user)
    except TeacherProfile.DoesNotExist:
        return {"error": "Teacher profile not found."}

    subjects = teacher.subjects.all()
    analysis = {}

    for subject in subjects:
        test_results = TestResult.objects.filter(test__subject=subject).select_related('student__user')
        chapter_scores = defaultdict(lambda: {"scored": 0, "total": 0})
        student_scores = defaultdict(lambda: {"scored": 0, "total": 0})

        max_marks = None
        min_marks = None

        for result in test_results:
            chapter_title = result.test.chapter.title if result.test.chapter else "No Chapter"
            chapter_scores[chapter_title]["scored"] += result.marks_obtained
            chapter_scores[chapter_title]["total"] += result.test.max_marks

            if max_marks is None or result.marks_obtained > max_marks:
                max_marks = result.marks_obtained
            if min_marks is None or result.marks_obtained < min_marks:
                min_marks = result.marks_obtained

            username = result.student.user.username
            student_scores[username]["scored"] += result.marks_obtained
            student_scores[username]["total"] += result.test.max_marks

        chapter_info = []
        for chapter, data in chapter_scores.items():
            accuracy = round((data["scored"] / data["total"]) * 100, 2) if data["total"] else 0
            chapter_info.append(f"- {chapter}: {accuracy}% accuracy")

        student_info = []
        for username, scores in student_scores.items():
            if scores["total"] == 0:
                continue
            accuracy = round((scores["scored"] / scores["total"]) * 100, 2)
            student_info.append(f"- {username}: {scores['scored']} / {scores['total']} ({accuracy}%)")

        if not chapter_info and not student_info:
            analysis[subject.name] = f"📘 Subject: {subject.name}\n⚠️ No test results available."
        else:
            analysis[subject.name] = (
                f"📘 Subject: {subject.name}\n"
                f"🔺 Highest Marks: {max_marks if max_marks is not None else 0}\n"
                f"🔻 Lowest Marks: {min_marks if min_marks is not None else 0}\n\n"
                f"📊 Chapter-wise Performance:\n" + "\n".join(chapter_info) + "\n\n"
                f"👥 Student Performance:\n" + "\n".join(student_info)
            )

    return analysis





def get_teacher_advice(user):
    analysis = get_teacher_performance(user)
    if "error" in analysis:
        return analysis["error"]

    advice = []
    for subject, data in analysis.items():
        chapters = data["chapters"]
        max_marks = data["max_marks_obtained"]
        min_marks = data["min_marks_obtained"]
        student_scores = data["student_scores"]

        # Determine top/weak students here
        top_students = []
        weak_students = []
        for username, scores in student_scores.items():
            if scores["total"] == 0:
                continue
            accuracy = (scores["scored"] / scores["total"]) * 100
            if accuracy >= 75:
                top_students.append(f"{username} ({round(accuracy, 2)}%)")
            elif accuracy < 40:
                weak_students.append(f"{username} ({round(accuracy, 2)}%)")

        weak_chapters = [f"{chapter} ({info['accuracy']}%)"
                         for chapter, info in chapters.items() if info["accuracy"] < 50]
        strong_chapters = [f"{chapter} ({info['accuracy']}%)"
                           for chapter, info in chapters.items() if info["accuracy"] >= 70]

        subject_feedback = [f"📘 **{subject}**"]
        subject_feedback.append(f"🔺 Highest Marks Obtained: {max_marks}")
        subject_feedback.append(f"🔻 Lowest Marks Obtained: {min_marks}")

        if strong_chapters:
            subject_feedback.append("✔️ Students are performing well in the following chapters:")
            subject_feedback.extend([f"  - {chapter}" for chapter in strong_chapters])

        if weak_chapters:
            subject_feedback.append("⚠️ These chapters may require additional focus or revision:")
            subject_feedback.extend([f"  - {chapter}" for chapter in weak_chapters])

        if top_students:
            subject_feedback.append("🏆 Top-performing students:")
            subject_feedback.extend([f"  - {student}" for student in top_students])

        if weak_students:
            subject_feedback.append("🔻 Students needing attention:")
            subject_feedback.extend([f"  - {student}" for student in weak_students])

        advice.append("\n".join(subject_feedback))

    return "\n\n".join(advice)

from attendence.models import Attendance
from collections import defaultdict

def get_teacher_attendance_summary(user):
    try:
        teacher = TeacherProfile.objects.get(user=user)
    except TeacherProfile.DoesNotExist:
        return "You are not registered as a teacher."

    subjects = teacher.subjects.all()
    if not subjects:
        return "You are not assigned to any subjects."

    summary = {}

    for subject in subjects:
        records = Attendance.objects.filter(subject=subject, teacher=teacher, student__isnull=False)

        if not records.exists():
            summary[subject.name] = "⚠️ No attendance records available."
            continue

        total_sessions = records.values("date").distinct().count()

        student_attendance = defaultdict(int)
        for record in records:
            if record.present:
                student_attendance[record.student.user.username] += 1

        student_summary = [
            f"- {username}: {present}/{total_sessions} ({round((present/total_sessions)*100, 2)}%)"
            for username, present in student_attendance.items()
        ]

        summary[subject.name] = (
            f"📘 Subject: {subject.name}\n"
            f"📅 Sessions Conducted: {total_sessions}\n"
            f"👥 Student Attendance:\n" + "\n".join(student_summary)
        )

    return summary
