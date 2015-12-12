from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

from netdev.models import *
from netdev.forms import *
from datetime import datetime


from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


# suport functions

def decode_url(url_to_decode):
    return url_to_decode.replace('_', ' ')

def encode_url(url_to_encode):
    return url_to_encode.replace(' ', '_')

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/netdev/')

def create_topic(forum_name_url, subforum_name_url, category_name_url):

    url = "/netdev/forum/%s/%s/%s/" % (forum_name_url, subforum_name_url, category_name_url)

    return HttpResponseRedirect(url)

def create_post(forum_name_url, subforum_name_url, category_name_url, topic_id):

    url = "/netdev/forum/%s/%s/%s/%s/" % (forum_name_url, subforum_name_url, category_name_url, topic_id)

    return HttpResponseRedirect(url)

#view functions

def data(request):
    context_dict = user_info(request)
    return render(request, 'netdev/dados.html', context_dict)

def acceptance(request):
    context_dict = user_info(request)
    return render(request, 'netdev/aceitacao.html', context_dict)

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    if request.user.is_authenticated():
        return HttpResponse("You are logged in!")
    else:
        # If it's a HTTP POST, we're interested in processing form data.
        if request.method == 'POST':
            # Attempt to grab information from the raw form information.
            # Note that we make use of both UserForm and UserProfileForm.
            user_form = UserForm(data=request.POST)
            profile_form = UserProfileForm(data=request.POST)

            # If the two forms are valid...
            if user_form.is_valid() and profile_form.is_valid():
                # Save the user's form data to the database.
                user = user_form.save()

                # Now we hash the password with the set_password method.
                # Once hashed, we can update the user object.
                user.set_password(user.password)
                user.save()
                Friendlist.objects.create(main_user=user)

                # Now sort out the UserProfile instance.
                # Since we need to set the user attribute ourselves, we set commit=False.
                # This delays saving the model until we're ready to avoid integrity problems.
                profile = profile_form.save(commit=False)
                profile.user = user
                PublicProfile.objects.create(user=user)

                # Did the user provide a profile picture?
                # If so, we need to get it from the input form and put it in the UserProfile model.
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']

                # Now we save the UserProfile model instance.
                profile.save()

                # Update our variable to tell the template registration was successful.
                registered = True

            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            # They'll also be shown to the user.
            else:
                print user_form.errors, profile_form.errors

        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()

        # Render the template depending on the context.
        return render(request, 'netdev/register.html',
                {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.user.is_authenticated():
        return HttpResponse("You are logged in!")
    else:
        if request.method == 'POST':
            # Gather the username and password provided by the user.
            # This information is obtained from the login form.
                    # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                    # because the request.POST.get('<variable>') returns None, if the value does not exist,
                    # while the request.POST['<variable>'] will raise key error exception
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Use Django's machinery to attempt to see if the username/password
            # combination is valid - a User object is returned if it is.
            user = authenticate(username=username, password=password)

            # If we have a User object, the details are correct.
            # If None (Python's way of representing the absence of a value), no user
            # with matching credentials was found.
            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    login(request, user)
                    return HttpResponseRedirect('/netdev/')
                else:
                    # An inactive account was used - no logging in!
                    return render(request, 'netdev/login.html', {'desativada':True})
            else:
                # Bad login details were provided. So we can't log the user in.
                print "Informacoes invalidas de Login: {0}, {1}".format(username, password)
                return render(request, 'netdev/login.html', {'erro': True})

        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
        else:
            # No context variables to pass to the template system, hence the
            # blank dictionary object...
            return render(request, 'netdev/login.html', {})

@login_required
def users(request):
    context_dict = user_info(request)
    users_dict = []

    print request.POST
    if request.POST['search'] == '':
        users = User.objects.all().order_by('date_joined')[:100]
        friend_list = Friendlist.objects.get_or_create(main_user=request.user)[0]

        for user in users:
            if user.username == 'moderador':
                pass
            elif user.username == 'admin':
                pass
            else:
                if user in friend_list.friends.all():
                    users_dict.append({'user':user, 'profile':UserProfile.objects.get(user=user), 'public_profile':PublicProfile.objects.get(user=user), 'is_friend': True})
                else:
                     users_dict.append({'user':user, 'profile':UserProfile.objects.get(user=user), 'public_profile':PublicProfile.objects.get(user=user), 'is_friend': False})

        context_dict.update({'users': users_dict})

    else:
        users_profile = UserProfile.objects.filter(display_name__contains=request.POST['search'])
        public_profiles = PublicProfile.objects.filter(tags__contains=request.POST['search'])

        if len(users_profile) == 0 and len(public_profiles) == 0:
            context_dict.update({'empty':True, 'search':request.POST['search']})
        else:
            for user_profile in users_profile:
                user = User.objects.get(id=user_profile.user.id)
                friend_list = Friendlist.objects.get_or_create(main_user=user)[0]

                if user.username == 'moderador':
                    pass
                elif user.username == 'admin':
                    pass
                elif user == request.user:
                    pass
                else:
                    if user in friend_list.friends.all():
                        users_dict.append({'user':user, 'profile':user_profile, 'public_profile':PublicProfile.objects.get(user=user), 'is_friend': True})
                    else:
                         users_dict.append({'user':user, 'profile':user_profile, 'public_profile':PublicProfile.objects.get(user=user), 'is_friend': False})

            for public_profile in public_profiles:
                user = User.objects.get(id=public_profile.user.id)
                user_profile = UserProfile.objects.filter(user=user)[0]
                friend_list = Friendlist.objects.get_or_create(main_user=user)[0]

                if user.username == 'moderador':
                    pass
                elif user.username == 'admin':
                    pass
                elif user == request.user:
                    pass
                else:
                    if user in friend_list.friends.all():
                        users_dict.append({'user':user, 'profile':user_profile, 'public_profile':public_profile, 'is_friend': True})
                    else:
                         users_dict.append({'user':user, 'profile':user_profile, 'public_profile':public_profile, 'is_friend': False})

            if len(users_dict) == 0:
                context_dict.update({'empty':True, 'search':request.POST['search']})
            else:
                context_dict.update({'users': users_dict})

    return render(request, 'netdev/users.html', context_dict)

@login_required
def inbox(request):
    context_dict = user_info(request)

    inbox = Message.objects.filter(recipient=request.user, is_trash=False).order_by('-date')

    context_dict.update({'inbox': inbox})

    if request.POST:
        if 'message' in request.POST:
            for id in request.POST.getlist('message'):
                message = Message.objects.get(id=id)
                message.is_trash = True
                message.save()

    return render(request, 'netdev/messages/inbox.html', context_dict)

@login_required
def outbox(request):
    context_dict = user_info(request)

    outbox = Message.objects.filter(sender=request.user)

    context_dict.update({'outbox':outbox})

    return render(request, 'netdev/messages/outbox.html', context_dict)

@login_required
def trash(request):
    context_dict = user_info(request)

    inbox = Message.objects.filter(recipient=request.user, is_trash=True).order_by('-date')

    context_dict.update({'inbox': inbox})

    if request.POST:
        print request.POST
        if 'message' in request.POST:
            if 'delete' in request.POST:
                for id in request.POST.getlist('message'):
                    message = Message.objects.get(id=id)
                    message.delete()
            elif 'restore' in request.POST:
                for id in request.POST.getlist('message'):
                    message = Message.objects.get(id=id)
                    message.is_trash = False
                    message.save()

    return render(request, 'netdev/messages/trash.html', context_dict)

@login_required
def new_message(request):
    context_dict = user_info(request)

    if request.method == 'POST':
        print request.POST
        if 'answer' in request.POST:
            if request.POST['to'] == request.user.username:
                context_dict.update({'to': request.POST['from'], 'title': 'RE: ' + request.POST['title']})
            elif request.POST['from'] == request.user.username:
                context_dict.update({'to': request.POST['to'], 'title': 'RE: ' + request.POST['title'] })
        elif 'forward' in request.POST:
            context_dict.update({'title': 'FW: ' + request.POST['title'], 'text': request.POST['text']})

        if 'body' in request.POST:
            context_dict.update({'title': request.POST['subject'], 'text': request.POST['body'], 'to': request.POST['recipient']})
            try:
                recipient = request.POST['recipient']
                recipient_user = User.objects.get(username=recipient)

            except:
                context_dict.update({'erro':'Usuario destinatario invalido'})
                return render(request, 'netdev/messages/new_message.html', context_dict)

            if request.POST['body'] != '':
                body = request.POST['body']
                if request.POST['subject'] != '':
                    subject = request.POST['subject']
                    message = Message(recipient=recipient_user,sender=request.user,text=body,title=subject)
                    message.save()
                    return HttpResponseRedirect('/netdev/nova_mensagem/sucesso/')
                else:
                    context_dict.update({'erro':'Por favor, preencha o assunto da mensagem'})
                    return render(request, 'netdev/messages/new_message.html', context_dict)
            else:
                context_dict.update({'erro':'Por favor, preencha o corpo da mensagem'})
                return render(request, 'netdev/messages/new_message.html', context_dict)
    else:
        friend_list = Friendlist.objects.get_or_create(main_user=request.user)[0]
        print friend_list.friends.all()
        context_dict.update({'friend_list':friend_list.friends.all()})

    return render(request, 'netdev/messages/new_message.html', context_dict)

@login_required
def confirm_message(request):
    context_dict = user_info(request)
    return render(request, 'netdev/messages/sucess.html', context_dict)


@login_required
def message(request, message_id):
    context_dict = user_info(request)

    message = Message.objects.get(id=message_id)

    context_dict.update({'message': message})

    return render(request, 'netdev/messages/message.html', context_dict)

@login_required
def my_topics(request):
    context_dict = user_info(request)
    topic_dict = []

    topic_list = Topic.objects.filter(user=request.user).order_by('-creation_date')
    for topic in topic_list:
        category = topic.category
        subforum = topic.category.subforum
        forum = topic.category.subforum.forum
        topic_dict.append({'topic': topic, 'category':category, 'subforum':subforum,'forum':forum,
        'url': encode_url("/netdev/forum/%s/%s/%s/%s/"%(forum, subforum, category, topic.id))})

    context_dict.update({'topics': topic_dict})

    return render(request, 'netdev/forum/my_topics.html', context_dict)

@login_required
def repositorys(request):
    context_dict = user_info(request)
    return render(request, 'netdev/repositorys.html', context_dict)

def user_info(request):

    context_dict = {}
    current_user = request.user
    if current_user.username == 'admin':
        context_dict['user'] = current_user
        context_dict['user_profile'] = {'display_name': 'Admin'}

    elif current_user.is_authenticated():
        context_dict['user'] = current_user
        user_profile = UserProfile.objects.get(user=current_user)
        public_profile = PublicProfile.objects.get(user=current_user)
        context_dict['user_profile'] = user_profile
        context_dict['public_profile'] = public_profile

    return context_dict

def index(request):

    context_dict = user_info(request)
    updates_dict = []

    if context_dict != {}:

        user = request.user

        friend_list_obj = Friendlist.objects.get_or_create(main_user=user)[0]
        friend_list = friend_list_obj.friends.all()

        if request.POST:
            if 'body' in request.POST:
                status = StatusUpdate.objects.create(user=user, text=request.POST['body'], date=timezone.get_current_timezone().normalize(timezone.now().astimezone(timezone.get_current_timezone())))
                status.save()

        status_all = StatusUpdate.objects.all().order_by('-date')[:100]

        for status in status_all:
            if status.user in friend_list or status.user == user:
                updates_dict.append({'update':status, 'profile':UserProfile.objects.get(user=status.user)})

        context_dict.update({'updates': updates_dict})

         #contando o numero de acessos do usuario
        visits = request.session.get('visits')
        if not visits:
            visits = 1
        reset_last_visit_time = False

        last_visit = request.session.get('last_visit')
        if last_visit:
            last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

            if (datetime.now() - last_visit_time).seconds > 0:
                # ...reassign the value of the cookie to +1 of what it was before...
                visits = visits + 1
                # ...and update the last visit cookie, too.
                reset_last_visit_time = True
        else:
            # Cookie last_visit doesn't exist, so create it to the current date/time.
            reset_last_visit_time = True

        if reset_last_visit_time:
            request.session['last_visit'] = str(datetime.now())
            request.session['visits'] = visits

    return render(request,'netdev/index.html', context_dict)

@login_required
def public_profile(request, username):

    context_dict = user_info(request)
    user = User.objects.get(username=username)
    context_dict.update({'public_user': user,
                    'public_user_general':UserProfile.objects.get(user=user),
                    'public_user_profile':PublicProfile.objects.get(user=user)})
    friend_list = Friendlist.objects.get_or_create(main_user=request.user)[0]

    if user in friend_list.friends.all():
        context_dict['is_friend'] = True
    else:
        context_dict['is_friend'] = False

    return render(request, 'netdev/profile/public_profile.html', context_dict )

# def search(request):
#
#     context_dict = user_info(request)
#     print request.POST
#
#     return render(request, 'netdev/index.html', context_dict)

def profile_friends(request, username):

    context_dict = user_info(request)
    user = User.objects.get(username=username)
    context_dict.update({'public_user': user})
    users_dict = []

    friend_list = Friendlist.objects.get_or_create(main_user=user)[0]
    main_friend_list = Friendlist.objects.get(main_user=request.user)

    for friend in friend_list.friends.all():
        if friend in main_friend_list.friends.all():
            users_dict.append({'user':friend, 'profile':UserProfile.objects.get(user=friend), 'public_profile':PublicProfile.objects.get(user=friend), 'is_friend': True})
        else:
            users_dict.append({'user':friend, 'profile':UserProfile.objects.get(user=friend), 'public_profile':PublicProfile.objects.get(user=friend), 'is_friend': False})

    context_dict.update({'users': users_dict})

    return render(request, 'netdev/profile/profile_friends.html', context_dict )

def profile_repository(request, username):

    context_dict = user_info(request)
    user = User.objects.get(username=username)
    context_dict.update({'public_user': user})
    cat_dict = []
    files = RepoFile.objects.filter(author=user, public=True)
    categories = FileCategory.objects.filter(owner=user).order_by('pub_date')

    for category in categories:
        if RepoFile.objects.filter(category=category, public=True):
            cat_dict.append({'category': category, 'is_empty': False})
        else:
            cat_dict.append({'category': category, 'is_empty': True})

    context_dict.update({'files': files, 'categories': cat_dict})

    return render(request,'netdev/profile/public_repository.html', context_dict)

def profile_status(request, username):

    context_dict = user_info(request)
    user = User.objects.get(username=username)
    context_dict.update({'public_user': user, 'public_user_profile':UserProfile.objects.get(user=user),})
    status_all = StatusUpdate.objects.filter(user=user).order_by('-date')[:100]

    context_dict.update({'updates': status_all})
    print context_dict

    return render(request, 'netdev/profile/profile_status.html', context_dict )

def remove_status(request, update_id):

    context_dict = user_info(request)

    status = StatusUpdate.objects.get(id=update_id)
    context_dict.update({'update': status})

    if request.POST:
        if 'delete' in request.POST:
            status.delete()

            return HttpResponseRedirect('/netdev/perfil/%s/status/' % request.user.username)

    return render(request, 'netdev/profile/remove_status.html', context_dict )

def edit_status(request, update_id):

    context_dict = user_info(request)

    status = StatusUpdate.objects.get(id=update_id)
    context_dict.update({'update': status})

    if request.POST:
        status.text = request.POST['body']
        status.save()

        return HttpResponseRedirect('/netdev/perfil/%s/status/' % request.user.username)

    return render(request, 'netdev/profile/edit_status.html', context_dict )

@login_required
def check_account(request):
    context_dict = user_info(request)
    return render(request, 'netdev/profile/check_account.html', context_dict)

@login_required
def deactivate_account(request):
    context_dict = user_info(request)
    user = request.user

    if request.POST:
        if 'password' in request.POST:
            username = user
            user_auth = authenticate(username=username, password=request.POST['password'])
            if user_auth:
                user.is_active = False
                user.save()
                logout(request)
                return render(request, 'netdev/profile/confirm_deactivate.html', context_dict)
            else:
                context_dict.update({'erro':'erro'})
                return render(request, 'netdev/profile/deactivate_account.html', context_dict)

    return render(request, 'netdev/profile/deactivate_account.html', context_dict)

@login_required
def change_password(request):
    context_dict = user_info(request)
    user = request.user

    if request.POST:
        print request.POST
        user_auth = authenticate(username=user, password=request.POST['current_password'])
        pass1 = request.POST['new_password']
        pass2 = request.POST['new_password2']
        if user_auth:
            if pass1 == pass2:
                user.set_password(pass1)
                user.save()
                update_session_auth_hash(request, user)

                return render(request, 'netdev/profile/confirm_password.html', context_dict)
            else:
                context_dict.update({'error2':True, 'pass':request.POST['current_password']})
        else:
            if pass1 == pass2:
                context_dict.update({'error1':True, 'pass2':pass2})
            else:
                context_dict.update({'error1':True, 'error2':True})

    return render(request, 'netdev/profile/change_password.html', context_dict)

@login_required
def view_account(request):
    context_dict = user_info(request)
    user = request.user
    context_dict.update({'public_user': user,
                    'public_user_general':UserProfile.objects.get(user=user),
                    'public_user_profile':PublicProfile.objects.get(user=user)})

    return render(request, 'netdev/profile/view_account.html', context_dict)

@login_required
def edit_account(request):
    context_dict = user_info(request)
    user = request.user
    cur_user = UserProfile.objects.filter(user=user)[0]

    profile_form = UserProfileForm(request.POST or None, request.FILES or None, instance=cur_user)
    context_dict.update({'profile_form':profile_form})

    if request.method == "POST":
        if profile_form.is_valid():
            profile_form_uncommited = profile_form.save(commit=False)
            profile_form_uncommited.save()

            return redirect('/netdev/minha_conta/')

    return render(request, 'netdev/profile/edit_account.html', context_dict)

@login_required
def change_profile(request):
    context_dict = user_info(request)
    if request.POST:
        if 'job' in request.POST:
            public_profile = PublicProfile.objects.get(user=request.user)
            public_profile.academics = request.POST['academics']
            public_profile.experience = request.POST['experience']
            public_profile.tags = request.POST['tags']
            public_profile.job = request.POST['job']
            public_profile.location = request.POST['location']
            public_profile.save()

            return HttpResponseRedirect('/netdev/perfil/' + str(request.user))

    return render(request, 'netdev/profile/change_profile.html', context_dict)

@login_required
def confirm_friendship(request, username):

    context_dict = user_info(request)
    user = User.objects.get(username=username)
    context_dict.update({'public_user': user,
                    'public_user_profile':UserProfile.objects.get(user=user)})

    if request.POST:
        friend_list = Friendlist.objects.get_or_create(main_user=request.user)[0]

        try:
            friend_list.friends.add(user)
            friend_list.save()
            context_dict['success'] = True
        except:
            pass


    return render(request, 'netdev/profile/confirm_friendship.html', context_dict )

@login_required
def remove_friendship(request, username):

    context_dict = user_info(request)
    user = User.objects.get(username=username)
    context_dict.update({'public_user': user,
                    'public_user_profile':UserProfile.objects.get(user=user)})

    if request.POST:
        friend_list = Friendlist.objects.get_or_create(main_user=request.user)[0]

        try:
            friend_list.friends.remove(user)
            friend_list.save()
            context_dict['success'] = True
        except:
            pass


    return render(request, 'netdev/profile/remove_friendship.html', context_dict )

def about(request):
   # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = user_info(request)
    if context_dict != {}:
        visits = request.session.get('visits')
        if not visits:
            visits = 1

        last_visit = request.session.get('last_visit')
        if not last_visit:
           last_visit = str(datetime.now())

        context_dict['visits'] = str(visits)
        context_dict['last_visit'] = last_visit[0:16    ]

        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.
    return render(request,'netdev/about.html', context_dict)

# Forum Views
@login_required
def foruns(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    #context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    context_dict = user_info(request)

    forum_list = Forum.objects.order_by('name')
    context_dict['foruns'] = forum_list

    for forum in forum_list:
        forum.url = forum.name.replace(' ', '_')

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'netdev/forum/foruns.html', context_dict)

@login_required
def forum(request, forum_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the forum name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    forum_name = forum_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the forum passed by the user.

    context_dict = user_info(request)
    context_dict['forum_name'] = forum_name

    try:
        # Can we find a forum with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        forum = Forum.objects.get(name=forum_name)

        # Retrieve all of the associated topics.
        # Note that filter returns >= 1 model instance.
        subforuns = SubForum.objects.filter(forum=forum)

        # Adds our results list to the template context under name pages.
        context_dict['subforuns'] = subforuns
        # We also add the forum object from the database to the context dictionary.
        # We'll use this in the template to verify that the forum exists.
        context_dict['forum'] = forum

        for subforum in subforuns:
            subforum.url = subforum.name.replace(' ', '_')

    except Forum.DoesNotExist:
        # We get here if we didn't find the specified forum.
        # Don't do anything - the template displays the "no Forum" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('netdev/forum/forum.html', context_dict, context)

@login_required
def subforum(request, forum_name_url, subforum_name_url):

    context = RequestContext(request)

    forum_name = forum_name_url.replace('_', ' ')
    subforum_name = subforum_name_url.replace('_', ' ')

    context_dict = user_info(request)
    context_dict['forum_name'] = forum_name
    context_dict['subforum_name'] = subforum_name

    try:
        forum = Forum.objects.get(name=forum_name)
        subforum = SubForum.objects.filter(forum=forum, name=subforum_name)[0]
        categories = Category.objects.filter(subforum=subforum).order_by('name')[:10]

        context_dict['forum'] = forum
        context_dict['subforum'] = subforum
        context_dict['categories'] = categories

        for category in categories:
            category.url = category.name.replace(' ', '_')

    except SubForum.DoesNotExist:
        pass

    return render_to_response('netdev/forum/subforum.html', context_dict, context)

@login_required
def category(request, forum_name_url, subforum_name_url, category_name_url):

    context = RequestContext(request)

    forum_name = forum_name_url.replace('_', ' ')
    subforum_name = subforum_name_url.replace('_', ' ')
    category_name = category_name_url.replace('_', ' ')

    context_dict = user_info(request)
    context_dict['forum_name'] = forum_name
    context_dict['subforum_name'] = subforum_name
    context_dict['category_name'] = category_name

    try:
        forum = Forum.objects.get(name=forum_name)
        subforum = SubForum.objects.filter(forum=forum, name=subforum_name)[0]
        category = Category.objects.filter(subforum=subforum, name=category_name)[0]
        topics = Topic.objects.filter(category=category)

        context_dict['forum'] = forum
        context_dict['subforum'] = subforum
        context_dict['category'] = category
        context_dict['topics'] = topics

    except Category.DoesNotExist:
        pass

    return render_to_response('netdev/forum/category.html', context_dict, context)

@login_required
def topic(request, forum_name_url, subforum_name_url, category_name_url, topic_id):

    context = RequestContext(request)
    context_dict = user_info(request)

    forum_name = forum_name_url.replace('_', ' ')
    subforum_name = subforum_name_url.replace('_', ' ')
    category_name = category_name_url.replace('_', ' ')

    context_dict.update({'forum_name': forum_name, 'subforum_name': subforum_name, 'category_name': category_name,
                    'topic_id': topic_id, 'url': 'netdev/forum/%s/%s/%s/%s/' % (forum_name, subforum_name, category_name, topic_id)})

    try:
        forum = Forum.objects.get(name=forum_name)
        subforum = SubForum.objects.filter(forum=forum,name=subforum_name)[0]
        category = Category.objects.filter(subforum=subforum, name=category_name)[0]
        topic = Topic.objects.get(id=topic_id)
        posts = Post.objects.filter(topic=topic).order_by('updated')

        topic_user = UserProfile.objects.get(user=topic.user)
        post_objects = []
        for post in posts:
            user_profile = UserProfile.objects.get(user=post.user)
            post_objects.append({'user': user_profile, 'post': post, 'public_profile':PublicProfile.objects.get(user=post.user)})

        context_dict['forum'] = forum
        context_dict['subforum'] = subforum
        context_dict['category'] = category
        context_dict['topic'] = topic
        context_dict['topic_user'] = topic_user
        context_dict['topic_user_public'] = PublicProfile.objects.filter(user=topic.user)[0]
        context_dict['posts'] = post_objects

    except Topic.DoesNotExist:
        pass

    return render_to_response('netdev/forum/topic.html', context_dict, context)

@login_required
def add_topic(request, forum_name_url, subforum_name_url, category_name_url):
    # Get the context from the request.
    context = RequestContext(request)

    forum_name = forum_name_url.replace('_', ' ')
    subforum_name = subforum_name_url.replace('_', ' ')
    category_name = category_name_url.replace('_', ' ')

    context_dict = user_info(request)

    # A HTTP POST?
    if request.method == 'POST':
        form = TopicForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            topic = form.save(commit=False)

            # Now call the index() view.
            # The user will be shown the homepage.
            try:
                forum = Forum.objects.get(name=forum_name)
                subforum = SubForum.objects.filter(forum=forum, name=subforum_name)[0]
                category_object = Category.objects.filter(subforum=subforum, name=category_name)[0]

                topic.category = category_object
                topic.user = request.user
            except Category.DoesNotExist:
                # If we get here, the subcategory does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('netdev/forum/add_topic.html', context_dict, context)

            topic.save()

            return create_topic(forum_name_url, subforum_name_url, category_name_url)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = TopicForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    context_dict['topic_form'] =  form

    return render_to_response('netdev/forum/add_topic.html', context_dict, context)

@login_required
def add_post(request, forum_name_url, subforum_name_url, category_name_url, topic_id):
    print request.POST
    context = RequestContext(request)

    forum_name = forum_name_url.replace('_', ' ')
    subforum_name = subforum_name_url.replace('_', ' ')
    category_name = category_name_url.replace('_', ' ')

    context_dict = user_info(request)

    if request.method == 'POST':
        form = PostForm(request.POST or None)

        if form.is_valid():
            # This time we cannot commit straight away.
            # Not all fields are automatically populated!
            post = form.save(commit=False)

            # Retrieve the associated Category object so we can add it.
            # Wrap the code in a try block - check if the category actually exists!
            try:
                forum = Forum.objects.get(name=forum_name)
                subforum = SubForum.objects.filter(forum=forum, name=subforum_name)[0]
                category = Category.objects.filter(subforum=subforum, name=category_name)[0]
                topic_ob = Topic.objects.get(id=topic_id)
                post.topic = topic_ob
                post.user = request.user

            except Topic.DoesNotExist:
                # If we get here, the topic does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render_to_response('netdev/forum/topic.html', context_dict, context)

            # Also, create a default value for the number of views.
            post.views = 0

            # With this, we can then save our new model instance.
            post.save()

            # Now that the page is saved, display the category instead.
            return create_post(forum_name_url, subforum_name_url, category_name_url, topic_id)
        else:
            print form.errors
    else:
        form = PostForm()

    context_dict['post_form'] = form

    return render_to_response('netdev/forum/add_post.html', context_dict, context)

@login_required
def edit_topic(request, forum_name_url, subforum_name_url, category_name_url, topic_id):

    context_dict = user_info(request)

    forum_name = forum_name_url.replace('_', ' ')
    subforum_name = subforum_name_url.replace('_', ' ')
    category_name = category_name_url.replace('_', ' ')

    if request.method == 'POST':
        if 'edit' in request.POST:
            try:
                forum = Forum.objects.get(name=forum_name)
                subforum = SubForum.objects.filter(forum=forum, name=subforum_name)[0]
                category = Category.objects.filter(subforum=subforum, name=category_name)[0]
                topic_ob = Topic.objects.get(id=topic_id)

                if 'Post' in request.POST['edit']:
                    post_ob = Post.objects.get(id=request.POST['edit'].strip('Post '))
                    context_dict['post'] = post_ob

                    return render(request, 'netdev/forum/edit_topic.html', context_dict)
                elif 'Topic' in request.POST['edit']:
                    topic_ob = Topic.objects.get(id=request.POST['edit'].strip('Topic '))
                    context_dict['topic'] = topic_ob

                    return render(request, 'netdev/forum/edit_topic.html', context_dict)

                else:
                    print 'none'

            except Topic.DoesNotExist:
                # If we get here, the topic does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render(request, 'netdev/forum/category.html', context_dict)

        elif 'post_id' in request.POST:
            try:
                text = request.POST['body']
                post_id = request.POST['post_id']
                post_ob = Post.objects.get(id=post_id)
                post_ob.body = text
                post_ob.creation_date = datetime.now()
                post_ob.save()

                return create_post(forum_name_url, subforum_name_url, category_name_url, topic_id)


            except Post.DoesNotExist:
                # If we get here, the topic does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render(request, 'netdev/forum/category.html', context_dict)

        elif 'topic_id' in request.POST:
            try:
                text = request.POST['text']
                title = request.POST['title']
                topic_id = request.POST['topic_id']
                topic_ob = Topic.objects.get(id=topic_id)
                topic_ob.text = text
                topic_ob.title = title
                topic_ob.save()

                return create_post(forum_name_url, subforum_name_url, category_name_url, topic_id)


            except Topic.DoesNotExist:
                # If we get here, the topic does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render(request, 'netdev/forum/category.html', context_dict)

        else:
            print 'error'

    else:
        print 'nao post'
    return render(request, 'netdev/forum/edit_topic.html', context_dict)

@login_required
def edit_post(request, forum_name_url, subforum_name_url, category_name_url, topic_id):
    return edit_topic(request, forum_name_url, subforum_name_url, category_name_url, topic_id)

@login_required
def remove_topic(request, forum_name_url, subforum_name_url, category_name_url, topic_id):

    context_dict = user_info(request)

    if request.method == 'POST':
        if 'remove' in request.POST:
            try:
                topic_ob = Topic.objects.get(id=topic_id)
                context_dict['topic'] = topic_ob

                return render(request, 'netdev/forum/remove_topic.html', context_dict)
            except Topic.DoesNotExist:
                # If we get here, the topic does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render(request, 'netdev/forum/topic.html', context_dict)

        if 'topic_id' in request.POST:
            try:
                topic_ob = Topic.objects.get(id=topic_id)
                posts = Post.objects.filter(topic=topic_ob)
                posts.delete()
                topic_ob.delete()

                return HttpResponseRedirect('/netdev/forum/%s/%s/%s/' % (forum_name_url, subforum_name_url, category_name_url))


            except Topic.DoesNotExist:
                # If we get here, the topic does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render(request, 'netdev/forum/topic.html', context_dict)


    return render(request, 'netdev/forum/topic.html', context_dict)

@login_required
def remove_post(request, forum_name_url, subforum_name_url, category_name_url, topic_id):

    context_dict = user_info(request)

    print request.POST

    if request.method == 'POST':
        if 'remove' in request.POST:
            try:
                post_ob = Post.objects.get(id=request.POST['remove'].strip('Post '))
                context_dict['post'] = post_ob

                return render(request, 'netdev/forum/remove_topic.html', context_dict)

            except Post.DoesNotExist:
                # If we get here, the topic does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render(request, 'netdev/forum/topic.html', context_dict)

        if 'post_id' in request.POST:
            try:
                post_ob = Post.objects.get(id=request.POST['post_id'])
                post_ob.delete()

                return HttpResponseRedirect('/netdev/forum/%s/%s/%s/%s/' % (forum_name_url, subforum_name_url, category_name_url, topic_id))

            except Post.DoesNotExist:
                # If we get here, the topic does not exist.
                # Go back and render the add category form as a way of saying the category does not exist.
                return render(request, 'netdev/forum/topic.html', context_dict)

    return render(request, 'netdev/forum/topic.html', context_dict)


def repository_index(request):

    context_dict = user_info(request)
    cat_dict = []
    files = RepoFile.objects.filter(author=request.user)
    categories = FileCategory.objects.filter(owner=request.user).order_by('pub_date')

    for category in categories:
        if RepoFile.objects.filter(category=category):
            cat_dict.append({'category': category, 'is_empty': False})
        else:
            cat_dict.append({'category': category, 'is_empty': True})

    context_dict.update({'files': files, 'categories': cat_dict})

    return render(request,'netdev/repository/repofile_index.html', context_dict)

def add_file(request):

    context_dict = user_info(request)
    file_form = RepoFileForm(request.POST or None, request.FILES or None)

    file_form.fields['category'].queryset = FileCategory.objects.filter(owner=request.user)

    if request.method == 'POST':
        if file_form.is_valid():
            file_form_uncommited = file_form.save(commit=False)
            file_form_uncommited.author = request.user
            file_form_uncommited.save()
            file_form.save_m2m()

            return redirect('/netdev/meu_repositorio/')

    context_dict.update({'form': file_form})

    return render(request,'netdev/repository/repofile_add.html', context_dict)


def add_filecat(request):

    context_dict = user_info(request)
    filecat_form = FileCategoryForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if filecat_form.is_valid():
            filecat_form_uncommited = filecat_form.save(commit=False)
            filecat_form_uncommited.owner = request.user
            filecat_form_uncommited.save()
            filecat_form.save_m2m()
    #
            return redirect('/netdev/meu_repositorio/')

    context_dict.update({'form': filecat_form})

    return render(request, 'netdev/repository/filecat_add.html', context_dict)

def cat_delete(request, cat_id):

    context_dict = user_info(request)
    category = FileCategory.objects.get(id=cat_id)
    context_dict.update({'category': category})

    if request.POST:
        if 'category_id' in request.POST:
            cat_ob = FileCategory.objects.get(id=request.POST['category_id'])
            files = RepoFile.objects.filter(category=cat_ob)
            files.delete()
            cat_ob.delete()
            return redirect('/netdev/meu_repositorio/')

    return render(request, 'netdev/repository/filecat_delete.html', context_dict)

def cat_edit(request, cat_id):

    context_dict = user_info(request)
    cur_cat = get_object_or_404(FileCategory, pk=cat_id)

    editcat_form = FileCategoryForm(request.POST or None, instance=cur_cat)

    if request.method == "POST":
        if editcat_form.is_valid():
            editcat_form_uncommited = editcat_form.save(commit=False)
            editcat_form_uncommited.save()

            return redirect('/netdev/diretorio/%s/' % cat_id)

    context_dict.update({'form':editcat_form})

    return render(request,'netdev/repository/filecat_edit.html', context_dict)

def edit_file(request, file_id):

    context_dict = user_info(request)
    cur_file = get_object_or_404(RepoFile, pk=file_id)

    editfile_form = RepoFileForm(request.POST or None, request.FILES or None, instance=cur_file)
    editfile_form.fields['category'].queryset = FileCategory.objects.filter(owner=request.user)
    print editfile_form.fields['front']
    #print editfile_form

    if request.method == "POST":
        if editfile_form.is_valid():
            editfile_form_uncommited = editfile_form.save(commit=False)
            editfile_form_uncommited.save()

            return redirect('/netdev/arquivo/%s/' % file_id)

    context_dict.update({'form':editfile_form})

    return render(request,'netdev/repository/repofile_edit.html', context_dict)

def view_file(request, file_id):

    context_dict = user_info(request)

    file = RepoFile.objects.get(id=file_id)

    context_dict.update({'file':file})

    return render(request, 'netdev/repository/repofile_detail.html', context_dict)

def delete_file(request, file_id):

    context_dict = user_info(request)

    file = RepoFile.objects.get(id=file_id)

    context_dict.update({'file': file})

    if request.POST:
        if 'file_id' in request.POST:
            file_ob = RepoFile.objects.get(id=request.POST['file_id'])
            file_ob.delete()
            return redirect('/netdev/meu_repositorio/')

    return render(request, 'netdev/repository/repofile_confirm_delete.html', context_dict)


def cat_show(request, cat_id):

    context_dict = user_info(request)

    category = FileCategory.objects.get(id=cat_id)
    files = RepoFile.objects.filter(category=category)

    context_dict.update({'category': category, 'files':files})

    return render(request, 'netdev/repository/files_per_category.html',context_dict)


def filecat_all(request):

    context_dict = user_info(request)

    categories = FileCategory.objects.filter(owner=request.user)

    context_dict.update({'categories': categories})

    return render(request, 'netdev/repository/filecat_all.html',context_dict)


