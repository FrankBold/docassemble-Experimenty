from docassemble.base.util import *

def contains_spolek(x):
  x = x.lower()
  if "spolek" in x:
    return True
  elif "z.s." in x:
    return True
  elif "zapsaný spolek" in x:
    return True
  else:
    validation_error('Název spolku *musí* obsahovat "z.s.", "spolek", nebo "zapsaný spolek"')
  return

def string_pole(x):
  x = x.split('\r\n')
  return x