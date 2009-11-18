#encoding=utf-8
from django.http import HttpResponseRedirect, get_host
from django.shortcuts import render_to_response
import settings
import json
import models
import facebook


def authorize_app(request):
    #return render_to_response('authorize_app.html', {'api_key': settings.FACEBOOK_API_KEY, 
    #                                                 'perms': 'publish_stream,offline_access',
    #                                                 'next_url': 'http://' + get_host(request) + '/set-facebook-info/'})
    return HttpResponseRedirect("http://www.facebook.com/login.php?api_key=%s&connect_display=popup&v=1.0&next=%s&cancel_url=http://www.facebook.com/connect/login_failure.html&fbconnect=true&return_session=true&req_perms=%s"%(str(settings.FACEBOOK_API_KEY), 'http://' + get_host(request) + '/set-facebook-info/', "publish_stream,offline_access"))
    
def set_facebook_info(request):
    session_info = json.loads(request.GET.get('session', ''))
    user = None
    
    try:
        user = models.FacebookUser.objects.get(fb_uid=str(session_info['uid']))
    except models.FacebookUser.DoesNotExist:
        user = models.FacebookUser(fb_uid=str(session_info['uid']), 
                                   session=session_info['session_key'], 
                                   secret=session_info['secret'])
        user.save()
    
    return HttpResponseRedirect('/profile/' + str(session_info['uid']))

def show_facebook_profile(request, uid):
    user = models.FacebookUser.objects.get(fb_uid=uid)
    
    fb = facebook.Facebook(api_key=settings.FACEBOOK_API_KEY, secret_key=user.secret)
    
    fb.session_key = user.session
    
    info = fb.users.getInfo([user.fb_uid], ['name', 'birthday_date', 'pic_big_with_logo', 
                                                    'sex', 'hometown_location'])[0]
    
    if info['hometown_location']:
        country =  info['hometown_location']['country']
        city = info['hometown_location']['city']
        
    friends = fb.friends.get()
    friends = fb.users.getInfo(friends[0:10], ['name', 'birthday', 'relationship_status'])
    
    friend_list = []
    for friend in friends:
        friend_list.append(friend['name'] + ' cumple el ' + friend['birthday'] + ' y est&aacute; ' + friend['relationship_status'])
    
    return render_to_response('profile.html', {'pic':info['pic_big_with_logo'], 'name':info['name'], 
                                               'bday':info['birthday_date'],'sex':info['sex'], 
                                               'country':country,'city':city, 'friends': friend_list, 'uid':uid})

def set_status(request, uid):
    if request.method == "POST":
        user = models.FacebookUser.objects.get(fb_uid=uid)
    
        fb = facebook.Facebook(api_key=settings.FACEBOOK_API_KEY, secret_key=user.secret)
    
        fb.session_key = user.session
        
        fb.users.setStatus(status=request.POST['status'], clear=False, uid=int(uid))
    
    return HttpResponseRedirect('/')
    