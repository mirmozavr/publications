from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
import sqlite3

from momo import settings
from web.models import Publication


def index(request):
    return render(request, 'main.html')


def contacts(request):
    return render(request, 'contacts.html')


def delete_task(conn, id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        # date = request.POST.get('date')
        text = request.POST.get('text')
        password = request.POST.get('password')

        if password == '456' and title:
            print('hmmmm')
            Publication.objects.deletion(id=title)

        if password != '123':
            return render(request, 'post.html', {'error': 'wrong password'})
        if title and text:
            Publication.objects.create(title=title, text=text)
            return redirect('/publications')
        else:
            return render(request, 'post.html', {'error': 'title and text must not be empty'})

    return render(request, 'post.html')


def publications(request):
    publications_sorted = Publication.objects.order_by('-date')
    return render(request, 'publications.html', {'publications': publications_sorted})


def publication(request, pub_id):
    try:
        publication = Publication.objects.get(id=pub_id)
    except Publication.DoesNotExist:
        return redirect('/')
    return render(request, 'publication.html', {'publication': publication})


def status(request):
    return HttpResponse('status OK.')
