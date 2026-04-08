#!/usr/bin/env python2.7

import os
import httplib2

import oauth2client
import apiclient
import flask

from uuid import uuid4
from flask import Flask, render_template, request, g
from models import users_model, index_model, teachers_model, students_model, \
        courses_model, model
from google.cloud import datastore


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = str(uuid4())



@app.before_request
def before_request():
    pass


@app.before_request
def teacher_session():
    if '/teacher/' in request.path:
        if 'credentials' not in flask.session:
            return flask.redirect(flask.url_for('index'))
        elif not flask.session['is_teacher']:
            return flask.redirect(flask.url_for('register'))


@app.before_request
def student_session():
    if '/student/' in request.path:

        if 'credentials' not in flask.session:
            return flask.redirect(flask.url_for('index'))
        elif not flask.session['is_student']:
            return flask.redirect(flask.url_for('register'))


# make sure user is authenticated w/ live session on every request
@app.before_request
def manage_session():
    # want to go through oauth flow for this route specifically
    # not get stuck in redirect loop
    if request.path == '/oauth/callback':
        return

    # allow all users to visit the index page without a session
    if request.path == '/' or request.path == '/oauth/logout':
        return

    # validate that user has valid session
    # add the google user info into session
    if 'credentials' not in flask.session:
        flask.session['redirect'] = request.path
        return flask.redirect(flask.url_for('oauth2callback'))


@app.teardown_request
def teardown_request(exception):
    pass

@app.route('/switch_type', methods=['POST'])
def switch_type():
    im = index_model.Index(flask.session['id'])
    if request.form['type'] == 'teacher':
        if im.is_teacher():
            return flask.redirect(flask.url_for('main_teacher'))
        else:
            return flask.redirect(flask.url_for('register'))

    elif request.form['type'] == 'student':
        if im.is_student():
            return flask.redirect(flask.url_for('main_student'))
        else:
            return flask.redirect(flask.url_for('register'))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    im = index_model.Index(flask.session['id'])
    if im.is_student():
        print flask.url_for('main_student')
        return flask.redirect(flask.url_for('main_student'))
    elif im.is_teacher():
        return flask.redirect(flask.url_for('main_teacher'))
    else:
        return render_template('login.html', not_registered=True)


@app.route('/student/', methods=['GET', 'POST'])
def main_student():
    sm = students_model.Students(flask.session['id'])
    courses = sm.get_courses()
    context = dict(data=courses)
    signed_in = True if sm.has_signed_in() else False

    if request.method == 'GET':
        return render_template(
                'main_student.html',
                signed_in=signed_in,
                **context)

    elif request.method == 'POST':
        if 'secret_code' in request.form.keys():
            provided_secret = request.form['secret_code']
            actual_secret, seid = sm.get_secret_and_seid()
            if int(provided_secret) == int(actual_secret):
                sm.insert_attendance_record(seid)
                valid = True
            else:
                valid = False

            return render_template(
                    'main_student.html',
                    submitted=True,
                    valid=valid,
                    **context)


@app.route('/teacher/', methods=['GET', 'POST'])
def main_teacher():
    tm = teachers_model.Teachers(flask.session['id'])

    if request.method == 'POST':
        cm = courses_model.Courses()
        if "close" in request.form.keys():
            cid = request.form["close"]
            cm.cid = cid
            cm.close_session(cm.get_active_session())
        elif "open" in request.form.keys():
            cid = request.form["open"]
            cm.cid = cid
            cm.open_session()

    courses = tm.get_courses_with_session()
    empty = True if len(courses) == 0 else False
    context = dict(data=courses)
    return render_template('main_teacher.html', empty=empty, **context)


@app.route('/teacher/add_class', methods=['POST', 'GET'])
def add_class():
    tm = teachers_model.Teachers(flask.session['id'])

    if request.method == 'GET':
        return render_template('add_class.html')

    elif request.method == 'POST':
        # first check that all unis are valid
        um = users_model.Users()
        for uni in request.form['unis'].split('\n'):
            uni = uni.strip('\r')
            # always reads at least one empty line from form
            if not uni:
                continue
            if not um.is_valid_uni(uni):
                return render_template('add_class.html', invalid_uni=True)

        # then create course and add students to course
        course_name = request.form['classname']
        cid = tm.add_course(course_name)
        cm = courses_model.Courses(cid)

        for uni in request.form['unis'].split('\n'):
            uni = uni.strip('\r')
            cm.add_student(uni)

        return flask.redirect(flask.url_for('main_teacher'))


