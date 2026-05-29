"""
RW EduPlatform – Seed Script
Run: python seed.py (from backend directory, with virtualenv active)
Creates demo institution, admin, teacher, student accounts + sample data.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduplatform.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.utils import timezone
from users.models  import User, Institution, StudentProfile, TeacherProfile
from courses.models import Department, Course
from notices.models import Notice
from fees.models    import FeeCategory, FeeStructure
from exams.models   import Exam, Question, Choice
import datetime

print("🌱 Seeding RW EduPlatform database…\n")

# ── Institution ─────────────────────────────────────────────────────────────
inst, _ = Institution.objects.get_or_create(
    code='DEMO001',
    defaults={
        'name':    'Demo School of Excellence',
        'address': 'Coimbatore, Tamil Nadu, India',
        'phone':   '+91-422-0000000',
        'email':   'admin@demo-school.edu',
    }
)
print(f"✅ Institution: {inst.name}")

# ── Admin ────────────────────────────────────────────────────────────────────
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email':       'admin@rwplatform.com',
        'first_name':  'Admin',
        'last_name':   'RW',
        'role':        'admin',
        'institution': inst,
        'is_staff':    True,
        'is_superuser':True,
        'is_verified': True,
    }
)
if created:
    admin.set_password('Admin@1234')
    admin.save()
print(f"✅ Admin: admin / Admin@1234")

# ── Teacher ──────────────────────────────────────────────────────────────────
teacher, created = User.objects.get_or_create(
    username='teacher1',
    defaults={
        'email':       'teacher1@rwplatform.com',
        'first_name':  'Priya',
        'last_name':   'Sharma',
        'role':        'teacher',
        'institution': inst,
        'is_verified': True,
    }
)
if created:
    teacher.set_password('Teacher@1234')
    teacher.save()
    TeacherProfile.objects.create(
        user=teacher,
        employee_id='TCH001',
        department='Computer Science',
        designation='Senior Lecturer',
        joining_date=datetime.date(2022, 6, 1),
    )
print(f"✅ Teacher: teacher1 / Teacher@1234")

# ── Students ─────────────────────────────────────────────────────────────────
students = []
student_data = [
    ('student1', 'Arjun',   'Kumar',  'STU001'),
    ('student2', 'Meera',   'Nair',   'STU002'),
    ('student3', 'Rahul',   'Verma',  'STU003'),
]
for username, fname, lname, roll in student_data:
    s, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email':       f'{username}@rwplatform.com',
            'first_name':  fname,
            'last_name':   lname,
            'role':        'student',
            'institution': inst,
            'is_verified': True,
        }
    )
    if created:
        s.set_password('Student@1234')
        s.save()
        StudentProfile.objects.create(
            user=s,
            roll_number=roll,
            admission_date=datetime.date(2023, 7, 1),
        )
    students.append(s)
print(f"✅ Students: student1/student2/student3 – password: Student@1234")

# ── Department & Course ───────────────────────────────────────────────────────
dept, _ = Department.objects.get_or_create(
    institution=inst, code='CS',
    defaults={'name': 'Computer Science'}
)
course, _ = Course.objects.get_or_create(
    institution=inst, code='CS101',
    defaults={
        'name':        'Introduction to Python',
        'description': 'Basics of Python programming for beginners.',
        'teacher':     teacher,
        'department':  dept,
        'is_active':   True,
        'start_date':  datetime.date(2024, 1, 1),
        'end_date':    datetime.date(2024, 12, 31),
    }
)
for s in students:
    course.students.add(s)
print(f"✅ Course: {course.name} with {len(students)} students")

# ── Notice ────────────────────────────────────────────────────────────────────
Notice.objects.get_or_create(
    institution=inst,
    title='Welcome to RW EduPlatform!',
    defaults={
        'content':          'This is your new educational management platform. Explore all features!',
        'priority':         'high',
        'target_audience':  'all',
        'published_by':     admin,
        'is_published':     True,
    }
)
print(f"✅ Notice created")

# ── Fee Category & Structure ──────────────────────────────────────────────────
cat, _ = FeeCategory.objects.get_or_create(
    institution=inst, name='Tuition Fee',
    defaults={'description': 'Semester tuition fee'}
)
FeeStructure.objects.get_or_create(
    institution=inst, category=cat, academic_year='2024-25',
    defaults={
        'amount':   25000,
        'due_date': datetime.date(2024, 7, 31),
        'is_active':True,
    }
)
print(f"✅ Fee structure created")

# ── Sample Exam ───────────────────────────────────────────────────────────────
exam, _ = Exam.objects.get_or_create(
    institution=inst, title='Python Basics Quiz',
    defaults={
        'course':            course,
        'description':       'Test your knowledge of Python fundamentals.',
        'duration_mins':     30,
        'total_marks':       10,
        'pass_marks':        6,
        'status':            'published',
        'show_result_immediately': True,
        'created_by':        teacher,
    }
)
if not exam.questions.exists():
    q1 = Question.objects.create(exam=exam, text='What is the output of print(2**3)?', question_type='mcq', marks=2, order=1)
    Choice.objects.create(question=q1, text='6',  is_correct=False)
    Choice.objects.create(question=q1, text='8',  is_correct=True)
    Choice.objects.create(question=q1, text='9',  is_correct=False)
    Choice.objects.create(question=q1, text='16', is_correct=False)

    q2 = Question.objects.create(exam=exam, text='Python is a compiled language.', question_type='truefalse', marks=1, order=2)
    Choice.objects.create(question=q2, text='True',  is_correct=False)
    Choice.objects.create(question=q2, text='False', is_correct=True)

    q3 = Question.objects.create(exam=exam, text='Which keyword is used to define a function in Python?', question_type='mcq', marks=2, order=3)
    Choice.objects.create(question=q3, text='func',   is_correct=False)
    Choice.objects.create(question=q3, text='define', is_correct=False)
    Choice.objects.create(question=q3, text='def',    is_correct=True)
    Choice.objects.create(question=q3, text='function',is_correct=False)
print(f"✅ Sample exam with questions created")

print("\n🎉 Seeding complete! You can now log in at http://localhost/admin or via the API.")
print("\nCredentials summary:")
print("  Admin:   admin        / Admin@1234")
print("  Teacher: teacher1     / Teacher@1234")
print("  Student: student1/2/3 / Student@1234")
