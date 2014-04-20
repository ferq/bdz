import sys
import itertools
choices = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789_$&#@ "
for length in range(0,20):
   for entry in itertools.product(choices,repeat = length):
      password = ''.join(entry)
      print password
      if password == '123':
         print 'I win'
         sys.exit(0)