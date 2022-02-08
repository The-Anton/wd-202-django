### [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)

### [Iterators and generators in Python](https://docs.python.org/3/glossary.html#term-iterator)

### [Problem Solving with algorithms and data structures with Python](https://runestone.academy/runestone/books/published/pythonds/index.html)

### [Problem-Solving with Python](https://problemsolvingwithpython.com/)

### [Python CheetSheet](https://www.pythoncheatsheet.org/)

Note that class names are always in UpperCamelCase

Python also supports multiple inheritance. This is used when we want to inherit from multiple classes.

```
class A:
    def print_a(self):
        print("A")

class B:
    def print_b(self):
        print("B")

class AB(A,B): # This class inherits from both A and B
    def print_ab(self):
        print("AB")

ab = AB()
ab.print_a() # A
ab.print_b() # B
ab.print_ab() # AB
```
Each Python object has a method resolution order ( MRO ) which is a list of classes that are used to resolve the method. The MRO is used to determine which class to call when a method is called. Let's say that each of the inherited classes has the same function, to identify which method is called we use the MRO.


```
# Continue from the above example

print(AB.mro()) # [<class '__main__.AB'>, <class '__main__.A'>, <class '__main__.B'>, <class 'object'>]

# The MRO is [AB, A, B, object] so the AB class is checked first then the A class and then the B class.
```



Mixins

When developing applications you might come across common functionality that is shared between a number of classes, in Python each feature can be built into different classes and then combined together to create a new class with the functionality required.

In the above examples we created classes and defined functionality in them, another approach is to create classes with functionality and combine them together to create a new class.

```
class RunnableMixin:
    def run(self):
        print("Can Run")

class WalkableMixin:
    def walk(self):
        print("Can Walk")

class TalkingMixin:
    def talk(self):
        print("Can Talk")

class Animal(RunnableMixin, WalkableMixin):
    pass

class Human(RunnableMixin, WalkableMixin, TalkingMixin):
    pass
```

Each of the feature classes is called a Mixin. Mixins are extremely useful in web development to add new features to existing classes.


#### Python does not do any type of enforcement on private or protected members, but it is a convention to follow when designing classes.

For the curious folk who want to know how python does this internally, check out this [link](https://docs.python.org/3/tutorial/classes.html#private-variables)


