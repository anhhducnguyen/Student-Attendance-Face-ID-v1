
from django.http import HttpResponse
from django.shortcuts import render
from .models import TblStudents
from django.db.models import Count


# def studentsView(request):
#     students = TblStudents.objects.all()
#     # l = list(TblStudents.objects.all())
#     # t1 = TblStudents.objects.values_list("name", "email")
#     # t2 =TblStudents.annotate(Count("student_id"))
    
#     t3 = TblStudents.objects.values()

#     # This list contains a Blog object.
#     t4 = TblStudents.objects.filter(name__startswith="Beatles")

#     # tìm kiếm chính xác
#     t5 = TblStudents.objects.filter(name="Phong Vu").values()

#     # tìm kiếm 1 phần
#     t6 = TblStudents.objects.filter(name__contains="N").values()

#     print(t6)
#     return render(request, "admin/students.html", {'students': students})

# def data(request):
#     # Lấy tất cả các bản ghi từ bảng TblStudents
#     students = TblStudents.objects.all()
    
#     # Chuyển đổi QuerySet thành danh sách các từ điển để dễ đọc
#     t3 = list(TblStudents.objects.values())

#     # Lọc các bản ghi có name bắt đầu bằng "Beatles"
#     t4 = list(TblStudents.objects.filter(name__startswith="Beatles").values())

#     # Tìm kiếm chính xác
#     t5 = list(TblStudents.objects.filter(name="Phong Vu").values())

#     # Tìm kiếm một phần
#     t6 = list(TblStudents.objects.filter(name__contains="N").values())

#     # In ra dữ liệu thuần cho các truy vấn
#     print("T3:", t3)
#     print("T4:", t4)
#     print("T5:", t5)
#     print("T6:", t6)

#     return HttpResponse(t3)

from django.http import JsonResponse
from .models import TblStudents

def data(request):
    # Lấy tất cả các bản ghi từ bảng TblStudents
    students = TblStudents.objects.all()
    
    # Chuyển đổi QuerySet thành danh sách các từ điển để dễ đọc
    t3 = list(TblStudents.objects.values())

    # Lọc các bản ghi có name bắt đầu bằng "Beatles"
    t4 = list(TblStudents.objects.filter(name__startswith="Beatles").values())

    # Tìm kiếm chính xác
    t5 = list(TblStudents.objects.filter(name="Phong Vu").values())

    # Tìm kiếm một phần
    t6 = list(TblStudents.objects.filter(name__contains="N").values())

    # Đóng gói dữ liệu vào một từ điển để trả về JSON
    data = {
        "all_students": t3,
        "starts_with_beatles": t4,
        "exact_name_phong_vu": t5,
        "contains_n": t6
    }

    # Trả về dữ liệu dưới dạng JSON
    return JsonResponse(data)


def ok(request):
    return render(request, 'ok.htm')

def ok(request):
    return render(request,'ok.htm')
