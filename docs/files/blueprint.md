---
title: Blueprint
parent: Files
nav_order: 2
---

{% assign in_source="CakeFile_BP" %}
{% include components/source_info_blueprint.html %}

{% assign bp_path="file" %}

## UCakeFile
{% include components/default_toc.md %}

## Introduction
The Blueprint file object in **CakeIO** is **UCakeFile**. **UCakeFile** is designed to provide an ergonomic and comprehensive interface for common file operations.

{% include components/src_advert_blueprint.md %}

## Basic Usage
The following covers some of the core interfaces required to utilize and manipulate UCakeFile objects.

### UCakeFile Creation
We can create an **UCakeFile** via `BuildCakeFile` or `BuildCakeFileViaPath`.

{% assign bp_file_id="build-cake-file" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="build-cake-file-via-path" %}
{% include components/blueprint_image.md %}

If we want to create a **UCakeFile** with no initial path data, we can use `BuildCakeFileEmpty`:

{% assign bp_file_id="build-cake-file-empty" %}
{% include components/blueprint_image.md %}

### File Paths
To get the file path as a string, we can use the convenience function `GetPathString`:
{% assign bp_file_id="get-path-string" %}
{% include components/blueprint_image.md %}

{% assign link_desc="UCakePath" %}
To get a {% include rlinks/cakepath_blueprint.md %} copy that contains the file path, we can use `ClonePath`.

{% assign bp_file_id="clone-path" %}
{% include components/blueprint_image.md %}

{: .note }
This is just a copy of the file path, no changes made the to returned **UCakePath** will be reflected in the source **UCakeFile**.

To change the file path represented by a **UCakeFile** object, we can use `SetPath` or `SetPathViaPath`:
{% assign bp_file_id="set-path" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="set-path-via-path" %}
{% include components/blueprint_image.md %}

### File Name
If we want to read the full file name by itself as a string, we can use `GetFileName`:

{% assign bp_file_id="get-file-name" %}
{% include components/blueprint_image.md %}

