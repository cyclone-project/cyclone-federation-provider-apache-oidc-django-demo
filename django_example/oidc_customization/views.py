from django.contrib import messages
from django.contrib.auth.models import Group
from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.template.context import RequestContext

from oidc_customization.forms import RegisterUserFromOIDC


def index(request):
    s = "<table>"
    for field in request.META:
        if ',' in str(request.META[field]):
            parts = str(request.META[field]).split(',')
            request.META[field] = "<ul>"
            for p in parts:
                request.META[field] += "<li>" + p + "</li>"
            request.META[field] += "</ul>"
            # request.META[field] = parts[-1].strip()
        if request.META[field] is not None:
            s += "<tr><td>" + field + "</td><td> " + str(request.META[field]) + "</td></tr>"
    s += "</table>"
    return HttpResponse(s)


def register(request):
    if request.method == 'POST':
        form = RegisterUserFromOIDC(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            if not request.user.groups.filter(name="Users waiting for account validation").exists():
                g = Group.objects.get_or_create(name="Users waiting for account validation")[0]
                # new request, setting groups correctly
                g.user_set.add(request.user)
                g.save()
                g = Group.objects.get_or_create(name="Users not requesting account")[0]
                g.user_set.remove(request.user)
                g.save()
                # and mailing administrators
                # TODO mail admin that registration request have been made
    else:
        form = RegisterUserFromOIDC(instance=request.user, request=request)
        # form = RegisterUserFromOIDCBasic(instance=request.user)

    if request.user.groups.filter(name="Users waiting for account validation").exists():
        messages.add_message(request, messages.INFO,
                             'You already have requested an account, your demand will be treated shortly. '
                             'Meanwhile you can still update your information.')
    context = RequestContext(request, {
        'form': form,
    })

    template = loader.get_template('oidc_customization/register.html')
    return HttpResponse(template.render(context))
