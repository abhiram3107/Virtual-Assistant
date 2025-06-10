from assessments.models.test_result import get_performance_summary  # ✅ import the function

def get_student_progress(user):
    if not hasattr(user, "student_profile"):
        return "You are not registered as a student."

    summary = get_performance_summary(user.student_profile)
    result = []

    good_performance = []
    improvement_needed = []

    # Subject-wise performance
    for subject, data in summary["subject_performance"].items():
        if all(key in data for key in ['accuracy', 'scored', 'total']):
            result.append(f"{subject}: {data['accuracy']}% ({data['scored']}/{data['total']})")
        else:
            result.append(f"{subject}: Data missing or incomplete")
        
        # Add performance feedback
        if data['accuracy'] >= 70:
            good_performance.append(f"{subject}: {data['accuracy']}% (Good)")
        elif data['accuracy'] < 50:
            improvement_needed.append(f"{subject}: {data['accuracy']}% (Needs Improvement)")

    performance_feedback = []
    if good_performance:
        performance_feedback.append("You are performing well in the following subjects:\n" + "\n".join(good_performance))
    if improvement_needed:
        performance_feedback.append("You need to improve in the following subjects:\n" + "\n".join(improvement_needed))

    return "Your subject-wise performance:\n" + "\n".join(result) + "\n\n" + "\n".join(performance_feedback)


def get_improvement_advice(user):
    if not hasattr(user, "student_profile"):
        return "You are not registered as a student."

    summary = get_performance_summary(user.student_profile)  # ✅ correct call
    
    # For subjects, chapters, and topics below 50% accuracy, suggest improvements
    low_performance_subjects = {
        k: v for k, v in summary["subject_performance"].items() if v["accuracy"] < 50
    }
    low_performance_chapters = {
        k: v for k, v in summary["chapter_performance"].items() if v["accuracy"] < 50
    }
    low_performance_topics = {
        k: v for k, v in summary["topic_performance"].items() if v["accuracy"] < 50
    }

    improvement_advice = []

    # Suggest improvement for low-performing subjects
    if low_performance_subjects:
        improvement_advice.append("You need to improve in the following subjects:\n" + "\n".join([f"{k}: {v['accuracy']}%" for k, v in low_performance_subjects.items()]))
    else:
        improvement_advice.append("You're doing well in all subjects!")

    # Suggest improvement for low-performing chapters
    if low_performance_chapters:
        improvement_advice.append("You need to improve in the following chapters:\n" + "\n".join([f"{k}: {v['accuracy']}%" for k, v in low_performance_chapters.items()]))
    else:
        improvement_advice.append("You're doing well in all chapters!")

    # Suggest improvement for low-performing topics
    if low_performance_topics:
        improvement_advice.append("You need to improve in the following topics:\n" + "\n".join([f"{k}: {v['accuracy']}%" for k, v in low_performance_topics.items()]))
    else:
        improvement_advice.append("You're doing well in all topics!")

    return "\n".join(improvement_advice)




from attendence.models import Attendance  # Update this path based on your project
from collections import defaultdict

def get_student_attendance_summary(user):
    if not hasattr(user, "student_profile"):
        return "You are not registered as a student."

    student = user.student_profile
    attendance_records = Attendance.objects.filter(student=student)

    if not attendance_records.exists():
        return "No attendance records found."

    subject_stats = defaultdict(lambda: {"attended": 0, "total": 0})
    overall_attended = 0
    overall_total = 0

    for record in attendance_records:
        subject_name = record.subject.name
        subject_stats[subject_name]["total"] += 1
        overall_total += 1
        if record.present:
            subject_stats[subject_name]["attended"] += 1
            overall_attended += 1

    report_lines = ["📋 Attendance Summary:\n"]
    for subject, stats in subject_stats.items():
        attended = stats["attended"]
        total = stats["total"]
        percentage = round((attended / total) * 100, 2) if total > 0 else 0
        report_lines.append(f"- {subject}: {attended}/{total} classes attended ({percentage}%)")

    overall_percentage = round((overall_attended / overall_total) * 100, 2) if overall_total > 0 else 0
    report_lines.append(f"\n🧮 Overall Attendance: {overall_attended}/{overall_total} ({overall_percentage}%)")

    return "\n".join(report_lines)
