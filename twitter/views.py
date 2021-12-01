from django.shortcuts import render, redirect
from .models import *
from .forms import UserRegisterForm, PostForm, UserUpdateForm, ProfileUpdateForm 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
	if request.user.is_authenticated==False:
		return redirect('register')
	else:	
		posts = Post.objects.all()
		profile = Profile.objects.get(user=request.user)
		user = User.objects.get(username=request.user)
		userprofile= profile.followers()
		if Profile.objects.filter(user=user).exists()==False:
			profile = Profile(user=user)
			profile.save()
			

			return redirect('home')

		elif request.method == 'POST':
			form = PostForm(request.POST)

			if form.is_valid():
				post = form.save(commit=False)
				post.user = request.user
				post.save()
				
				return redirect('home')
		else:
			form = PostForm()

		context = {'posts':posts, 'profile': profile, 'userprofile': userprofile, 'form' : form }
		return render(request, 'twitter/newsfeed.html', context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			

			return redirect('home')
	else:
		form = UserRegisterForm()

	context = {'form' : form}
	return render(request, 'twitter/register.html', context)


def delete(request, post_id):
	post = Post.objects.get(id=post_id)
	post.delete()
	return redirect('home')


def profile(request, username):
	user = User.objects.get(username=username)
	profile = Profile.objects.get(user=user)
	if request.user.is_authenticated==False:
		return redirect('register')
		
	else:
		userprofile= profile.followers()
		posts = user.posts.all()
		context = {'user':user, 'userprofile': userprofile, 'posts':posts}
		return render(request, 'twitter/profile.html', context)


def editProfile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user) #llenar el formulario con informacion que ya tiene
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('home')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm()

	context = {'u_form': u_form, 'p_form' : p_form}
	return render(request, 'twitter/edit.html', context)

def follow(request, username):
	current_user = request.user  #obtener el usuario que esta en sesion
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = RelationShip(from_user=current_user, to_user=to_user_id)  #el ususario que va a seguir / usuario que es seguido
	rel.from_user=current_user
	rel.to_user=to_user_id
	if rel.from_user==rel.to_user:
		return redirect('home')
	else:
		rel.save()
		return redirect('home')

def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = RelationShip.objects.get(from_user=current_user.id, to_user=to_user_id)
	rel.delete()
	return redirect('home')

def likepost(request, pk):
    user = request.user
    if request.method == 'GET':
    
        post_obj = Post.objects.get(id=pk) #post1
        profile = Profile.objects.get(user=user) #usuario que le dio like

        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)  #si es el usuario ya existe significa un deslike por lo tanto se borra
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=pk)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()

        # data = {
        #     'value': like.value,
        #     'likes': post_obj.liked.all().count()
        # }

        # return JsonResponse(data, safe=False)
    return redirect('home')