# exceptions.py
from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, AuthenticationFailed, PermissionDenied
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        return Response({
            "thanh_cong": False,
            "thong_bao": "Bạn cần đăng nhập để truy cập tài nguyên này",
            "ma_loi": {
                "xac_thuc": "Người dùng chưa được xác thực"
            }
        }, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, PermissionDenied):
        return Response({
            "thanh_cong": False,
            "thong_bao": "Bạn không có quyền thực hiện hành động này",
            "ma_loi": {
                "quyen_truy_cap": "Tài khoản hiện tại không đủ quyền để thực hiện hành động này"
            }
        }, status=status.HTTP_403_FORBIDDEN)

    response = exception_handler(exc, context)
    if response is None:
        return Response({
            "thanh_cong": False,
            "thong_bao": "Đã xảy ra lỗi hệ thống",
            "ma_loi": {
                "he_thong": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau"
            }
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
