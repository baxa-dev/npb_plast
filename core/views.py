from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View
from requests import get

from core.forms import ContactForm


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        print(request.POST)
        form = ContactForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                get("http://api.telegram.org/bot5046439124:AAFUJMJzy2dCWNObY1rbEZIWpJ6P7fpR0nA/" 
                    "sendMessage?chat_id=@nbpplast&text={}".format(
                        f"Имя: {form.cleaned_data['full_name']}\nТелефонный номер: {form.cleaned_data['phone']}"
                    ))
                return redirect('/')

        return render(request, 'index.html')
