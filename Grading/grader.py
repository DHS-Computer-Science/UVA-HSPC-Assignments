#!/usr/bin/env python3

from github import Github
import re, shutil
from git import Repo
import tempfile
from Grader import Grader
import pymysql, datetime
import os

if os.path.exists('.auth'):
  with open('.auth', 'r') as f:
    g  = Github(*[i for i in f.read().splitlines() if i][:2])
else:
  g    = Github()

requests = g.rate_limiting

dhs_cs = g.get_organization("DHS-Computer-Science")
repos  = [i for i in dhs_cs.get_repos()
             if re.search("practice-\\d{4}-\\d{2}-.*", i.name, re.I)]


messages = ['not graded', 'complete', 'formatting error',
            'compile error', 'run time error', 'ran for too long',
            'outputs do not match', 'not started']


conn = pymysql.connect(host='127.0.0.1', user='dhs', passwd='titans', db='uva')

users = {}

for repo in repos:
  match = re.search('uva-hspc-practice-(\\d{4}-\\d{2})-(.*)$', repo.name, re.I)

  name  = match.group(1)
  login = match.group(2).lower()

  if login not in users.keys():
    tmp   = g.get_user(match.group(2))
    user  = g.get_user(match.group(2)).name #for the people that have a name

    if not user:                            #for those that do not
      user = match.group(2)

    users[login.lower()] = user
  else:
    user = users[match.group(2).lower()]

  print("{} - {}({})".format(name, user, match.group(2)))
  lm = repo.get_commit('HEAD').last_modified
  date = datetime.datetime.strptime(lm, '%a, %d %b %Y %H:%M:%S %Z').timestamp()

  cur = conn.cursor()

  a = cur.execute("SELECT id,date,status,name FROM practice " \
                  "WHERE login = '{}' AND problem = '{}';".format(login, name))
  for i in cur:
    sql_id   = i[0]
    sql_date = i[1]
    sql_stat = i[2]
    sql_name = i[3]

  if a != 0 and sql_name != user:
    cur.execute("UPDATE practice SET name = '{}' WHERE id='{}';" \
                .format(user, sql_id))
    conn.commit()

  if a == 0 or (sql_stat != 'complete' and float(sql_date) < date):
    tmp_dir = tempfile.mkdtemp()
    Repo.clone_from(repo.clone_url, tmp_dir)
    sub = Grader(tmp_dir)
    stat = sub.run()

    if stat < 8:
      message = messages[stat]
    else:
      message = 'internal error 999'

    print(message)

    if a == 0:
      cur.execute("INSERT INTO practice (name, login, problem, status, date) " \
                  "VALUES ('{}', '{}', '{}', '{}', '{}')"\
                  .format(user, login, name, message, date))
    else:
      cur.execute("UPDATE practice SET status='{}', date='{}' WHERE id='{}';" \
                                                .format(message, date, sql_id))
    shutil.rmtree(tmp_dir)
    #print(tmp_dir)
    conn.commit()
  else:
    print('nothing to do')

  print()
  cur.close()
conn.close()

time= datetime.datetime.fromtimestamp(g.rate_limiting_resettime).isoformat(' ')

used       = requests[0] - g.rate_limiting[0]
left,limit = g.rate_limiting

print('Used {} api requests, {}/{} left, will reset at: {}'.format(
          used,            left,limit,                 time))
