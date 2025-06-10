import os
import django
import random
from faker import Faker
from django.db import models

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VA.settings")
django.setup()

from users.models import User, StudentProfile, TeacherProfile, HodProfile
from program.models import Program, Subject, Chapter, Topic
from assessments.models import Test, TestResult

fake = Faker()

ROLE_PREFIX = {
    'student': 'STU',
    'teacher': 'TCH',
    'hod': 'HOD',
}

id_counters = {
    'student': 1,
    'teacher': 1,
    'hod': 1,
}

def generate_user(role):
    count = id_counters[role]
    username = f"{role}{count:03d}"
    email = f"{username}@example.com"
    user = User.objects.create(username=username, email=email, role=role)
    id_counters[role] += 1
    return user

def create_programs(n=5):
    program_names = ["B.Tech Computer Science", "B.Sc Physics", "B.A Economics", "B.Com Finance", "BCA"]
    programs = []
    for name in program_names[:n]:
        prog = Program.objects.create(
            name=name,
            institution=fake.company(),
            duration_years=random.randint(3, 5)
        )
        programs.append(prog)
    return programs

def create_subjects(programs, subjects_per_program=3):
    subjects = []
    for prog in programs:
        for i in range(subjects_per_program):
            sub = Subject.objects.create(
                program=prog,
                name=fake.job()[:25],
                semester=random.randint(1, 8)
            )
            subjects.append(sub)
    return subjects

def create_chapters(subjects):
    chapters = []
    for sub in subjects:
        for i in range(1, 4):
            chap = Chapter.objects.create(
                subject=sub,
                title=f"Chapter {i} of {sub.name}",
                order=i
            )
            chapters.append(chap)
    return chapters

def create_topics(chapters):
    topics = []
    for chap in chapters:
        for i in range(1, 3):
            top = Topic.objects.create(
                chapter=chap,
                title=f"Topic {i} of {chap.title}",
                order=i
            )
            topics.append(top)
    return topics

def create_students(programs, count=10):
    students = []
    for _ in range(count):
        user = generate_user('student')
        program = random.choice(programs)
        semester = random.randint(1, 8)
        stud_id = f"STU{user.id:03d}"
        profile = StudentProfile.objects.create(
            user=user,
            student_id=stud_id,
            program=program,
            semester=semester,
            year=1  # will be set by save()
        )
        students.append(profile)
    return students

def create_teachers(subjects, count=5):
    teachers = []
    for _ in range(count):
        user = generate_user('teacher')
        tch_id = f"TCH{user.id:03d}"
        profile = TeacherProfile.objects.create(user=user, teacher_id=tch_id)
        profile.subjects.set(random.sample(subjects, k=min(2, len(subjects))))
        teachers.append(profile)
    return teachers

def create_hods(count=3):
    hods = []
    departments = ["CSE", "ECE", "EEE", "Civil", "IT"]
    for i in range(count):
        user = generate_user('hod')
        hod_id = f"HOD{user.id:03d}"
        profile = HodProfile.objects.create(
            user=user,
            hod_id=hod_id,
            department=random.choice(departments)
        )
        hods.append(profile)
    return hods

def create_tests(subjects, chapters, topics, count=15):
    tests = []
    for _ in range(count):
        subject = random.choice(subjects)
        chapter = random.choice([c for c in chapters if c.subject == subject])
        topic = random.choice([t for t in topics if t.chapter == chapter])
        test = Test.objects.create(
            subject=subject,
            chapter=chapter,
            topic=topic,
            name=f"Test on {topic.title}",
            max_marks=random.choice([50, 75, 100]),
            date=fake.date_this_year()
        )
        tests.append(test)
    return tests

def create_results(students, tests):
    for student in students:
        for test in random.sample(tests, k=5):
            marks = random.randint(0, test.max_marks)
            TestResult.objects.create(
                student=student,
                test=test,
                marks_obtained=marks
            )

def populate():
    print("🚀 Starting mock data generation...")

    programs = create_programs()
    print("✅ Programs created")

    subjects = create_subjects(programs)
    print("✅ Subjects created")

    chapters = create_chapters(subjects)
    print("✅ Chapters created")

    topics = create_topics(chapters)
    print("✅ Topics created")

    students = create_students(programs)
    print("✅ Students created")

    teachers = create_teachers(subjects)
    print("✅ Teachers created")

    hods = create_hods()
    print("✅ HODs created")

    tests = create_tests(subjects, chapters, topics)
    print("✅ Tests created")

    create_results(students, tests)
    print("✅ Test results created")

    print("\n🎉 Data population complete!")

if __name__ == "__main__":
    populate()
