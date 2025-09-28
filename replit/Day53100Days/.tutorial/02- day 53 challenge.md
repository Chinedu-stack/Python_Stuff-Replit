# 👉 Day 53 Challenge

Your video game inventory system should:

1. Have a menu that allows the user to:
    1. Add
    2. View
    3. Remove
2. Adding an item saves it to a file using captalize mode. Duplicates are allowed.
3. Removing an item deletes it from the file.
3. View is trickier. It should output the name of the item and tell you *how many* of those items you have.
4. Use auto-save and auto-load with `try... except`.


Example:

```
🌟RPG Inventory🌟

1: Add  2: Remove  3: View  > 1

Input the item to add: > Mana potion
Mana potion has been added to your inventory.

1: Add  2: Remove  3: View  > 2

Input the item to remove: > Sword
Sword has been removed from your inventory.

1: Add  2: Remove  3: View  > 3

Input the item to view: > Wizard's sleeve
You have 2 Wizard's sleeve
```

<details> <summary> 💡 Hints </summary>
  
- Use the `count()` function when viewing an item.

</details>