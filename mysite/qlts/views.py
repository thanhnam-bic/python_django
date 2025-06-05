from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import TaiSan
from django.views.decorators.csrf import csrf_exempt


def index(request):
    print(">> Đã vào view index")
    return HttpResponse("Xin chào. Bạn đã đến app QLTS")

@csrf_exempt
def xoa_tai_san(request, id):
    if request.method == 'DELETE':
        try:
            asset = TaiSan.objects.get(pk=id)
            asset.delete()
            return JsonResponse({'message': 'Xóa tài sản thành công', 'ma_tai_san': id})
        except TaiSan.DoesNotExist:
            return JsonResponse({'error': 'Tài sản không tồn tại', 'ma_tai_san': id}, status=404)
    else:
        return JsonResponse({'error': 'Chỉ hỗ trợ phương thức DELETE'}, status=405)

# Create your views here.
