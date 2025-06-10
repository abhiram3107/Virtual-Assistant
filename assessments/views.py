# assessments/views/performance.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from assessments.models import TestResult
from users.models import StudentProfile

@api_view(['GET'])
def performance_analysis(request, student_id):
    try:
        student = StudentProfile.objects.get(id=student_id)
    except StudentProfile.DoesNotExist:
        return Response({"error": "Student not found"}, status=404)

    data = TestResult.get_performance_summary(student)
    return Response(data)
