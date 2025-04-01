# CakeIO
CakeIO is a plugin for Unreal Engine that provides an ergonomic and comprehensive API for IO related tasks. CakeIO is built directly on top of Unreal Engine's low level IO interfaces, leveraging its maturity and stability while providing an enriched and modernized set of objects and APIs to provide a first-class developer experience for common IO related tasks. 

## Tour

### Enhanced Error Handling
CakeIO introduces custom error types to improve error reporting from IO operations, empowering callers with more context in the event an operation fails. These error types have been designed to easily adapt to whatever level of error handling a user needs, allowing CakeIO to remain ergonomic in a variety of use cases -- from quick editor scripts to professional software.

When minimal error handling is required, operations always provide a way where their outcome can be viewed as a Boolean indicating success or failure:

However, when more robust error handling is necessary, CakeIO's errors will give you the context required to properly respond to any untoward outcomes.

### Dedicated IO Types
CakeIO provides dedicated types to represent the common entities used in IO operations, from paths to directories and even file extensions. Let's take a look at a few of the core types to get a taste of what CakeIO offers.

(When writing these, use the following form: showcase what would be expected from an IO library to give a veteran programmer assurance of services AND an easy way to evaluate the API and its ergonomics. Then add one extra feature per type that showcases how much easier CakeIO makes it over base Unreal. Do not explicitly frame the extra feature this way.)

#### Paths
Paths are now first-class types, allowing us to effectively store, compare, and manipulate filesystem paths in a single interface. Path objects enforce a standard representation for path separators -- we can build paths from Windows or Unix-like path strings and the path object will handle the rest for us.

Path comparison allows to easily check if two paths reference the same location on the filesystem. 

Path objects offer us a variety of utilities for path manipulation and generation -- we can easily combine paths together, replace path parents, leafs, and more!

For more information on path objects, please see the [official API documentation](core-api/paths.md).

#### Files
The file objects offer a comprehensive and ergonomic way to interact with files on the filesystem. 

To create a file object, we need to give it a path object that represents the file's path.

The file object comes replete with various IO operations. We can get information about the file from the operating system, such as whether the file exists or how large the file is in bytes:

As we would expect, we can also read and write to files. The file objects supply interfaces for two main data types: text and binary. We can create, read, write, and append data to the file easily.
                             
We can also get information about the file path itself, such as the file name or its extension. 

CakeIO provides in-depth categories for file names and file extensions. It distinguishes between single extensions (e.g., ".txt") and multi extensions (e.g., ".txt.md"). We can generate file name variants based on these categories:

For more information on file objects, please see the [official API documentation](core-api/files.md).

#### Directories
Directory objects offers a comprehensive interface to work with directories. 

We have access to all standard IO operations like creating, deleting, and copying directories:

Directory traversal is given special attention in CakeIO. CakeIO offers three distinct styles of directory traversals, each giving the caller a different level of control over the traversal operation. 

Traversals let the caller select which type of children we should visit -- items (both files and subdirectories), files, or subdirectories. 

Furthermore, directory objects have a file extension filter which can be used to selectively visit files based on their file extensions. For more information on filtered file traversals, GO HERE.

There is much more to directory objects than what is listed here. For more information on directory objects, please see the [official API documentation](core-api/directories.md).