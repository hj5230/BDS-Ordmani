from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class Auth(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info == '/login/':
            return
        user = request.session.get('user')
        if user:
            return
        return redirect('/login/')

class AdminAces(MiddlewareMixin):
    def process_request(self, request):
        '''if不用此项验证的网站return 网址白名单'''
        pos = request.session['user']['pos_id']
        if not(2 <= pos <= 4):
            return
        return redirect('/dashboard/')

class officeAces(MiddlewareMixin):
    def process_request(self, request):
        pos = request.session['user']['pos_id']
        if pos == 2:
            return
        return redirect('/dashboard/')

class salesAces(MiddlewareMixin):
    def process_request(self, request):
        pos = request.session['user']['pos_id']
        if pos == 3:
            return
        return redirect('/dashboard/')

class wareAces(MiddlewareMixin):
    def process_request(self, request):
        pos = request.session['user']['pos_id']
        if pos == 4:
            return
        return redirect('/dashboard/')