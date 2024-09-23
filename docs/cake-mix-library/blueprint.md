---
title: Blueprint
parent: CakeMixLibrary
nav_order: 2
---
{% assign bp_path="cakemix" %}


{% assign in_source="CakeMixBlueprintLibrary" %}
{% include components/source_info_blueprint.html %}

## Introduction
**CakeMixLibrary** is a utility library that offers a variety of extra functionality to core CakeIO objects. Its primary purpose is to make more advanced IO operations easily achievable via a single function call. It also serves as an experimental ground that might influence CakeIO's future API evolution. For instance, if a particular function meant for **UCakeDir** becomes quite popular, then it might be promoted to a standard member function in the future.

## CakeMixLibrary
{% include components/default_toc.md %}

@add: Sort Path/File/Dir functions

{: .warning }
This library and its documentation deals with advanced usage of the CakeIO API and assumes the reader is well-acquainted with the fundamentals of CakeIO and its core objects. 

## Library Tour
We will now tour CakeMixLibrary's various namespaces with some basic examples of usage.

### UCakeDir
The following examples will showcase the utility functions offered for **UCakeDir** objects. 

#### Gathering Items into an Array
We can gather `UCakeFile` or `UCakeDir` objects into an array with the Gather family of functions. 

{% assign policy_id="OpDepth" %}
The simplest form of these functions is `Gather<Element>`, where `<Element>` is the target directory element we want to gather.  All of these functions take a **UCakeDir** object argument representing the directory we wish to gather items from and an {% include link_policy.md %} policy parameter which determines the depth the gather function should traverse when collecting items:

{% assign bp_file_id="gather-files" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="gather-subdirs" %}
{% include components/blueprint_image.md %}

`GatherFiles` returns an array of **UCakeFiles**,  and `GatherSubdirs` returns an array of **UCakeDirs**. 

There is also a filtered version for `GatherFiles`, which we can use via `GatherFilesWithFilter`:
{% assign bp_file_id="gather-files-with-filter" %}
{% include components/blueprint_image.md %}

{: .note }
The array returned from any Gather function can be empty.

There is a more specialized version of **Gather** which will gather up to a specific amount of items. This specialized version is the **GatherSome** family of functions, which take an extra parameter that indicates the maximum number of items that should be gathered:

{% assign bp_file_id="gather-some-files" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="gather-some-files-with-filter" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="gather-some-subdirs" %}
{% include components/blueprint_image.md %}

The examples above function just like the previous set of gather functions, except now they will terminate early if they have gathered the maximum number of items as specified by the `Max<Element>Count` argument.

{: .note }
The parameter that indicates the maximum number of items is inclusive, which means we will gather up to 4 items in the examples above.

#### Counting Items Contained in a Directory
Sometimes we might want to know just the amount of files or subdirectories contained in a directory, and for that we can use the **Count** family of functions. We submit a source **FCakeDir** object that represents the directory we wish to iterate and an {% include link_policy.md %} policy that determines how deep the iteration should traverse.

{% assign bp_file_id="count-files" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="count-files-with-filter" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="count-subdirs" %}
{% include components/blueprint_image.md %}

#### Copying / Moving Files Contained in a Directory
Sometimes we might want to copy or move only specific files from one directory to another without having to copy the entire directory and its contents. **CakeMixLibrary** has utility functions that let us copy or move only files from one directory to another. We can even copy/move files based on **UCakeDir**'s extension filter.

{: .note }
For the sake of brevity, we are only covering usage for the copy interfaces. Usage for moving files is exactly the same.

`CopyFiles` returns the same values we would expect from a directory IO operation: we get a boolean indicating whether or not the copy operation succeeded, and an `ECakeDirError` error code give greater context to the result. As a convenience, `CopyFiles` also returns the number of files that were copied in the operation.

{% assign bp_file_id="copy-files" %}
{% include components/blueprint_image.md %}

In the example above, the `CopyFiles` call will attempt to copy all shallow files from `/x/game/data/` to `/y/game/archive`. As we can see from the shrinking screen space, `CopyFiles` introduces some extra CakePolicies that give us greater customization of this copy process. Beyond the depth policy, there are three other policies to consider: 

{% assign policy_id="OverwriteItems" %}
{% include link_policy.md %} is a policy which you should be quite familiar with, so we'll focus on the other two policies. 

{% assign policy_id="ErrorHandling" %}
{% include link_policy.md %} is a policy that relies heavily on the context of its associated function. We can either abort on an error or continue on an error; the way that an error is defined will depend upon the function. In the case of `CopyFiles` or `MoveFiles`, the error occurs when a single file copy/move fails. There may be situations where this is acceptable and we should continue attempting the rest of the copy/move operations, but by default any failure to copy or move a file will result in the entire operation terminating early.

