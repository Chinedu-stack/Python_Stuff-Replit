# Solution (No Peeking!)
![](https://www.youtube.com/watch?v=vKiPT8UGv4A)

<details> <summary> 👀 Answer </summary>

```python
import os, time
inventory = []

try:
  f = open("inventory.txt", "r")
  inventory = eval(f.read())
  f.close()
except:
  pass

def addItem():
  time.sleep(1)
  os.system("clear")
  print("INVENTORY")
  print("=========")
  print()
  item = input("Item to add > ").capitalize()
  inventory.append(item)
  print("Added")

def viewItem():
  time.sleep(1)
  os.system("clear")
  print("INVENTORY")
  print("=========")
  print()
  seen = []
  for item in inventory:
    if item not in seen:
      print(f"{item} {inventory.count(item)}")
      seen.append(item)

  time.sleep(2)

def removeItem():
  time.sleep(1)
  os.system("clear")
  print("INVENTORY")
  print("=========")
  print()
  item = input("Item to remove > ").capitalize()
  if item in inventory:
    inventory.remove(item)
    print("Removed")
  else:
    print("You don't have that item")


while True:
  time.sleep(1)
  os.system("clear")
  print("INVENTORY")
  print("=========")
  print()
  menu = input("1: Add\n2: View\n3: Remove\n> ")
  if menu=="1":
    addItem()
  elif menu=="2":
    viewItem()
  else:
    removeItem()

  f = open("inventory.txt", "w")
  f.write(str(inventory))
  f.close()

```

</details>

- Join our [100 Days Community](https://replit.com/100-days-help)
- Join our [Discord](https://replit.com/discord)
- Want [live support?](https://replit.com/replit-101)