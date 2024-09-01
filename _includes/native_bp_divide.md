### The Native and Blueprint Divide
There are two different file extension types -- one specifically tailored to Native (C++) code and another for Blueprint. Their interfaces share a lot of common structure, but they will diverge at times in order to accomodate the constraints of their target programming language (e.g., Blueprint doesn't allow overloads). 

The documentation reflects this two type distinction -- there are guides for both Native and Blueprint objects. Please choose the category that applies to your current use case, as the guidance and usage will vary.

{: .note }
Internally the Blueprint type wraps the native type. There is always a way to gain access to the native type when you are in native code; you can find examples of this access throughout all of the Blueprint type C++ implementations.