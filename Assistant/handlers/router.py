# Assistant/handlers/router.py
from Assistant.handlers.intent_router import identify_intent
from Assistant.handlers import student_analysis, teacher_analysis, hod_analysis
from users.models import StudentProfile, TeacherProfile, HodProfile
from Assistant.handlers.student_analysis import get_student_attendance_summary

def get_user_role(user):
    if StudentProfile.objects.filter(user=user).exists():
        return "student"
    elif TeacherProfile.objects.filter(user=user).exists():
        return "teacher"
    elif HodProfile.objects.filter(user=user).exists():
        return "hod"
    return "unknown"

def route_query(user_input, user=None):
    role = get_user_role(user)
    intent = identify_intent(user_input)

    # Student Routes
    if role == "student":
        if intent == "get_progress":
            return student_analysis.get_student_progress(user)
        elif intent == "get_advice":
            return student_analysis.get_improvement_advice(user)
        elif intent == "get_attendance":
            return get_student_attendance_summary(user)

    # Teacher Routes
    elif role == "teacher":
        if intent == "teacher_progress":
            return teacher_analysis.get_teacher_performance(user)
        elif intent == "teacher_advice":
            return teacher_analysis.get_teacher_advice(user)
        elif intent == "teacher_attendance":
            return teacher_analysis.get_teacher_attendance_summary(user)

    # HOD Routes
    elif role == "hod":
        if intent == "hod_progress":
            return hod_analysis.get_hod_performance(user)
        elif intent == "hod_advice":
            return hod_analysis.get_hod_advice(user)
        elif intent == "hod_attendance":
            return hod_analysis.get_hod_attendance_summary(user)


    return {"message": "Sorry, I couldn't understand your request."}