{% assign policy_id="MaintainRelativePaths" %}
{% include link_policy.md %} is a policy used to determine how we should treat files that are children of subdirectories. This policy only has effect when we are performing deep iterations. In essence, we get to decide if a nested file like `data/items.db` should be moved into the destination directory as `data/items.db` (creating the subdirectory data if necessary) or if we should strip the parent path and place `items.db` directly in the destination directory.

Let's look at an example where we make some changes to these new policies:
{% assign bp_file_id="copy-files-policy-inversion" %}
{% include components/blueprint_image.md %}

Here is an example of settings that deviate from the defaults. There are two key differences: 
1. CopyFiles will now attempt to copy all files regardless whether individual files fail to copy.
2. All files will be placed directly in the destination directory, removing any relative subdirectory trees that might have existed in the source directory.

{: .note }
There are also `WithFilter` variations available for CopyFiles/MoveFiles. Outside of filter policy parameters, their usage is identical. (Try not to wince when you see the full policy list.)

#### Deleting Items Contained in a Directory
**CakeMixLibrary** offers some utility methods to allow targeted deletion of files or subdirectories in a directory. Again, like we saw in `CopyFiles`, since these functions involve directory IO operations, they return the same boolean / error code pair we would expect. In addition, we are also given the number of files that were deleted by the operation.

We can delete all files at a specific depth via `DeleteFiles`:
{% assign bp_file_id="delete-files" %}
{% include components/blueprint_image.md %}

We can use the following policies to further customize this delete operation:
{% assign policy_id="FileDelete" %}
* {% include link_policy.md %}
{% assign policy_id="ErrorHandling" %}
* {% include link_policy.md %}

> For CakeMix's Delete family of functions, the error that will trigger the **ErrorHandling** policy is when a delete operation on a file or subdirectory fails.

We can also delete files with the source **UCakeDir**'s file extension filter via `DeleteFilesWithFilter`:
{% assign bp_file_id="delete-files-with-filter" %}
{% include components/blueprint_image.md %}

This shares all the same policy parameters and defaults as **DeleteFiles** and also includes the standard filter modification policies.

If we'd like to only delete subdirectories, we can do so via `DeleteSubdirs`:
{% assign bp_file_id="delete-subdirs" %}
{% include components/blueprint_image.md %}

{: .note }
`DeleteSubdirs` only takes an error handling policy since depth is irrelevant (deleting all subdirectories contained directly within the source directory is implicitly a deep operation).

Finally, if we want to delete all items contained within a directory but keep the source directory itself intact, we can use `DeleteAllItems`:
{% assign bp_file_id="delete-all-items" %}
{% include components/blueprint_image.md %}

Depth is irrelevant because we are deleting everything, but we still can determine whether or not read only files should be deleted and if the operation should abort if an item fails being deleted.

#### Creating Multiple Subdirectories in a Directory
If we want to create multiple subdirectories in a directory, we can use the convenience function function `CreateSubdirsUnders`. We submit an **FCakeDir** source directory and an **FString** that contains the directories to make; each directory should be separated by the `|` character, much like file extension syntax. 

For example, if we had a directory `/x/game`, the string `"data|models/extra|misc"` would attempt to create the following subdirectory structure:
```
📁 game
    📁 data 
    📁 models 
        📁 extra
    📁 misc 
```
Since `CreateSubdirsUnder` involves directory IO operations, it returns the same boolean / error code pair we would expect. We also are given the number of subdirectories successfully created.  In a perfect world, this should be the same number as you submitted.
{% assign bp_file_id="create-subdirs-under" %}
{% include components/blueprint_image.md %}

{% assign policy_id="ErrorHandling" %}
But perfect worlds don't exist, and so we can use the {% include link_policy.md %} policy to control whether or not we should abort the operation if any of the subdirectories cannnot be created. The default value for this parameter is **AbortOnError**.

#### Finding the First File with Extension in a Directory
We can get the first file selected by an **UCakeDir**'s file extension filter via `FindFirstFileWithFilter`:
{% assign bp_file_id="find-first-file-with-filter" %}
{% include components/blueprint_image.md %}

The function returns a boolean indicating whether or not a file was found and a **UCakeFile** that will hold the file path when it is found. If no file was found, the returned **UCakeFile** will be empty, so make sure you check the boolean before using it! The usual filter modification policies can be submitted via arguments if the caller wants to adjust the filter logic.

