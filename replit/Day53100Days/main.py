import os, time 
####---------------------AUTOSAVE---------------------------AUTOSAVE
try:
  ###3 autoload
  a = open("game.list","r")
  gamelist = eval(a.read())
  a.close()
except:
  gamelist = []
###-------------------------SUBROUTINES---------------------------------------SUBROUTINE

def add():
  item = input("Input item you want to add > ").capitalize()
  gamelist.append(item)
  print(f"{item} has been added to your inventory")


def view():
  item = input("Input item you want to view").capitalize()
  for items in gamelist:
    if item == items:
      num = gamelist.count(items)
      print(f"You have {num} {item}")
      break
    else:
      print(f"{item} was not found in you list")
      
def remove():
  item = input("What item do you want to remove > ")
  if item in gamelist:
    gamelist.remove(item)
  else:
    print(f"Sorry {item} isnt't in your list. Please ty again.")

def reset():
  time.sleep(3)
  os.system("clear")
  


####--------------------------MAIN LOOP----------------------------------MAIN LOOP
while True:
 menu = input("1. Add: \n2. View: \n3. Remove: \n").strip().lower()
 if menu == "1":
  add() ####create adding subroutine
  reset()
 elif menu == "2":
  view()  #### creat view subroutine
  reset()
 elif menu == "3":
  remove()  #### create view subroutine
  reset()
  
 else:
  print("Input not valid.Please try again")

###---------------------------AUTOSAVE-------------------------------------AUTOSAVE
  try:
   a = open("game.list","w")
   a.write(str(gamelist))
   a.close()
  except:
   print("something seems to be wrong nedu check it out")