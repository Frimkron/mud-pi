# Contributing to MuddySwamp

Thank you for helping out with the Open Source Club's MuddySwamp project!

Following these guidelines helps us keep good project workflow. We appreciate you working with us on it.

Please read our [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) to understand our community expectations. Check out our [slack](https://ufosc.slack.com) for any additional questions or just to hangout!

## How do I help?

Please check the **[Projects]()** and **[Issues]()** pages for current tasks. If you see something that you would like to help with, ask about helping in a comment and we'll assign it too you. If you're just starting out, checkout our **[beginner friendly]()** issues for ways to help. 

Checkout the [DESIGN.md](docs/DESIGN.md) file for a high level explanation of the project.

### Report Bug 

Check to see if someone already reported this [bug]() already exists. If so then leave a comment on that issue. If not, please provide a detailed description of the bug. Include what was happening before the error, all settings, and test results. This helps us more quickly identify and solve any problems. Create an **[Issue]()** with the description and add a bug label. We will do our best to respond quickly to it. 

### Testing your own Server

To test server code on your own machine, run

	python MuddySwamp.py

Then with a telnet client, you will connect to the following IP like so:

	telnet 127.0.0.1 1234

For contributors working on server code, make sure you test changes like so before submitting changes.
### Request a Feature

Check to see if the feature is already listed in our [TODO.md](docs/TODO.md). If it's not, describe the feature and why it would be beneficial. Create an **[Issue]()** with this description and add a feature enhancement label. We will do our best to respond quickly to it. 


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

## Style Guide 

Use our **[.editorconfig]()** to help automatically format your code. A short list of what we require.

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