#!/usr/bin/env python3

from github import Github
import re, shutil
from git import Repo
import tempfile
from Grader import Grader
import pymysql

g      = Github()
dhs_cs = g.search_users("DHS-Computer-Science")[0]
repos = [i for i in dhs_cs.get_repos()
           if re.search("practice-\\d{4}-\\d{2}-.*", i.name)]


messages = ['not graded', 'complete', 'formatting error',
            'compile error', 'run time error', 'ran for too long',
            'outputs do not match', 'not started']


conn = pymysql.connect(host='127.0.0.1', user='dhs', passwd='titans', db='uva')

for repo in repos:
  tmp_dir = tempfile.mkdtemp()
  
  match = re.search('uva-hspc-practice-(\\d{4}-\\d{2})-(.*)$', repo.name)
  name = match.group(1)
  user = match.group(2)
  
  print("{} - {}".format(name, user))
  date = Repo.clone_from(repo.clone_url, tmp_dir).commit('HEAD').authored_date
  
  cur = conn.cursor()
  
  a = cur.execute("SELECT id,date,status FROM practice " \
                  "WHERE name = '{}' AND problem = '{}';".format(user, name))
  for i in cur:
    sql_id   = i[0]
    sql_date = i[1]
    sql_stat = i[2]
  
  if a == 0 or (sql_stat != 'complete' and int(sql_date) < date):
    sub = Grader(tmp_dir)
    stat = sub.run()

    if stat < 8:
      message = messages[stat]
    else:
      message = 'internal error 999'
      
    print(message)
    
    if a == 0:
      cur.execute("INSERT INTO practice (name, problem, status, date) " \
                  "VALUES ('{}','{}','{}','{}')".format(user,name,message,date))
    else:
      cur.zexecute("UPDATE practice SET status='{}', date='{}' WHERE id='{}';" \
                                                    .format(message, date, id))
    conn.commit()
  else:
    print('nothing to do')
  print()
  cur.close()
  shutil.rmtree(tmp_dir)
conn.close()