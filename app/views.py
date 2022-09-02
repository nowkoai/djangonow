import genericpath
import re
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
from .models import Neuron, Synapse,Task
from django.contrib.auth import login
from .forms import UserCreationForm, TaskForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Neuron

import json
from django.forms import model_to_dict #No
from django.views.generic import View
import logging

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("app:index")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'app/index.html', context)
class TaskView(LoginRequiredMixin,View):
    def get(self, request):
        # リクエストがjson形式のとき
        logging.debug('getしました')
        if request.headers.get("Content-Type") == "application/json":
            # すべてのtaskを辞書型で受け取る
            tasks = Task.objects.all().values()
            tasks_list = list(tasks)
            # json形式でレスポンスを返す
            return JsonResponse(tasks_list, safe=False, status=200)
        return render(request, "app/index.html")

    def post(self, request):
        # json文字列を辞書型にし、pythonで扱えるようにする。
        task = json.loads(request.body)
        form = TaskForm(task)
        logging.debug('postしました')
        # データが正しければ保存する。
        if form.is_valid():
            new_task = form.save()
            return JsonResponse({"task": model_to_dict(new_task)}, status=200)
        return redirect("app:index")

    def put(self, request):
        response = json.loads(request.body)
        # dbの中から、同じidのtaskを取得する。
        task = Task.objects.get(id=response.get("id"))
        # タスクが完了していたら、未完了に、
        # タスクが未完了なら、完了にする
        if task.completed:
            task.completed = False
        else:
            task.completed = True
        # 更新した内容を保存する。
        task.save()
        return JsonResponse(model_to_dict(task))

    def delete(self, request):
        response = json.loads(request.body)
        task = Task.objects.get(id=response.get("id"))
        # タスクを削除する
        task.delete()
        return JsonResponse({"result": "Ok"})