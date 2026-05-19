# Lab 4 Reflection

## What happens when you attempt to modify a read-only property?

When you try to assign a value to my_book.description, Python raises an
AttributeError with the message "can't set attribute." This happens because
the description property only has a getter defined, no setter
registered with it. Without a setter, Python has no function to call when an
assignment is attempted, so it blocks it entirely and throws the error.