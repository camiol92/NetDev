__author__ = 'Cami'
from django.conf.urls import patterns, url
from netdev import views
from django.conf import settings

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^sobre/$', views.about, name='about'),
        url(r'^repositorios/$', views.repositorys, name='repositorys'),
        url(r'^usuarios/$', views.users, name='users'),
        url(r'^perfil/$', views.profile, name='profile'),
        url(r'^perfil/(?P<username>\w+)/$', views.public_profile, name='public_profile'),
        url(r'^amigos/$', views.friends, name='friends'),
        url(r'^meus_topicos/$', views.my_topics, name='my_topics'),
        url(r'^caixa_de_entrada/$', views.inbox, name='inbox'),
        url(r'^caixa_de_saida/$', views.outbox, name='outbox'),
        url(r'^nova_mensagem/$', views.new_message, name='new_message'),
        url(r'^mensagem/(?P<message_id>\w+)/$', views.message, name='message'),
        url(r'^perfil/(?P<username>\w+)/adicionado/$', views.confirm_friendship, name='confirm_friendship'),
        url(r'^perfil/(?P<username>\w+)/removido/$', views.remove_friendship, name='remove_friendship'),
        url(r'^mudar_perfil/$', views.change_profile, name='change_profile'),
        url(r'^registrar', views.register, name='register'),
        url(r'^entrar/$', views.user_login, name='login'),
      #  url(r'^restrito/', views.restricted, name='restricted'),
        url(r'^forum/$', views.foruns, name='foruns'),
        url(r'^sair/$', views.user_logout, name='logout'),
        url(r'^forum/(?P<forum_name_url>\w+)/$', views.forum, name='forum'),
        url(r'^forum/(?P<forum_name_url>\w+)/(?P<subforum_name_url>\w+)/(?P<category_name_url>\w+)/novo_topico/$', views.add_topic, name='add_topic'),
        url(r'^forum/(?P<forum_name_url>\w+)/(?P<subforum_name_url>\w+)/(?P<category_name_url>\w+)/(?P<topic_id>\w+)/nova_resposta/$', views.add_post, name='add_post'),
        url(r'^forum/(?P<forum_name_url>\w+)/(?P<subforum_name_url>\w+)/$', views.subforum, name='subforum'),
        url(r'^forum/(?P<forum_name_url>\w+)/(?P<subforum_name_url>\w+)/(?P<category_name_url>\w+)/$', views.category, name='category'),
        url(r'^forum/(?P<forum_name_url>\w+)/(?P<subforum_name_url>\w+)/(?P<category_name_url>\w+)/(?P<topic_id>\w+)/$', views.topic, name='topic'),
        url(r'^forum/(?P<forum_name_url>\w+)/(?P<subforum_name_url>\w+)/(?P<category_name_url>\w+)/(?P<topic_id>\w+)/editar_topico/$', views.edit_topic, name='edit_topic'),
        url(r'^forum/(?P<forum_name_url>\w+)/(?P<subforum_name_url>\w+)/(?P<category_name_url>\w+)/(?P<topic_id>\w+)/editar_resposta/$', views.edit_post, name='edit_post'),
        url(r'^forum/(?P<forum_name_url>\w+)/(?P<subforum_name_url>\w+)/(?P<category_name_url>\w+)/(?P<topic_id>\w+)/remover_topico/$', views.remove_topic, name='remove_topic'),
        url(r'^forum/(?P<forum_name_url>\w+)/(?P<subforum_name_url>\w+)/(?P<category_name_url>\w+)/(?P<topic_id>\w+)/remover_resposta/$', views.remove_post, name='remove_post'),
    )

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
