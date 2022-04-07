# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from polls.forms import *
from polls.models import *
from datetime import date
from django.views.generic.base import TemplateView
import os
import sys
import phonenumbers
from pytr.dl import DL
from pytr.account import login
from pytr.api import TradeRepublicApi
from concurrent.futures import as_completed
import jsonpickle
import asyncio
import shutil
from wsgiref.util import FileWrapper

def error_404(request, *args, **argv):
	data = {}
	return render(request,'404.html', data, status=404)

def error_500(request, *args, **argv):
	data = {}
	return render(request,'500.html', data, status=500)

def error_403(request, *args, **argv):
	data = {}
	return render(request,'403.html', data, status=403)

def error_csrf(request, *args, **argv):
	data = {}
	return render(request,'csrf_error.html', data, status=403)

def index(request):
	return render(request, 'base.html')

def work_responses2(self):
	'''
	process responses of async requests
	'''
	if len(self.doc_urls) == 0:
		self.log.info('Nothing to download')
		exit(0)

	with self.history_file.open('a') as history_file:
		self.log.info('Waiting for downloads to complete..')
		for future in as_completed(self.futures):
			if future.filepath.is_file() is True:
				self.log.debug(f'file {future.filepath} was already downloaded.')

			try:
				r = future.result()
			except Exception as e:
				self.log.fatal(str(e))

			future.filepath.parent.mkdir(parents=True, exist_ok=True)
			with open(future.filepath, 'wb') as f:
				f.write(r.content)
				self.done += 1
				history_file.write(f'{future.doc_url_base}\n')

				self.log.debug(f'{self.done:>3}/{len(self.doc_urls)} {future.filepath.name}')

			if self.done == len(self.doc_urls):
				self.log.info('Done.')
				sys.exit(0)

def login(request):
	if request.method == 'POST':
		if request.POST.get('tel') and request.POST.get('pin'):
			mobile = request.POST['tel']
			pin = request.POST['pin']
			mobile_validate = phonenumbers.parse(mobile)
			if phonenumbers.is_possible_number(mobile_validate) and pin.isnumeric():
				try:
					tr = TradeRepublicApi(phone_no=mobile, pin=pin, keyfile=None, locale='de', save_cookies=False)
					tr.inititate_weblogin()
					s_tr = jsonpickle.encode(tr)
					obj = Account(sess=s_tr)
					obj.save()
					response = HttpResponse(status=204)
					response.set_cookie(key='TRSESS', value=obj.uuid, httponly=True, samesite='Strict')
					return response
				except Exception as e:
					#return HttpResponse("An error occured during weblogin.")
					print(str(e))
					return render(request, '403.html')
			else:
				#return HttpResponse("Please provide a valid phone number and pin.")
				return render(request, '403.html')
		else:
			#return HttpResponse("Please provide a phone number and pin.")
			return render(request, '403.html')
	else:
		return HttpResponse(status=501)

def download(request):
	session = request.COOKIES.get('TRSESS')
	otp = request.POST['otp']

	if session is None:
		return render(request, '403.html')
		#return HttpResponse("Missing session. Please provide your correct credentials.")
	else:
		if len(otp) == 4:
			try:
				obj = Account.objects.filter(uuid=session)[0]
			except:
				return render(request, '403.html')
				#return HttpResponse("Invalid session. Please try again.")

			try:
				tr = jsonpickle.decode(obj.sess)
				tr.complete_weblogin(otp)
			except Exception as e:
				print(str(e))
				return render(request, '403.html')
				#return HttpResponse("Error during weblogin with OTP.")

			path = "/tmp/" + str(session) + "/"

			days = 365
			last_n_days = 0
			#last_n_days = (time.time() - (24 * 3600 * days)) * 1000

			DL.work_responses = work_responses2

			dl = DL(
			tr,
			path,
			"{iso_date}{time} {title}{doc_num}",
			since_timestamp=last_n_days,
			max_workers=8,
			)

			today = date.today()
			now = today.strftime("%Y%m%d")
			filename = now + "_" + "TRSync_" + str(session)

			coroutine = dl.dl_loop()

			try:
				coroutine = dl.dl_loop()
				loop = asyncio.new_event_loop()
				asyncio.set_event_loop(loop)
				data = loop.run_until_complete(coroutine)
			except KeyboardInterrupt:
				#return HttpResponse("Interrupt")
				return render(request, '500.html')
			finally:
				loop.close()
				print("Creating ZIP archive")
				path_to_zip = shutil.make_archive(filename, 'zip', path)
				print(str(path_to_zip))
				response = HttpResponse(FileWrapper(open(path_to_zip,'rb')), content_type='application/zip')
				response['Content-Disposition'] = 'attachment; filename="{filename}.zip"'.format(
				filename = filename
				)
				# remove zip file
				print("Removing all sensitive files and objects.")
				os.remove(path_to_zip)
				# remove dir at /tmp/<session-id>
				shutil.rmtree(path)
				# remove model object with class object
				Account.objects.filter(uuid=session).delete()
				# return zip file for download
				print("Providing the zip file.")
				return response

		else:
			#return HttpResponse("Wrong OTP length")
			return render(request, '403.html')
