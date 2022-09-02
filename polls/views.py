from django.http import HttpResponse


def index(request):
    return HttpResponse("1111111111ここが自動変更されればOKです！")