{: .note }
There are other functions for generating different versions of a filename (e.g., one without its file extension data). For more information, please see the [File Name Types](#file-name-types) section.

### File Extension
To get the file extension as an FString, we can use the convenience function GetFileExtString:

{% assign bp_file_id="get-file-ext-string" %}
{% include components/blueprint_image.md %}

{% assign link_desc="UCakeFileExt" %}
If we want a {% include rlinks/cakefileext_blueprint.md %} copy of the file extension, we can get one via `CloneFileExt`:

{% assign bp_file_id="clone-file-ext" %}
{% include components/blueprint_image.md %}

### File Path Empty/Reset
We can check if an **UCakeFile**'s file path is empty via `PathIsEmpty`, and we can clear an **UCakeFile**'s path via `Reset`:

{% assign bp_file_id="path-is-empty" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="reset" %}
{% include components/blueprint_image.md %}

## IO Operations

{% assign link_desc="Error Handling" %}
{: .note }
The following examination of IO operations does not include any examples of error handling. For information on error handling strategies, see {% include rlinks/errorhandling_blueprint.md %}.

### File Existence
We can check if a file exists on the filesystem via `Exists`:

{% assign bp_file_id="exists" %}
{% include components/blueprint_image.md %}

### Read/Write Operations
**UCakeFile** provides interfaces for handling files as text files or binary (data) files. Text files will use strings for read/write operations, and binary files will use arrays of bytes for read/write operations. 

#### Creating Files
The file creation interface is meant to be used on files that do not already exist. To create a text or binary file, we use `CreateTextFile` or `CreateBinaryFile`:

{% assign bp_file_id="create-text-file" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="create-binary-file" %}
{% include components/blueprint_image.md %}

We can use the following policies to further customize the create functions' behavior: 
{% assign policy_id="OverwriteItems" %}
* {% include link_policy.md %}
{% assign policy_id="MissingParents" %}
* {% include link_policy.md %}

If a file already exists, we generally should use the `WriteTextFile` or `WriteBinaryFile` interfaces. However, there are convenience functions that will either create the file if it does not exist or overwrite the file if it does exist via `CreateOrWriteTextFile` and `CreateOrWriteBinaryFile`:

{% assign bp_file_id="create-or-write-text-file" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="create-or-write-binary-file" %}
{% include components/blueprint_image.md %}

#### Reading Files
To read the data from a text or binary file, we use `ReadFileAsString` or `ReadFileAsBytes`:

{% assign bp_file_id="read-file-as-string" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="read-file-as-bytes" %}
{% include components/blueprint_image.md %}

#### Writing Files
We use the writing interfaces when a file exists and we want to overwrite its contents with new contents. We can overwrite a file's contents via `WriteTextToFile` and `WriteBytesToFile`:

{% assign bp_file_id="write-text-to-file" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="write-bytes-to-file" %}
{% include components/blueprint_image.md %}


{: .warning }
The write functions will fail if the file does not exist, so be sure to check before calling them.

If we want to append data to the file instead of overwriting its old contents, we use `AppendTextToFile` or `AppendBytesToFile` :

{% assign bp_file_id="append-text-to-file" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="append-bytes-to-file" %}
{% include components/blueprint_image.md %}


### Copying Files
We can copy a file to another directory via `CopyFile`. The **UCakePath** submitted represents the directory to which the file is copied.

{% assign bp_file_id="copy-file" %}
{% include components/blueprint_image.md %}

If we have a **UCakeDir** that represents the destination directory, we can use `CopyFileViaDir` instead:

{% assign bp_file_id="copy-file-via-dir" %}
{% include components/blueprint_image.md %}

{: .note }
In the examples above, the copied file's final path is `some/other/dir/spells.db`

Sometimes we might want to copy a file with a new name, and for that we can use `CopyFileAliased` or `CopyFileAliasedViaDir`. In addition to a destination path, we also need to provide a new name that the copied file should have:

{% assign bp_file_id="copy-file-aliased" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="copy-file-aliased-via-dir" %}
{% include components/blueprint_image.md %}

{: .note }
In the examples above, the copied file's final path is `some/other/dir/spells_archive.db`

We can use the following policies to further customize the behavior of all the copy functions: 
{% assign policy_id="OverwriteItems" %}
* {% include link_policy.md %}
{% assign policy_id="MissingParents" %}
* {% include link_policy.md %}

### Moving Files

{: .note }
It is important to understand that a move is actually a compound IO operation -- a source file is copied to the desired location, and then that source file is deleted. This is important to keep in mind when examining the error codes from failed moves -- in terms of IO operations, a move could fail during the copy operation or the delete operation, but there is no dedicated error code for a "move" failure.


We can move a file to another directory via `MoveFile`. The **UCakePath** submitted represents the directory to which the file is to be moved.

{% assign bp_file_id="move-file" %}
{% include components/blueprint_image.md %}

If we have a **UCakeDir** that represents the destination directory, we can use `MoveFileViaDir` instead:

{% assign bp_file_id="move-file-via-dir" %}
{% include components/blueprint_image.md %}

{: .note }
In the examples above, the file's new path is `some/other/dir/spells.db`

Sometimes we might want to copy a file with a new name, and for that we can use `MoveFileAliased` or `MoveFileAliasedViaDir`. In addition to a destination path, we also need to provide a new name that the file should have after the move:

{% assign bp_file_id="move-file-aliased" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="move-file-aliased-via-dir" %}
{% include components/blueprint_image.md %}

{: .note }
In the examples above, the moved file's new path is `some/other/dir/spells_archive.db`

We can use the following policies to further customize the behavior of all the move functions: 
{% assign policy_id="OverwriteItems" %}
* {% include link_policy.md %}
{% assign policy_id="MissingParents" %}
* {% include link_policy.md %}

We can also rename a file with `RenameFile`.
{% assign bp_file_id="rename-file" %}
{% include components/blueprint_image.md %}

We can use the following policy to further customize the behavior of `RenameFile`: 
{% assign policy_id="OverwriteItems" %}
* {% include link_policy.md %}

### Deleting Files
To delete a file, use `DeleteFile`:
{% assign bp_file_id="delete-file" %}
{% include components/blueprint_image.md %}

We can use the following policy to further customize the behavior of `DeleteFile`: 
{% assign policy_id="FileDelete" %}
* {% include link_policy.md %}

{: .note }
In the event that the file does not exist, `ErrorCode` will be set to NOP.

### Retrieving File OS Information
**UCakeFile** provides a set of functions that can retrieve information about its file from the operating system, such as its file size in bytes. 

{: .warning }
All functions in this section can fail to retrieve valid information. Always check the boolean that indicates if the retrieval was successful before using the returned data.

`GetStatData` gives us a struct that contains all of the file information we can retrieve from the operating system.
{% assign bp_file_id="get-stat-data" %}
{% include components/blueprint_image.md %}

There are two ways to check if `GetStatData` was successful, the `IsValid` boolean on the CakeFileStatData struct itself, or the `GotValidStatData` boolean returned by `GetStatData`.

We can also retrieve some of the stats individually if we don't want the entire collection.

We can attempt to retrieve the size of a file via `GetFileSizeInBytes`:
{% assign bp_file_id="get-file-size-in-bytes" %}
{% include components/blueprint_image.md %}

We can attempt to retrieve the access timestamp via `GetAccessTimestamp`:
{% assign bp_file_id="get-access-timestamp" %}
{% include components/blueprint_image.md %}

We can attempt to retrieve the modified timestamp via `GetModifiedTimestamp`:
{% assign bp_file_id="get-modified-timestamp" %}
{% include components/blueprint_image.md %}

We can also try to set the modified timestamp to a custom value via `SetModifiedTimestamp`. This function returns true if the modified time was successfully changed, false otherwise.
{% assign bp_file_id="set-modified-timestamp" %}
{% include components/blueprint_image.md %}

## Advanced Usage
### File Name Types
**CakeIO** classifies file names into three different categories. Using the file name `info.cdr.txt` as an example:
1. **Full Name**: The file name with all of its extensions: `info.cdr.txt`
2. **Root Name**: The file name with its trailing extension removed: `info.cdr`
3. **Bare Name**: The file name without any extensions: `info`

{: .note }
When FileName is used by itself, **Full Name** is implied. Thus, `CloneFileName` will clone the full file name, whereas `CloneFileNameBare` will clone the bare file name.

We can read the full file name of an **UCakeFile** via `GetFileName`:
{% assign bp_file_id="get-file-name" %}
{% include components/blueprint_image.md %}

If we need a copy of the full name, we can use `CloneFileName`:
{% assign bp_file_id="clone-file-name" %}
{% include components/blueprint_image.md %}

We can get a copy of the root file name via `CloneFileNameRoot`:
{% assign bp_file_id="clone-file-name-root" %}
{% include components/blueprint_image.md %}

We can get a copy of the bare file name via `CloneFileNameBare`:
{% assign bp_file_id="clone-file-name-bare" %}
{% include components/blueprint_image.md %}
