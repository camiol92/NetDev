__author__ = 'Cami'

import os
from datetime import datetime
import django

def populate():

    forum_general = add_forum('Geral',  'Forum para discussoes gerais')[0]
    forum_software = add_forum('Software', 'Forum para discossoes de SW')[0]
    forum_recruiting = add_forum('Recrutamento', 'Forum para divulgacaoo de vagas e curriculos')[0]
    forum_events = add_forum('Eventos', 'Forum para divulgacao e propostas de eventos')[0]
    forum_hardware = add_forum('Hardware', 'Forum para discossoes de HW')[0]

    subforum_hw_processors = add_subforum('Processadores', forum_hardware,  'Forum para discussao de processadores')[0]
    subforum_hw_platforms = add_subforum('Plataformas', forum_hardware,  'Forum para discussoes de plataformas')[0]
    subforum_hw_network = add_subforum('Redes', forum_hardware,  'Forum para discussoes de redes')[0]

    sub_geral_1 = add_subforum('Regras', forum_general, 'Subforum para Regras')[0]
    cat_geral_1 = add_category('Gerais', sub_geral_1, 'Categoria de Regras gerais')[0]
    moderador = add_user('moderador','moderador@netdev.com.br','mod','Moderador','Quartel General', 'Male')
    add_topic('Fixado', 'texto fixado', cat_geral_1, moderador)

    cat_intel = add_category('Intel', subforum_hw_processors,  'Forum para discutir processadores intel')[0]
    cat_amd = add_category('AMD', subforum_hw_processors,  'Forum para discussao de processadores AMD')[0]



    #topic_1 = add_topic('I3 e o melhor?','Comprei um i3 eh da hora?',subcat_i3,'Joao')[0]
    #topic_2 = add_topic('Pau no i3','O meu i3 deu pau quando fui instalar',subcat_i3,'Mirinha')[0]




    #
    # cat_intel = add_category('Intel', sub_hw_processors)
    # cat_amd = add_category('AMD', sub_hw_processors)
    # cat_arduino = add_category('Arduino', sub_hw_platforms)
    # cat_beagle = add_category('Beaglebone', sub_hw_platforms)
    # cat_raspberry = add_category('Raspberry Pi', sub_hw_platforms)
    # cat_wire = add_category('Cabo', sub_hw_network)
    # cat_wireless = add_category('Wireless', sub_hw_network)

    # add_topic(title='Bem Vindos',forum=general)
    # add_topic(title='About', forum=general)
    # add_topic(title='Discussao Geral', forum=general)
    #
    # project = add_forum('Projetos')[0]
    #
    # add_topic(name='Projetos Pessoais',forum=project)
    # add_topic(name='Projetos Profissionais', forum=project)
    #
    # recruiting = add_forum('Recrutamento')[0]
    #
    # add_topic(name='Para Empresas', forum=recruiting)
    # add_topic(name='Para Usuarios', forum=recruiting)

    for topic in Topic.objects.all():
        print topic

def add_forum(name, description):
    f = Forum.objects.get_or_create(name=name, description=description)
    return f

def add_subforum(name, forum,  description):
    s = SubForum.objects.get_or_create(name=name, forum=forum, description=description)
    return s

def add_category(name, subforum,description):
    c = Category.objects.get_or_create(name=name, subforum=subforum, description=description)
    return c


def add_topic(title, text, category, user):
    t = Topic.objects.get_or_create(title=title, text=text, category=category, views=0, replies=0, creation_date=datetime.now(), user=user)
    return t

def add_post(text, category, user):
    a = Post.objects.get_or_create(text=text, category=category, creation_date=datetime.now(), user=user)
    return a

def add_user(username, email, pwd, display, local, gender):
    user = User.objects.get_or_create(username=username, email=email, password=pwd, is_staff=False, is_superuser=False)
    user_profile = UserProfile.objects.get_or_create(user=user, display_name=display, gender=gender)
    public_profile = PublicProfile.objects.get_or_create(user=user)
    return user


if __name__ == '__main__':
    print "Starting Netdev population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
    django.setup()

    from netdev.models import Forum, SubForum, Category, Topic, Post, User, UserProfile, PublicProfile

    populate()