@app.route('/teacher/remove_class', methods=['POST', 'GET'])
def remove_class():
    tm = teachers_model.Teachers(flask.session['id'])

    # show potential courses to remove on get request
    if request.method == 'GET':
        courses = tm.get_courses()
        context = dict(data=courses)
        return render_template('remove_class.html', **context)

    # remove course by cid
    elif request.method == 'POST':
        cid = request.form['cid']
        tm.remove_course(cid)
        return flask.redirect(flask.url_for('main_teacher'))


@app.route('/teacher/view_class', methods=['POST', 'GET'])
def view_class():
    if request.method == 'GET':
        flask.redirect(flask.url_for('main_teacher'))

    elif request.method == 'POST':
        cm = courses_model.Courses()

        if 'close' in request.form.keys():
            cid = request.form['close']
            cm.cid = cid
            cm.close_session(cm.get_active_session())
        elif 'open' in request.form.keys():
            cid = request.form['open']
            cm.cid = cid
            cm.open_session()
        else:
            cid = request.form['cid']
            cm.cid = cid

        res = 0
        uni = None
        if 'add_student' in request.form.keys():
            uni = request.form['add_student']
            res = cm.add_student(uni)
        elif 'remove_student' in request.form.keys():
            uni = request.form['remove_student']
            res = cm.remove_student(uni)

        course_name = cm.get_course_name()
        secret = cm.get_secret_code()
        num_sessions = cm.get_num_sessions()
        students = cm.get_students()
        students_with_ar = []
        for student in students:
            sm = students_model.Students(student['id'])
            student_uni = sm.get_uni()
            num_ar = sm.get_num_attendance_records(cid)
            students_with_ar.append([student, student_uni, num_ar])

        context = dict(students=students_with_ar)
        return render_template(
                'view_class.html',
                cid=cid,
                secret=secret,
                course_name=course_name,
                num_sessions=num_sessions,
                uni=uni,
                res=res,
                **context)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template(
                'register.html',
                name=flask.session['google_user']['name'],
                is_student=flask.session['is_student'],
                is_teacher=flask.session['is_teacher']
        )

    elif request.method == 'POST':
        m = model.Model()
        ds = m.get_client()
        if request.form['type'] == 'student':
            # check that uni doesn't already exist
            # if it doesn't, continue student creation
            um = users_model.Users()
            if not um.is_valid_uni(request.form['uni']):
                key = ds.key('student')
                entity = datastore.Entity(
                    key=key)
                entity.update({
                    'sid': flask.session['id'],
                    'uni': request.form['uni']
                })
                ds.put(entity)

                flask.session['is_student'] = True
                return flask.redirect(flask.url_for('main_student'))
            else:
                return render_template(
                        'register.html',
                        name=flask.session['google_user']['name'],
                        invalid_uni=True)

        else:
            try:
                key = ds.key('teacher')
                entity = datastore.Entity(
                    key=key)
                entity.update({
                    'tid': flask.session['id']
                })
                ds.put(entity)
                flask.session['is_teacher'] = True
            except:
                pass
            return flask.redirect(flask.url_for('main_teacher'))


@app.route('/oauth/callback')
def oauth2callback():
    flow = oauth2client.client.flow_from_clientsecrets(
        'client_secrets_oauth.json',
        scope=[
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri=flask.url_for('oauth2callback', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()

        # use token to get user profile from google oauth api
        http_auth = credentials.authorize(httplib2.Http())
        userinfo_client = apiclient.discovery.build('oauth2', 'v2', http_auth)
        user = userinfo_client.userinfo().v2().me().get().execute()

        # TODO only allow columbia.edu emails
        # if 'columbia.edu' not in user['email']:
        #     return flask.redirect(flask.url_for('bademail'))

        um = users_model.Users()

        flask.session['google_user'] = user
        flask.session['id'] = um.get_or_create_user(user)

        # now add is_student and is_teacher to flask.session
        im = index_model.Index(flask.session['id'])
        flask.session['is_student'] = True if im.is_student() else False
        flask.session['is_teacher'] = True if im.is_teacher() else False

        redirect = flask.session['redirect']
        flask.session.pop('redirect', None)
        return flask.redirect(redirect)


@app.route('/oauth/logout', methods=['POST', 'GET'])
def logout():
    flask.session.clear()
    return flask.redirect(flask.url_for('index'))
