from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import TblStudents
from django.http import JsonResponse
from .models import TblStudents
from django.db.models import Count
from .forms import StudentForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# def demo(request):
#     students = TblStudents.objects.all()
#     return render(request, "admin/student.html", {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('demo')
    else:
        form = StudentForm()
    return render(request, 'admin/add_student.html', {'form': form})

def update_student(request, student_id):
    student = get_object_or_404(TblStudents, student_id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('demo')
    else:
        form = StudentForm(instance=student)
    return render(request, 'admin/update_student.html', {'form': form, 'student': student})

def delete_student(request, student_id):
    student = get_object_or_404(TblStudents, student_id=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('demo')
    return render(request, 'admin/delete_student.html', {'student': student})

def demo(request):
    search_query = request.GET.get('q', '')
    if search_query:
        students = TblStudents.objects.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(student_id__icontains=search_query)
        )
    else:
        students = TblStudents.objects.all()
    return render(request, "admin/student.html", {'students': students, 'search_query': search_query})


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


