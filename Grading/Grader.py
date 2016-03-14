import subprocess
import tempfile
import fnmatch
import shutil
import time
import os, re

try:
  from subprocess import DEVNULL # py3k
except ImportError:
  import os
  DEVNULL = open(os.devnull, 'wb')

class Grader:
  def __init__(self, submission, timeout=60):
    #the file that will be compared against
    self.test_output = '{test}/in-out/judging.out'.format(test=submission)
    #the input file
    self.test_input  = '{test}/in-out/judging.in'.format(test=submission)
    #the file where the output will be writen
    self.outfile     = '{test}/output'.format(test=submission)

    #set the timeout
    self.timeout     = timeout

    #location to extract to
    self.submission_dir = submission

    #remove .class files
    for root, dirs, files in os.walk(self.submission_dir):
      for f in fnmatch.filter(files, '*.[cC][lL][Aa][sS][sS]'):
        os.remove(os.path.join(root, f))

    #the java file which will be run
    self.main_class  = (submission, 'Main')

  '''
  outputs:
    True:  compiled
    False: didn't
  '''
  def compile(self):
    mycmd = ['javac',
             os.path.join(self.main_class[0], self.main_class[1]+'.java')]
    tester = subprocess.Popen(mycmd,          stdin=subprocess.PIPE,
                              stdout=DEVNULL, stderr=subprocess.STDOUT)
    while tester.poll() is None:
      time.sleep(1)
    return tester.returncode == 0

  '''
  outputs:
    True:  good
    False: baad
  '''
  def compare(self):
    status = 6
    with open(self.outfile, 'r') as user, \
         open(self.test_output, 'r') as test:
      u_out   = user.read().replace('\r', '\r')
      correct = test.read().replace('\r', '\r')

    if u_out == correct:
      status = 1
    elif re.sub('([\\s\n:]+|0*(?:[0-9]+)(\\.\\d*)?)', '', u_out.lower()) == \
         re.sub('([\\s\n:]+|0*(?:[0-9]+)(\\.\\d*)?)', '', correct.lower()):
      status = 2
    return 7 if not u_out else status

  def get_dir(self):
    return self.submission_dir

  '''
  Values for result:
    0: not graded
    1: good(complete)
    2: formatting error
    3: compile error
    4: run time error
    5: ran for too long
    6: outputs do not match
    7: not started
    other: very very bad error
  '''
  def run(self):
    if not self.compile():
      return 3
    mycmd = ['java', '-classpath', self.main_class[0], self.main_class[1]]
    try:
      with open(self.outfile, 'w') as outfile, \
           open(self.test_input, 'r') as infile:
        start  = time.time()
        tester = subprocess.Popen(mycmd, stdin=infile,
                                  stdout=outfile, stderr=DEVNULL)
        while tester.poll() is None:
          if (time.time() - start) > float(self.timeout):
            tester.kill()
            return 5
          time.sleep(0.5)
      if tester.returncode != 0:
        return 4
      else:
        return self.compare() #change it if you don't like it
    except IOError as e:
      #Should not happen, I think
      #Note I should watch my language in school related projects
      #  but then again, who's gonna read this?
      print('Error: {}'.format(e.strerror))
      raise
      return 9999
