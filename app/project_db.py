from flask import url_for
from notanorm import SqliteDb

DB_FILE = "project_reviewal.db"

def upload_project(title, image, team_name, pmID, devoIDs, tags, repo, intro, descrip, rating, hosted_loc):
    db = SqliteDb(DB_FILE)

    devos = "|".join(devoIDs)
    tags = "|".join(tags)
    db.insert("projects", title=title, image=image, team_name=team_name, pmID=pmID, devoIDs=devos, tags=tags, repo=repo, intro=intro, descrip=descrip, rating=rating, hosted_loc=hosted_loc)

    project = db.select("projects", title=title, team_name=team_name, intro=intro)[-1]
    return project

def get_project_details(project_id):
    db = SqliteDb(DB_FILE)
    
    project = db.select("projects", project_id=project_id)[0]
    details = project
    details['devoIDs'] = project['devoIDs'].split("|")
    details['tags'] = project['tags'].split("|")

    return details

def get_project_snapshot(project_id):
    db = SqliteDb(DB_FILE)

    project = db.select("projects", project_id=project_id)[0]
    snapshot = {'image': project['image'], 'title': project['title'], 'team': project['team_name'], 'tags': project['tags'].split("|"), 'summary': project['intro'], 'project_id': project['project_id']}

    return snapshot

def edit_project_info(projectID, column_toEdit, new_val):
    db = SqliteDb(DB_FILE)

    db.update("projects", where={"project_id": projectID}, upd={column_toEdit: new_val})

def get_all_projects():
    db = SqliteDb(DB_FILE)

    return db.select('projects')

def get_all_project_ids():
    projects = get_all_projects()
    ids = []

    for project in projects:
        ids.append(project['project_id'])
    
    return ids

def delete_project(project_id):
    db = SqliteDb(DB_FILE)
    db.delete("projects", project_id=project_id)

def clear_projects_table():
    check = input("YOU ARE ABOUT TO DELETE EVERY ENTRY IN THE PROJECTS TABLE OF THE DATABASE. CONTINUE (Y/N): ")
    if check != "Y":
        return False
    db = SqliteDb(DB_FILE)
    db.delete_all("projects")

def clear_users_table():
    check = input("YOU ARE ABOUT TO DELETE EVERY ENTRY IN THE USERS TABLE OF THE DATABASE. CONTINUE (Y/N): ")
    if check != "Y":
        return False
    db = SqliteDb(DB_FILE)
    db.delete_all("users")