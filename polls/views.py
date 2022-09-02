from django.http import HttpResponse


def index(request):
    return HttpResponse("-----ここが自動変更されればOKです！")
