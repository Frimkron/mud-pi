# Contributing to MuddySwamp

Thank you for helping out with the Open Source Club's MuddySwamp project!

Following these guidelines helps us keep good project workflow. We appreciate you working with us on it.

Please read our [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) to understand our community expectations. Check out our [discord](https://discord.gg/SCqmG3x) for any additional questions or just to hangout!

# How do I help?

Please check the **[Projects](https://github.com/ufosc/MuddySwamp/projects)** and **[Issues](https://github.com/ufosc/MuddySwamp/issues)** pages for current tasks. If you see something that you would like to help with, ask about helping in a comment and we'll assign it too you. If you're just starting out, checkout our **[beginner friendly](https://github.com/ufosc/MuddySwamp/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22)** issues for ways to help. 

Checkout the [DESIGN.md](./DESIGN.md) file for a high level explanation of the project.

# Report Bug 

Check to see if someone already reported this [bug](https://github.com/ufosc/MuddySwamp/issues). If so then leave a comment on that issue. If not, please provide a detailed description of the bug. Include what was happening before the error, all settings, and test results. This helps us more quickly identify and solve any problems. **[Create an Issue](https://github.com/ufosc/MuddySwamp/issues/new)** with the description and add a bug label. We will do our best to respond quickly to it. 

## Testing on your own Server

To test server code on your own machine, run

	python MuddySwamp.py

Then with a telnet client, you will connect to the following IP like so:

	telnet 127.0.0.1 1234

For contributors working on server code, make sure you test changes like so before submitting changes.
# Request a Feature

Check to see if the feature is already listed in our [TODO.md](./TODO.md). If it's not, describe the feature and why it would be beneficial. **[Create an Issue](https://github.com/ufosc/MuddySwamp/issues/new)** with this description and add a feature enhancement label. We will do our best to respond quickly to it. 


### Submit Changes 

1. Create a fork or branch to tackle a specific issue 
	- Team members branch off of dev and follow this [guide](https://guides.github.com/introduction/flow/) 
	- Others make a [fork](https://guides.github.com/activities/forking/)
  	- Name it after the issue or feature you are working on
2. Follow the style guidelines below 
	- This helps with debugging and working on the project
3. Make small incremental commits
	- It's easier to find issues when only a small amount of code is changed
4. Run and pass tests
5. Make a pull request 
	- The request will be reviewed
	- Any needed changes will be noted 
6. The changes will be added to the project 
	- Yay! Thank you so much for helping out

# Contributing Code and Assets
Please read [DESIGN.md](./DESIGN.md) before you contribute code. Any inquiries are appreciated.
## Style Guide 

Use our **[.editorconfig](./.editorconfig)** to help automatically format your code. A short list of what we require.

For a longer more descriptive list, check out our club's **[general style guidelines](https://github.com/ufosc/resources/blob/master/coding-guidelines/general-style.md)**.


Python is meant to be a **readable**. We try to follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) and ask that you do so as well. It is worth reading, but here are key highlights.

### Naming Conventions
- Package / Module names:
    - lowercase
    - e.g.: alphabet, string_builder
- Class names:
    - CapWords
    - e.g. EventType, PlayerQueue
- Function and variable names:
    - lowercase_with_underscores:
    - e.g. my_circle, export_data()
- Global variables:
    - same as functions
- Constants:
    - ALL _CAPS
    - e.g. MAX_WIDTH, TOTAL

### Commenting
Good python code is self-documenting. Block comments are encouraged, but **avoid** inline comments. Examples:
```
def function(x):
    print(x) #inline comments look like this
    return(x +1)    
```
Use docstrings to add automatic documentation to modules, classes, and functions. You can call an object's docstring with `.__doc__` Example:
```
>>> from location import Exit
>>> print(Exit.__doc__)
Class representing an Exit
    Exits link a set of names with a particular location
    Contains:
        a list of strings [exit names]
        location [the location this points to]
    The list can be accessed by treating the this as an iterable
	...
```
More on docstrings can be found with [PEP 257](https://www.python.org/dev/peps/pep-0257/).

### Line Limit
Keep lines under 80 characters. See PEP 8 for explanations on how to handle a long line. 

## MuddySwamp - Creating a Location
Creating a location in MuddySwamp is easy. They are stored using the .json format, at you can refer to the locations [template](./locations/template) for reference.

A location's description is at the foundation of a text-based world. Here are a few words of advice:

- Use imagery
- Be brief and clear, avoid demonstratives and other clunky phrases
  - "In the corner, there is a bucket."  -> "In the corner, **sits** a bucket."
- Be Descriptive
  - "In the **shadowy** corner, sits a **gross** bucket."
- Show, don't tell
  - "In the shadowy corner, sits a bucket **caked in God knows what**."
- Action verbs are prefered over linking verbs (again, show don't tell)
  - "The boy is cold." -> "The boy **shivers**". 
- Vary your sentence structure
  - Bad:    "The boy and the girl played in the park. They were happy because they saw a dog. The boy was secretly in love."
  - Better: "The boy and the girl played in the park. Because they saw a dog, they were happy. Secretly, the boy was in love."
- Vary sentence length
  - Bad: "The prisoner's vision faded. He felt numbness. He saw past memories. He was going to die."
  - Better: "The prisoner's vision faded. He trembled and lost feeling in his limbs. Memories-his fifth birthday cake, his first kiss, his mother's tears at the trial-all flashed before him. He was going to die. 
- 3-4 sentences max (players will be reading these many times. More locations with short descriptions > less locations with long descriptions.)

## MuddySwamp - Creating a CharacterClass
Distinct characters are a cornerstone of this engine's gameplay. CharacterClasses provide a rich and easy way to write classes for in-game characters, with virtually no restrictions. Any python code can be included in a CharacterClass.

### CharacterClasses: more than just a class

In the [character module](./character.py), there are two important definitions.

1) The CharacterClass metaclass
2) The Character class

A metaclass can best be explained like this:

* Gandalf the Grey, Dumbledore, and Hannibal Traven are instances of Wizard 
* Wizard is a class, specifically, a CharacterClass

Without diving into the implementation too much, the CharacterClass metaclass changes the way ChracterClasses work, adding a few key features. These 'CharacterClasses' are more than just standard classes. Most importantly: any function prefixed with `cmd_` will be made accessible to the reader for direct execution. (More on this later.) 

To the user, writing a CharacterClass is the same as writing a normal class. 

In practice, the user simply inherits from the Character base class. By inheriting from the Character base class, their class will be a CharacterClass. 

### Example
Here is an example:

```python
from character import Character

class Wizard(Character):
  def __str__(self):
      '''overriding the str() function'''
      return self.name + "the Wizard"

  def _level_check(self):
      '''internal method to check level'''
      if len(self.spells > self.level * 5):
          self.level += 1
  
  def add_spell(self, spell):
    '''add a spell, making it available to this wizard'''
    self.spells = spell
  
  def cmd_cast(self, spell):
    '''usage: cast [spellname] [arguments]
    Cast [spellname] with arguments. Arguments very by spell.
    '''
    if spell in self.spells:
        # cast the spell
        spell(args)
    else:
        raise Exception("You do not have that spell.")
    
  def cmd_spells(self, input_str):
      '''usage: spells [spells]
      List your spells.'''
      if len(self.spells)  == 0:
        self.message("You have no spells.")
      for spell in self.spells:
        self.message(str(spell))
```

When a user becomes a Wizard, they will see this:


```
Welcome to MuddySwamp!
You are a(n): Wizard

What is your name?
>>>Bill

Announcement: Welcome to the server, Bill the Wizard!
>>> help

Type "help [command]" for specific information.
Commands available:
[PLAYER COMMANDS]
help  say  tell  walk  report
[WIZARD COMMANDS]
cast
>>> help cast

usage: cast [spellname] [arguments]
Cast [spellname] with arguments. Arguments very by spell. 

>>> cast fireball

Error: You do not have that spell.
>>> help spells

You have no spells.
```

First of all, notice how our class inherits from `Character`. This **must** be done for it to be viable. 

Let's look at the functions here:
 - `__str__` is a special method that hooks into a top level function. In this case, str(). You can read about those [here](https://docs.python.org/3/reference/datamodel.html).
 - `_level_check` is an internal method, which signals to other programmers that this method should not be called outside the class. (C++/Java programmers, think `private`).
 - `add_spell` is a normal method, intended to be executed anywhere.
 - `cmd_cast` and `cmd_spells` are commands, which can be executed anywhere, or **executed by the user as shown above**.

Remember, `cmd_` commands are what makes CharacterClasses special. By adding `cmd_cast` and `cmd_spells`, we have given the users two commands, `cmd_cast` and `cmd_spells`. We can implement them however we want, but there are a few restrictions:

First, you must accept at least one argument, expecting it to be a string. If the user exectutes:

```
>>> cast fireball
```

It is the same as executing:

```python
wizard1.cmd_cast("fireball")
```
(assuming wizard1 is the name of the object)

Next, Take note of the use of doc-strings. This is good python practice (see above). But more importantly, this **MUST** be done for `cmd_` functions. If we look at the help menus in the example above, you we will see that they are *generated from the the doc-strings*. Not only is it good practice, but it is vital for player experience!

Finally, note how the exception handling works. For right now, all exceptions that occur in the body of a `cmd_` function are sent to the player. This will be fixed later (likely introducing a PlayerException). For right now, know that you can (and should) use Exceptions as a quick way to send error messages to the player.


### An improved example
Now, this class won't work for a few reasons:
* self.spells has not been initialized
* self.level has not been initialized

I will make a list later describing all the built-in features of Character, but for right now, just take my word for it.

Realize that, any time you add some new data field, you have to initalize it. We have no reason to make a spells data field in the base class, because not all classes use spells. So, we need to fix this by adding an `__init__`.

```python
from character import Character

class Wizard(Character):
  def __init__(self, controller):
      self.spells = {}
      self.level = 1
      super().__init__(controller)

  def __str__(self):
      '''overriding the str() function'''
      return self.name + "the Wizard"

  def _level_check(self):
      '''internal method to check level'''
      if len(self.spells > self.level * 5):
          self.level += 1

  def update(self):
      self._level_check()
      super().update()

  def add_spell(self, spell):
    '''add a spell, making it available to this wizard'''
    self.spells[spell.name] = spell
  
  def cmd_cast(self, spell):
    '''usage: cast [spellname] [arguments]
    Cast [spellname] with arguments. Arguments very by spell.
    '''
    if spell in self.spells:
        # cast the spell
        spell(args)
    else:
        raise Exception("You do not have that spell.")
    
  def cmd_spells(self, input_str):
      '''usage: spells [spells]
      List your spells.'''
      if len(self.spells)  == 0:
        self.message("You have no spells.")
      for spell in self.spells:
        self.message(str(spell))
```

Comments on the `__init__`: you must accept a controller as an argument. This is what gives players the ability to control this character, and it is passed in at creation. Next, you **must** call `super().__init__(controller)`. This will call the constructor for the base class, Character, and allow it to do the work that it needs to do. 

Also note: I added in an `update` method. This is overriding a method in the Character class, which you can expect to be called periodically. If you have a functon, in this case, `_level_check`, to be called periodically, then we should put it here. 

### The More Classes the Better
There is still a problem: what the heck is a spell? Let's create a class!

```python
class Spell:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect
    
    def __str__(self):
        return self.name

    def __eq__(self, other):
        # overriding the == operator
        # will also affect 'in' operator
        try:
            return self.name == other.name
        except AttributeError:
            return self.name == other

    def __call__(self, target=None):
        # this makes the spell object callable
        # i.e. typing spell(target) means spell.__call__(target)
        effect(target)


class Wizard(Character):
  def __init__(self, controller):
      self.spells = {}
      self.level = 1
      super().__init__(controller)

  def __str__(self):
      '''overriding the str() function'''
      return self.name + "the Wizard"

  def _level_check(self):
      '''internal method to check level'''
      if len(self.spells > self.level * 5):
          self.level += 1

  def update(self):
      self._level_check()
      super().update()

  def add_spell(self, spell):
    '''add a spell, making it available to this wizard'''
    self.spells[spell.name] = spell
  
  def cmd_cast(self, input_str):
    '''usage: cast [spellname] [arguments]
    Cast [spellname] with arguments. Arguments very by spell.
    '''
    spell = input_str.split(" ")[0]
    target_name = input_str.split(" ")[1]
    target = None
    for charcter in self.location.char_list:
        if character == target_name:
            target = self.location.players
    if spell in self.spells:
        # cast the spell
        self.spells(target)
    else:
        raise Exception("You do not have that spell.")
    
  def cmd_spells(self, input_str):
      '''usage: spells [spells]
      List your spells.'''
      if len(self.spells)  == 0:
        self.message("You have no spells.")
      for spell in self.spells:
        self.message(str(spell))
```

So, I wrote a sample spell class. In reality, you should make it far more robust. What about different kinds of spells? Should there always be a target? The cast command in particular has a few issues, but this is just a demo. 

Now to make the magic happen:

```python
# lots of lazy exception handling for the sake of brevity
def fire_effect(target):
    try:
        target.message("You are on fire.")
        target.health -= 5
    except Exception:
        pass

def heal_effect(target):
    try:
        target.message("You are being healed")
        target.health += 5
    except Exception:
        pass

def insult_effect(target):
    import random
    sense = random.choice(['smell', 'look', 'sound', 'fight'])
    thing = random.choice(['horse', 'onion', 'muddycrab', 'gamer'])
    try:
        target.message("You %s like a %s." sense, thing)
    except Exception:
        pass

fireball = Spell("fireball", fire_effect)
soothe = Spell("soothe", heal_effect)
curse = Spell("curse", insult_effect)
wizard1.add_spell(fireball)
wizard1.add_spell(curse)
wizard1.add_spell(soothe)
```

Assume we have Bill the Wizard, or wizard1 from before, and we load him up with all the right spells. Now let's return to Bill:

```
>>> spells
fireball
curse
soothe

>>> cast fireball
```
(nothing happens because no target is selected)

```
>>> cast fireball Bill

You are on fire!
>>> cast curse Bill

You sound like a onion.
```
Notice we never prevented the player from targeting themselves in cmd_cast. Now suppose someone else enters:

```
Matt the Dark Wizard enters.
Matt the Dark Wizard blasts you with lightning.
>>> cast heal Bill
You are being healed.

>>> cast fireball Matt
>>> cast fireball Matt
>>> cast fireball Matt
>>> cast fireball Matt
>>> cast fireball Matt

Matt the Dark Wizard died.
```

Here, we witness our spells in action. Though, it seems kind of unfair that we just spammed that command over and over again. Maybe there should be a cooldown. Hmmm... sounds like an idea for another day.

The key take away here should be that there is not a one class-per-file rule, you can have as many CharacterClasses and classes in a file are controlled by the fileparser.py importing system. That brings us to our next section.

### Making your CharacterClass a playable option
For a CharacterClass to be playable, you first create a json. Suppose our script containing the class definition was in "wizard.py". We should put wizard.py into ./script/. 

Next, we create a json:
```js
{
    "name" : "Wizard",
    "frequency" : 1,
    "path" : "scripts/wizard.py"
}
```
For good practice, should save this json as wizard.json (matching the name of the CharacterClass), but this is not required. The important thing is, the "name" field MUST match the name of the CharacterClass, as defined in the file. The "path" should be a path from the top MuddySwamp directory, to the script containing the CharacterClass.

The field "frequency" establishes the relative frequency of this class. Basically, the higher this number, then the more likely that the character will spawn as a Wizard, relative to other CharacterClasses.

### Coming soon
A few topics that I did not cover in this guide that I will cover later:
* referencing static objects
* using mudtools
* the built-in features of the Character class
* class data fields, like name, starting_location, and frequency. 
