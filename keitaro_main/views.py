from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from datetime import datetime
import json



#Прикдад функції для отримання даних з серверу keitaro
'''
import requests
def request_keitaro_data(username, start_date = 0, end_date = 0, today = False):
	response = requests.get('http://keitaro.com')
	pass
'''
user_ids = {'bogdan': 1799244985, 'lovelas': 1836086969} 
# Create your views here.

#Взаємодії за ботом не мають csrf токену
@csrf_exempt
def check_id(request):
	user_id_input = int(request.body.decode("utf-8"))
	key_list = list(user_ids.keys())
	val_list = list(user_ids.values())
	if user_id_input in val_list:
		position = val_list.index(user_id_input)
		data = json.dumps({"id_status": True, "login": key_list[position]})
	else:
		data = json.dumps({"id_status": False})
	return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_bot(request):
	user_data_input = json.loads(request.body)
	user = User.objects.create_user(username = user_data_input['login'], password = user_data_input['password'])
	return HttpResponse(json.dumps({"reg_status": True}), content_type='application/json')

def profile_page(request):		
	if request.user.is_authenticated:
		username = request.user.username
		if (request.method == "POST")&(bool(request.POST.get("start_date")))&(bool(request.POST.get("end_date"))):
			print("\n\nPOST succesful\n\n")
			print(request.POST.get("start_date"))
			print(request.POST.get("end_date"))
			start_date = datetime.strptime(request.POST.get("start_date"), "%Y-%m-%d")
			end_date = datetime.strptime(request.POST.get("end_date"), "%Y-%m-%d")
			#conv_val, clik_val = request_keitaro_data(username, start_date = start_date, end_date = end_date)
			start_date = start_date.strftime("%d.%m.%Y")
			end_date = end_date.strftime("%d.%m.%Y")
			conv_val, clik_val = 1, 1


			return render(request, "profile.html", {"date": f"з {start_date} до {end_date}", "conversions": conv_val, "clicks": clik_val})
		else:
			#conv_val, clik_val = request_keitaro_data(username, today = True)
			conv_val, clik_val = 0, 0
			return render(request, "profile.html", {"date": "за сьогодні", "conversions": conv_val, "clicks": clik_val})
	else:		
		return redirect("/login/")