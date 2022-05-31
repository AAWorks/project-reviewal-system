# Jimin: Alejandro Alonso (PM), Noakai Aronesty, Justin Zou, Ivan Lam
# SoftDev pd2
# P04 -- Smithy

from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug import *
import os

with open("app/db_builder.py", "rb") as source_file:
    code = compile(source_file.read(), "app/db_builder.py", "exec")
exec(code)
with open("app/db_funcs.py", "rb") as source_file:
    code = compile(source_file.read(), "app/db_funcs.py", "exec")
exec(code)
with open("app/project_db.py", "rb") as source_file:
    code = compile(source_file.read(), "app/project_db.py", "exec")
exec(code)

PROJECTS_UPLOAD_FOLDER = 'app/static/images/projects'
USERS_UPLOAD_FOLDER = 'app/static/images/users'
ALLOWED_EXTENSIONS = {'png'}

app = Flask(__name__)
app.secret_key = 'stuffins'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        return render_template("login.html")
    except:
        return render_template("error.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        return render_template("register.html")
    except:
        return render_template("error.html")


@app.route('/terms', methods=['GET', 'POST'])
def terms():
    with app.open_resource('static/terms.txt') as terms:
        terms_lines = [line.decode("utf8") for line in terms.readlines()]
    try:
        return render_template("terms.html", terms=terms_lines)
    except:
        return render_template("error.html")

# authetication of login


@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    ''' Checks whether method is get, post. If get method, then redirect to
       loginpage. If post, then authenticate the username and password, rendering
       the error page if incorrect and the response.html if correct username/pass. '''

    # Variables
    method = request.method
    stuy_username = request.form.get('stuy_username').lower()
    user_id = request.form.get('user_id')
    password = request.form.get('password')

    try:
        stuy_username = request.form.get('stuy_username').lower()
        user_id = request.form.get('user_id')
    except:
        return render_template('login.html', input="bad_user")

    try:
        password = request.form.get('password')
    except:
        return render_template('login.html', input="bad_pass")

    # Get vs Post
    if method == 'GET':
        return redirect(url_for('disp_home'))

    try:
        auth_state = auth_user(stuy_username, user_id, password)
    except:
        return render_template('login.html', input="bad_user")

    if auth_state == "bad_pass":
        return render_template('login.html', input="bad_pass")
    elif auth_state == "bad_user":
        return render_template('login.html', input="bad_user")
    elif auth_state == True:
        session['user_id'] = user_id
        return redirect(url_for('user_account', user_id=user_id))


@app.route("/rAuth", methods=['GET', 'POST'])
def rAuthenticate():
    ''' Authentication of username and passwords given in register page from user '''

    method = request.method
    firstname = request.form.get('firstname').title()
    lastname = request.form.get('lastname').title()
    stuy_username = request.form.get('stuy_username').lower()
    github = request.form.get('github')
    password0 = request.form.get('password0')
    password1 = request.form.get('password1')

    if method == 'GET':
        return redirect(url_for('register'))

    if method == 'POST':
        # error when no username is inputted
        if len(github) == 0:
            return render_template('register.html', given="github username")
        if len(stuy_username) == 0:
            return render_template('register.html', given="stuyvesant username")
        # error when no password is inputted
        elif len(password0) == 0:
            return render_template('register.html', given="password")
        elif len(password0) < 6:
            return render_template('register.html', given="password greater than 6 characters")
        # a username and password is inputted
        # a username and password is inputted
        else:
            # if the 2 passwords given don't match, will display error saying so
            if password0 != password1:
                return render_template('register.html', mismatch=True)
            else:
                # creates user account b/c no fails
                create_user(stuy_username, password0,
                            firstname, lastname, github, url_for('static', filename='images/users/default.png'))
                return render_template('login.html', input='success', user_id=get_latest_id(stuy_username))


@app.route("/edit")
def editProfile():
    # try:
    user = get_user(session['user_id'])
    details = get_details(session['user_id'])
    name = user["firstname"] + " " + user["lastname"]
    about_info = []
    about_last = ""
    if (details['about']):
        for i in details['about'].split('\r\n'):
            about_info.append(i)
        about_last = about_info[-1]
    print(about_info)
    return render_template("edit.html",
                           pfp=user['pfp'], 
                           first=user["firstname"].title(), 
                           name=name.title(), 
                           user_id=session['user_id'], 
                           stuyname=user["stuy_username"], 
                           github=user["github"], 
                           devo_status=user["devostatus"], 
                           about_info=about_info[:-1], 
                           about_last=about_last,
                           back_end_info=details['back_end'],
                           front_end_info=details['front_end'],
                           git_foo_info=details['git_foo'],
                           can_serve_info=details['can_serve'],
                           discord_name=details['discord_name'],
                           discord_id=details['discord_id'],
                           facebook_name=details['facebook_name'],
                           twitter_name=details['twitter_name'],
                           reddit_name=details['reddit_name'])
    # except:
    #     return render_template("error.html")


@app.route('/update_info', methods=['GET', 'POST'])
def update_info():
    method = request.method
    about_info = request.form.get('about_section')
    user_id = request.form.get('user_id')
    back_end_info = int(request.form.get('back_end_range'))
    front_end_info = int(request.form.get('front_end_range'))
    git_foo_info = int(request.form.get('git_foo_range'))
    can_serve_info = request.form.get('can_serve_select')
    discord_name = request.form.get('discord_name')
    discord_id = request.form.get('discord_id')
    facebook_name = request.form.get('facebook_name')
    twitter_name = request.form.get('twitter_name')
    reddit_name = request.form.get('reddit_name')

    print(can_serve_info)

    if method == 'GET':
        return redirect(url_for('disp_home'))

    if method == 'POST':
        print(about_info)
        if (discord_name and not discord_id) or (not discord_name and discord_id):
            return redirect(url_for('editProfile', discord_not_match='true'))
        else:
            edit_user_details(user_id, about_info, back_end_info, front_end_info, git_foo_info, can_serve_info,
                            discord_name, discord_id, facebook_name, twitter_name, reddit_name)
            return redirect(url_for('user_account', user_id=user_id))


@app.route("/logout")
def logout():
    ''' Logout user by deleting user from session dict. Redirects to loginpage '''
    # Delete user. This try... except... block prevent an error from ocurring when the logout page is accessed from the login page
    try:
        session.pop('user_id')
    except KeyError:
        return redirect(url_for('disp_home'))
    # Redirect to login page
    return redirect(url_for('disp_home'))


@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def disp_home():
    ''' Loads the landing page '''
    try:
        if session:
            return render_template("home.html", returning="Current user: " + get_full_username(session['user_id']))
        else:
            return render_template("home.html")
    except:
        return render_template("error.html")


@app.route("/account/<user_id>", methods=['GET', 'POST'])
def user_account(user_id):
    # try:

    user = get_user(user_id)
    details = get_details(user_id)
    name = user["firstname"] + " " + user["lastname"]

    about_info = []
    if (details['about']):
        for i in details['about'].split('\r\n'):
            about_info.append(i)
    
    if session:
        user_match = (int(session['user_id']) == int(user['user_id']))
    else:
        user_match = False

    return render_template("account.html",
                           user_id=user['user_id'], pfp=user['pfp'],
                           first=user["firstname"].title(),
                           name=name.title(),
                           stuyname=user["stuy_username"],
                           github=user["github"],
                           devo_status=user["devostatus"],
                           about_info=about_info,
                           back_end_info=details['back_end'],
                           front_end_info=details['front_end'],
                           git_foo_info=details['git_foo'],
                           can_serve_info=details['can_serve'],
                           discord_name=details['discord_name'],
                           discord_id=details['discord_id'],
                           facebook_name=details['facebook_name'],
                           twitter_name=details['twitter_name'],
                           reddit_name=details['reddit_name'],
                           user_match=user_match
                           )
    # except:
    #     return render_template("error.html")


@app.route("/devos", methods=['GET', 'POST'])
def devos():
    # try:
    # tester = {"name": "Thluffy Sinclair", "id": "tsinclair20", "bio": "A totally tubular devo to test the totally tubular devos page!",
    #           "pfp": url_for('static', filename="images/users/default.png")}
    # devos = []
    # for i in range(10):
    #     devo = {}
    #     devo["name"] = tester['name']
    #     devo["id"] = tester['id'] + "#" + str(i)
    #     devo["bio"] = tester["bio"]
    #     devo["pfp"] = tester["pfp"]
    #     devos.append(devo)

    devos = [
        {
            "name": (u.firstname + " " + u.lastname).title(),
            "user_id": u.user_id,
            "stuyname": u.stuy_username,
            "num_projs": len(get_project_ids(u.user_id)),
            "bio": get_details(u.user_id)["about"],
            "pfp": u.pfp
        } for u in get_users()
    ]
    return render_template("devos.html", devos=devos)
    # except:
    #     return render_template("error.html")


@app.route("/gallery", methods=['GET', 'POST'])
def gallery():
    try:
        project_ids = get_all_project_ids()
        project_snaps = []

        for project_id in project_ids:
            project_snaps.append(get_project_snapshot(project_id))

        return render_template("gallery.html", projects=project_snaps)
    except:
        return render_template("error.html")

@app.route("/project/<project_id>", methods=['GET', 'POST'])
def view_project(project_id):
    #try:
        project = get_project_details(project_id)

        pm_id = project['pmID'].split("#")[-1]
        pm = get_user(pm_id)
        pm_name=(pm['firstname'] + " " + pm['lastname']).title()

        devos=[]
        for full_devo_id in project['devoIDs']:
            devo_id = full_devo_id.split("#")[-1]
            devo_info = get_user(devo_id)
            devo = {'name': (devo_info['firstname'] + " " + devo_info['lastname']).title(), 'id': devo_id}
            devos.append(devo)

        if project['hosted_loc'].startswith("http://") or project['hosted_loc'].startswith("https://"):
            hosted = True
        else:
            hosted = False

        return render_template("project.html", title=project['title'], project_image=project['image'], team_name=project['team_name'], tags=project['tags'], project_descrip_1=project['intro'], project_descrip_2=project['descrip'], pm_id=pm_id, pm_name=pm_name, devos=devos, repo_link=project['repo'], hosted=hosted, hosted_loc=project['hosted_loc'])
    #except:
     #   return render_template("error.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    user = get_user(session['user_id'])
    if request.method == 'POST':
        app.config['UPLOAD_FOLDER'] = PROJECTS_UPLOAD_FOLDER
        cover_photo = request.files['project_image']
        #f2 = request.files['team_flag']
        # f2.save(secure_filename(f2.filename))
        devoIDs = [request.form.get('devo1'), request.form.get(
            'devo2'), request.form.get('devo3')]
        tags = ["Project " + request.form.get('project_num')]

        new_project = upload_project(request.form.get('title'), url_for('static', filename='images/projects/default.png'), request.form.get('team_name'), request.form.get(
            'pm_id'), devoIDs, tags, request.form.get('repo'), request.form.get('summary'), request.form.get('descrip'), 5, request.form.get('hosted_loc'))
        pid = new_project['project_id']

        if cover_photo.filename != "" and allowed_file(cover_photo.filename):
            filename = str(pid) + "_cover" + ".png"
            cover_photo.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            edit_project_info(pid, 'image', url_for(
                'static', filename='images/projects/' + filename))

    return render_template("upload_project.html", user_id=user)

if __name__ == "__main__":  # false if this file imported as module
    # enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
