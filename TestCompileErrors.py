
import json
import subprocess
import pathlib
import pyparsing
import copy
import sys
import os
import itertools
from multiprocessing import Pool

from argparse import ArgumentParser

def GetCodeSnippets(file):
  flag = 'CHECK_COMPILE_FAILS('
  file = pathlib.Path(file)
  text = file.read_text()
  N = len(text)


  snippets = []
  pos = text.find(flag)

  while pos >= 0:

    depth = 1
    i = text.find('(',pos)+1
    while depth > 0 and i < N:
      if text[i] == '(':
        depth += 1

      if text[i] == ')':
        depth -= 1

      i += 1

    snippets.append({'range':(pos,i),'snippet':text[pos+len(flag):i-1]})

    pos = text.find(flag,pos+1)

  return snippets
    

def find_file(name):
  cpth = pathlib.Path(os.getcwd())
  for dir in itertools.chain([cpth], cpth.parents):
    if (dir/name).is_file():
      return dir/name
  return None

def try_to_compile(entry):
    should_fail = not pathlib.Path(entry['file']).stem.endswith('.0')
    ret = subprocess.run(entry['command'],shell=True,cwd=pathlib.Path(entry['directory']),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    test_failed = ret.returncode!=0 ^ should_fail
    message = { 'failed':test_failed,
                'reason':f'''Snippet in '{entry['file']}' should not have compiled, but it did.''',
                'returncode':ret.returncode,
                'output':ret.stdout.decode('utf-8'),
                'snippet': entry['snippet'],
                'command': entry['command'],
                'file': entry['file'],
                'original_snippet_location': entry['original_snippet_location'],
                }
    if not should_fail:
      message['reason'] = f'''Code without snippets in '{entry['file']}' should have compiled, but it did not.'''

    return message

def main():
  parser = ArgumentParser(description='Test that snippets of code do or do not compile.')

  parser.add_argument('--compile-database',
                      action='store',
                      dest='compile_database',
                      default='compile_commands.json',
                      help='The JSON compile database.'
                      )
  parser.add_argument('--verbose',
                      action='store_true',
                      help='Print result of all compile attempts..'
                      )

  args = parser.parse_args()




  database_file = find_file(pathlib.Path(args.compile_database))
  database = json.loads(database_file.read_text())

  scratch_dir = pathlib.Path('_TestCompile.tmp')
  if not scratch_dir.is_dir():
    scratch_dir.mkdir()

  new_database = []
  for entry in database:
    if 'file' in entry:
      file = pathlib.Path(entry['file'])
      snippets = GetCodeSnippets(file)

      if len(snippets) == 0:
        continue

      text = file.read_text()
      for i in range(-1,len(snippets)):
        tmp_file = scratch_dir / (file.stem+f'.{i+1}'+file.suffix)
        tmp_text = list()
        pos = 0
        for j in range(len(snippets)):
          tmp_text.append( text[pos:snippets[j]['range'][0]] )
          pos = snippets[j]['range'][1]
          if j == i:
            tmp_text.append( snippets[j]['snippet'])
          else:
            tmp_text.append( '')
        tmp_text.append( text[pos:] )

        tmp_file.write_text(''.join(tmp_text))

        new_entry = copy.deepcopy(entry)
        new_entry['file'] = str(tmp_file.absolute())
        new_entry['command'] = new_entry['command'].replace( entry['file'], new_entry['file'] )
        new_entry['original_snippet_location'] = f'''{str(file.absolute())}|{text[0:snippets[i]['range'][0]].count(os.linesep)+1}'''
        if i >= 0:
          new_entry['snippet'] = snippets[i]['snippet']
        else:
          new_entry['snippet'] = None

        new_database.append(new_entry)


  returncode = 0
  p = Pool()
  messages = p.map(try_to_compile,new_database)


  for message in messages:
    if message['failed']:
      returncode += 1
    if not args.verbose:
      if message['failed']:
        print('=Test Failed=')
        print('=============')
        print('Reason:',message['reason'])
        if message['returncode'] == 1:
          print('Command:',message['command'])
          print('Compiler Output:')
          print('v----------------------v')
          print(message['output'])
          print('^----------------------^')
        else:
          print('Command:',message['command'])
          print('Snippet:')
          print('v---------------------v')
          print(message['snippet'])
          print('^---------------------^')
          print('Original Snippet Location:', message['original_snippet_location'])
    else:
      print('File:',message['file'])
      print('Snippet:',message['snippet'])
      print('v---------------------v')
      print(message['snippet'])
      print('^---------------------^')
      print('Compiler Output:')
      print('v---------------------v')
      print(message['output'])
      print('^---------------------^')

  sys.exit(returncode)




if __name__ == '__main__':
  main()


