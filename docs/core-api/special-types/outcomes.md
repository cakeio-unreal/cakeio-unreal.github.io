## Introduction
{{ src_loc_group('Outcomes', 'CakeOutcomes')}}

Outcomes are special enums that represent the final outcome of a desired IO operation. They are used to give enhanced context about the result of an IO operation, especially when the operation fails.

## IO Outcomes
### Overview
There are two distinct outcome types used to represent IO operations: one for IO operations involving a file, and one for IO operations involving a directory. While there are many overlapping values, keeping the outcomes distinct types helps promote better type safety and allows us better error reporting clarity by keeping each outcome set as minimal and relevant as possible toward its associated operations.

### Ok and No Op
Both file and directory outcome types have two values that do not indicate an actual error: `Ok` and `No Op`. It is important to understand the difference between these two outcomes.

> **Ok**: The IO operation was executed and encountered no errors.

> **No Op**: The IO operation was skipped because it would have resulted in no effect.

The primary reason `NoOp` exists is so that callers can know whether or not an IO operation _actually occurred_. In many contexts, we don't need to distinguish between these two values because the desired state on the filesystem is achieved either way. For example, if we want to ensure that a file is deleted, then whether or not the call to DeleteFile actually resulted in an IO operation is immaterial -- the file does not exist on the filesystem regardless. However, when we are trying to append text to a file, a `NoOp` can be a telling return value, which would indicate that we were trying to append an empty string to the file. This might be valuable information if we were accepting inputs from an outside source.  

### ECakeOutcomeFileIO
This is the outcome value that is dedicated to represent outcomes associated with IO operations involving an individual file.

{{ read_csv(open_csv_by_typename('ECakeOutcomeFileIO')) }}

### ECakeOutcomeDirIO
This is the outcome value that is dedicated to represent outcomes associated with IO operations involving an individual directory.

{{ read_csv(open_csv_by_typename('ECakeOutcomeDirIO')) }}

### File / Directory Name Sanitization
Both file and directory outcomes have a value that represents an invalid file or directory name. As of now, this is only returned in functions that involve changing the file or directory name, and it only is returned when the proposed name is empty. __There currently is no validation that occurs regarding illegal characters in paths.__

### FailedDeletingPreexisting
While most outcomes are self-explanatory, this particular outcome value could benefit from a little extra explanation. This outcome can occur when the user runs an IO operation that allows preexisting items to be overwritten by the IO operation. In the event that an item already exists at the destination path, the IO operation will attempt to first delete that item in order to ensure the main IO operation can proceed. If the item at the destination path cannot be deleted, this value is returned.

## Directory Traversal Outcomes
!!! note
    This section deals with directory traversal. If you are unfamiliar with this concept, please see [this section](../directories.md#directory-traversal).

The following outcome enums are used to represent the result of directory traversal. 

### Did Not Launch
All traversal outcomes have a value to indicate that a traversal operation failed to start. It is important to understand the contexts that can cause an traversal to fail to start:

1. **The source directory does not exist.**
When a traversal is called on a CakeDir object, that traversal operation will first ensure that the directory it represents actually exists on the filesystem. If it does not, the iteration will not proceed.

2. **A [filtered traversal](../directories.md#filtered-traversals) is called on a directory object when its extension filter is empty.** 
This would visit files in a way that the caller does not want, and so the iteration will not proceed.

3. **A policy argument with an out of range value was submitted.**
All CakeIO policies are enums, so out of range issues should be quite rare. The only way these are able to occur is if one is casting integer values to the policy type; if you are doing this, _be extremely careful_! 

!!! tip
    If CakeIO logging is enabled, it will describe the error that prevented the iteration from launching.

### ECakeOutcomeTraversal
This outcome value is used by both unguarded and guarded traversal styles. 

{{ read_csv(open_csv_by_typename('ECakeOutcomeTraversal')) }}

### ECakeOutcomeSearch
This outcome value is used only by search traversals. 

{{ read_csv(open_csv_by_typename('ECakeOutcomeSearch')) }}

## Advanced Outcomes
These outcomes are used by high level, advanced APIs.

### ECakeOutcomeDirWork
This outcome value that is used by higher level functions that perform some work on elements within a target source directory. Used extensively in [CakeMixLibrary](../../advanced/cake-mix-library.md) functions.

{{ read_csv(open_csv_by_typename('ECakeOutcomeDirWork')) }}

### ECakeOutcomeBatchOp
This outcome value that is used by batch operations, which are special async operations that involve performing custom actions on collections of CakeFiles or CakeDirs in [CakeAsyncIO](../../advanced/async-io.md) functions.

{{ read_csv(open_csv_by_typename('ECakeOutcomeBatchOp')) }}
