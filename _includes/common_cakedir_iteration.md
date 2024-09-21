## Directory Iteration
Directory iteration is a vital part of working with file systems, and CakeIO offers a comprehensive set of iteration functions to support a wide variety of situations. Directory iteration is divided into three iteration styles, each of which utilize a unique callback signature. 

### Controlling Iterations
Before we examine iteration styles, it is important to understand that all styles allow the caller to control the following iteration characteristics: **iteration depth** and **directory element type**.

#### Directory Element Type
Callers are allowed to iterate across the following directory element type categories:
> **Items**: An **items** iteration will visit both files and subdirectories contained within the source directory.

> **Files**: A **files** iteration will only visit files contained within the source directory.

**Files** iterations are special because they offer an unfiltered version and a filtered version. The unfiltered version will visit all files at the specified depth, whereas the filtered version will use the directory object's file extension filter to select specific files to visit.

> **Subdirectories**: A **subdirectories** iteration will only visit subdirectories contained within the source directory.

#### Iteration Depth
Iteration depth specifies if an iteration is allowed to visit items located within subdirectories of the source directory:
> **Shallow** Iteration: In this depth, the iteration is only allowed to visit items located directly in the source directory. No children of subdirectories will be visited.

> **Deep** Iteration: In this depth, all children of subdirectories will be visited. This is the iteration depth you should use if you want to visit ALL target elements contained within a source directory.

```
Example Directory Tree
📁 Game
    📄 read_me.md [Shallow]
    📁 Data [Shallow]
        📄 map-1.lv [Deep]
        📄 map-2.lv [Deep]
        📁 Tables [Deep]
            📄 items.db [Deep]
```

In the example above, any item tagged with `Shallow` would be visited with a shallow iteration, whereas items marked as either `Shallow` OR `Deep` would be visited with a deep iteration.

### Iteration Styles
There are three main styles of directory iteration supported by CakeIO:
> **Sequential Iteration**: Visits all target elements within the source directory at a specified depth. This is the simplest form of iteration and offers no way to terminate the iteration early. Use this iteration style when you want to visit all target elements of a directory and you don't have any conditions that should interrupt the iteration. An example use case would be counting the number of files in a directory.

> **Guarded Iteration**: Visits all target elements within the source directory at a specified depth, but the caller can terminate the iteration early if an error is encountered. The caller is left to decide what constitutes an error. Use this iteration style whenever you want to ideally visit all target elements but might encounter an situation that should terminate the iteration early. An example use case would be an operation that copies files from one directory to another but should halt if an individual file copy fails.

> **Search Iteration**: Visits target elements within the source directory until a goal is met; the user is in full control of defining what the goal is. Searches can end in three different states: **Success** (the goal was met), **Failed** (all elements were visited but the goal was not met), or **Aborted** (an error was encountered before the goal was met). This is the most advanced iteration style, but also the most versatile. Use this style whenever you want to scan a directory's elements until a certain condition is met. An example use case would be attempting to gather exactly 3 files from a source directory.
