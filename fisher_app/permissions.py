"""
API izinleri
"""
from rest_framework import permissions
from fisher import settings


class DomainOnly(permissions.BasePermission):
    """
    settings.py içindeki DOMAIN değişkeninde bulunan adresten başkasını kabul etmez
    """
    def has_permission(self, request, view):
        ref = request.META.get('HTTP_REFERER', None)
        if ref and (settings.DOMAIN in ref or 'localhost' in ref):
            return True
        else:
            return False


class AjaxOnly(permissions.BasePermission):
    """
    Eğer user staff veya superuser değilse sadece ajax çağrılarını kabul eder
    """
    def has_permission(self, request, view):
        s = request.is_ajax() or (request.user.is_authenticated() and (request.user.is_staff or request.user.is_superuser))
        return s


class AuthenticatedUserOnly(permissions.BasePermission):
    """
    Sadece login olmuş ve aktif kullanıcıların çağrılarını kabul eder
    """
    def has_permission(self, request, view):
        s = request.user.is_authenticated() and request.user.is_active
        return s
