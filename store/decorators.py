from django.http import HttpResponse

from django.shortcuts import redirect


def unauthenticatedUser(view_func):
	def Wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('store')
		return view_func(request, *args, **kwargs)

	return Wrapper_func