#### Finding Files by File Name in a Directory
There are a few utility functions that can help us retrieve files whose file names match a particular query. 

Before we look at the functions, it is important to understand the underlying logic behind comparing the file names against a query. This logic can be altered by the caller via arguments to the function. In short, a directory iteration for files will occur; each file will have its file name extracted and then that file name will be compared against the query submitted by the caller. The elements that a caller can control are the following:
{% assign subsec_link="file-name-types" %}
{% assign link_desc="this section"%}

{% assign policy_id="NameComparison" %}
1. Whether the query and file name must match exactly, or if the file name merely must contain the query somewhere within it. The is controlled via the {% include link_policy.md %} policy parameter.
2. If the comparison between the query and the file name should be case sensitive. This is controlled via the Unreal core type `ESearchCase`.
3. What type of file name should be extracted from each file. This is controlled via an `ECakeFileNameType` enum, which allows us to select between each of the types (Full, Root, Bare). If you are unfamiliar with file name types, please see {% include rlinks/cakefile_native.md %} for a detailed explanation.

The functions all have the following default settings: the query and file name must match exactly, the comparison is case sensitive, and the full file name should be extracted.

{% assign bp_file_id="find-first-file-named" %}
{% include components/blueprint_image.md %}

Again, we are returned a boolean that indicates whether a file was found and a **UCakeFile** that will hold the file path when one is found. The **UCakeFile** will be empty if no file was found.


We can achieve a much broader search by changing the name comparison to `ContainedInName` and making the query more generalized:

{% assign bp_file_id="find-first-file-named-modified" %}
{% include components/blueprint_image.md %}

However, if we are using such broad search terms, we likely are interested in more than one file. For these situations we can use `FindFilesNamed`, which will return an array of **UCakeFile** objects containing all files that matched against the query:

{% assign bp_file_id="find-files-named" %}
{% include components/blueprint_image.md %}

We are returned a boolean which indicates if any files were found. The returned array will be empty in the case where no files were found.

{: .note }
The `FindFilesNamed` family of functions have `ContainedInName` as their default policy value for `NameComparison` value in order to be more ergonomic for general use cases. 

{: .note }
Both `FindFirstFileNamed` and `FindFilesNamed` have filtered versions: `FindFirstFileNamedWithFilter` and `FindFilesNamedWithFilter`. The usage is identical with the exception of the added policy parameters to control the filter logic.

### File
##### Changing a File's Extension Only
Sometimes we might want to change just the file extension of a particular file without changing the rest of the file name. To accomplish this, **CakeMixLibrary** offers two functions: `RenameFileExtOnly` and `RenameFileExtOnlyMulti`.

There is a key difference between the two functions: `RenameFileExtOnly` changes the entire file extension to the submitted extension, whereas `RenameFileExtOnlySingle` will change only the trailing extension component. 

Let's look at an example: Suppose we have a file named `items.db.zip` and we want to change the file extension to `.sqlite`. This file's extension is a {% glossary ext_multi, display: multi extension %}, so if we use `RenameFileExtOnly` and submit the argument `.sqlite`, the file will be renamed to `items.sqlite`. If instead we use `RenameFileExtOnlySingle` and submit `.sqlite`, we will get the following file name: `items.db.sqlite`.

In the case where our source file is a {% glossary ext_single, display: single extension %}, such as `items.db`, calling either function with the new file extension `.sqlite` will result in the same end file name: `items.sqlite`.

{: .hint }
Don't worry much about `RenameFileExtOnlySingle`, as it exists for very specialized cases which should be quite rare in day to day work. 

Let's take a look at an example using `RenameFileExtOnly`:
{% assign bp_file_id="rename-file-ext-only" %}
{% include components/blueprint_image.md %}

Since this involves a file IO operation, we are returned a boolean indicating if the operation succeeded, and an `ECakeFileError` error code that can give us more context.

{: .note }
Assuming `RenameFileExtOnly` / `RenameFileExtOnlySingle` are successful, the associated **FCakeFile**'s path information is automatically updated to reflect the changes.

### Path
Path currently has no functions defined. This may change in the future.

### Results
CakeMixLibrary offers utility functions to convert "result" types into human readable strings. Error codes and iteration outcomes are classified as result types. For details on how to get the string version from result types, please see the following subsections of **Error Handling**:
{% assign link_desc="IO Operation Error Codes" %}
{% assign subsec_link="human-readable-strings" %}
{% include rlinks/error_handling_blueprint.md %}

{% assign link_desc="Iteration Outcome Codes" %}
{% assign subsec_link="human-readable-strings-1" %}
{% include rlinks/error_handling_blueprint.md %}
