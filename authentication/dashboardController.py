from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Attendance, TblStudents, Classroom
from django.http import JsonResponse
from .models import TblStudents
from django.db.models import Count
# from .forms import StudentForm
from .forms import TblStudentsForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# def demo(request):
#     students = TblStudents.objects.all()
#     return render(request, "admin/student.html", {'students': students})

# def add_student(request):
#     if request.method == 'POST':
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('demo')
#     else:
#         form = StudentForm()
#     return render(request, 'admin/add_student.html', {'form': form})

# def update_student(request, student_id):
#     student = get_object_or_404(TblStudents, student_id=student_id)
#     if request.method == 'POST':
#         form = StudentForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             return redirect('demo')
#     else:
#         form = StudentForm(instance=student)
#     return render(request, 'admin/update_student.html', {'form': form, 'student': student})

# def delete_student(request, student_id):
#     student = get_object_or_404(TblStudents, student_id=student_id)
#     if request.method == 'POST':
#         student.delete()
#         return redirect('demo')
#     return render(request, 'admin/delete_student.html', {'student': student})

# def demo(request):
#     search_query = request.GET.get('q', '')
#     if search_query:
#         students = TblStudents.objects.filter(
#             Q(name__icontains=search_query) |
#             Q(email__icontains=search_query) |
#             Q(phone__icontains=search_query) |
#             Q(student_id__icontains=search_query)
#         )
#     else:
#         students = TblStudents.objects.all()
#     return render(request, "class/classroom_detail.html", {'students': students, 'search_query': search_query})
def classroom_student_list(request, class_id):
    classroom = get_object_or_404(Classroom, class_id=class_id)
    search_query = request.GET.get('q', '')

    if search_query:
        students = TblStudents.objects.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(student_id__icontains=search_query)
        ).filter(classroom=classroom)
    else:
        students = TblStudents.objects.filter(classroom=classroom)
    
    total_students = students.count()

    return render(request, "class/classroom_detail.html", {
        'classroom': classroom,
        'students': students,
        'search_query': search_query,
        'total_students': total_students,
        'class_id': class_id
    })


def data(request):
    # Chuyển đổi QuerySet thành danh sách các từ điển để dễ đọc
    t3 = list(TblStudents.objects.values())

    # Lọc các bản ghi có name bắt đầu bằng "Beatles"
    t4 = list(TblStudents.objects.filter(name__startswith="Beatles").values())

    # Tìm kiếm chính xác
    t5 = list(TblStudents.objects.filter(name="Phong Vu").values())

    # Tìm kiếm một phần
    t6 = list(TblStudents.objects.filter(name__contains="N").values())


    data = {
        "all_students": t3,
        "starts_with_beatles": t4,
        "exact_name_phong_vu": t5,
        "contains_n": t6,
    }
    return JsonResponse(data)

# =======================================================
def classroom_list(request):
    classrooms = Classroom.objects.all()
    return render(request, 'class/classroom_list.html', {'classrooms': classrooms})

def classroom_list_attendance(request):
    classrooms = Classroom.objects.all()
    return render(request, 'attendance/classroom_list.html', {'classrooms': classrooms})

def classroom_detail(request, class_id):
    classroom = get_object_or_404(Classroom, pk=class_id)
    students = classroom.students.all()
    return render(request, 'class/classroom_detail.html', {'classroom': classroom, 'students': students})

# def add_student(request, class_id):
#     classroom = get_object_or_404(Classroom, pk=class_id)
#     if request.method == 'POST':
#         form = TblStudentsForm(request.POST)
#         if form.is_valid():
#             student = form.save(commit=False)
#             student.classroom = classroom
#             student.save()
#             return redirect('class/classroom_detail.html', class_id=class_id)
#     else:
#         form = TblStudentsForm(initial={'classroom': classroom})
#     return render(request, 'class/add_student.html', {'form': form, 'classroom': classroom})





# def add_student(request, class_id):
#     classroom = get_object_or_404(Classroom, pk=class_id)
#     if request.method == 'POST':
#         form = TblStudentsForm(request.POST)
#         if form.is_valid():
#             student = form.save(commit=False)
#             student.classroom = classroom
#             student.save()
#             return redirect('classroom_detail', class_id=class_id)  # Corrected redirect URL name
#     else:
#         form = TblStudentsForm(initial={'classroom': classroom})
#     return render(request, 'class/add_student.html', {'form': form, 'classroom': classroom})


# def delete_student(request, student_id):
#     student = get_object_or_404(TblStudents, student_id=student_id)
#     if request.method == 'POST':
#         student.delete()
#         return redirect('classroom')
#     return render(request, 'class/delete_student.html', {'student': student})

def edit_student(request, student_id):
    student = get_object_or_404(TblStudents, pk=student_id)
    if request.method == 'POST':
        form = TblStudentsForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('classroom_detail', class_id=student.classroom.class_id)
    else:
        form = TblStudentsForm(instance=student)
    return render(request, 'class/edit_student.html', {'form': form, 'student': student})



def add_student(request, class_id):
    classroom = get_object_or_404(Classroom, pk=class_id)
    if request.method == 'POST':
        form = TblStudentsForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom = classroom
            student.save()
            return redirect('classroom_detail', class_id=class_id)  # Corrected redirect URL name
    else:
        form = TblStudentsForm(initial={'classroom': classroom})
    return render(request, 'class/add_student.html', {'form': form, 'classroom': classroom})







# def delete_student(request, student_id):
#     student = get_object_or_404(TblStudents, student_id=student_id)
#     if request.method == 'POST':
#         student.delete()
#         return JsonResponse({'status': 'success', 'message': 'Student deleted successfully.'})
#     return render(request, 'class/delete_student.html', {'student': student})

def delete_student(request, student_id):
    student = get_object_or_404(TblStudents, student_id=student_id)
    if request.method == 'POST':
        student.delete()
        # Fetch the updated list of students
        students = TblStudents.objects.all()
        students_data = list(students.values('student_id', 'name', 'email', 'phone', 'date_birth'))
        return JsonResponse({'status': 'success', 'message': 'Student deleted successfully.', 'students': students_data})
    return render(request, 'class/delete_student.html', {'student': student})


# def classroom_student_list(request, classroom_id):
#     classroom = get_object_or_404(Classroom, id=classroom_id)
#     students = TblStudents.objects.filter(classroom=classroom)
#     total_students = students.count()

#     return render(request, 'class/classroom_detail.html', {
#         'classroom': classroom,
#         'students': students,
#         'total_students': total_students
#     })
def classroom_student_list(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    students = TblStudents.objects.filter(classroom=classroom)
    total_students = students.count()

    return render(request, 'class/classroom_detail.html', {
        'classroom': classroom,
        'students': students,
        'total_students': total_students
    })


# def student_list(request, classroom_id):
#     classroom = get_object_or_404(Classroom, class_id=classroom_id)
#     students = TblStudents.objects.filter(classroom=classroom)
#     total_students = students.count()

#     # Lấy thông tin điểm danh của từng sinh viên trong lớp
#     attendance_records = Attendance.objects.filter(student__in=students)

#     return render(request, 'attendance/attendance.html', {
#         'classroom': classroom,
#         'students': students,
#         'total_students': total_students,
#         'attendance_records': attendance_records
#     })

# def student_list(request):
#     return render(request, "attendance/attendance.html")

def student_list(request):
    students = TblStudents.objects.all()
    attendance = Attendance.objects.filter(student__in=students)

    return render(request, 'attendance/attendance.html', {'students': students, 'attendance': attendance})
