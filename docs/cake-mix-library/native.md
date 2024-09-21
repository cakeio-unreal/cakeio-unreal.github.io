---
title: Native
parent: CakeMixLibrary
nav_order: 1
---

{% assign in_source="CakeMixLibrary" %}
{% include components/source_info.html %}

## CakeMixLibrary
{% include components/default_toc.md %}

## Required Includes
All source code examples going forward will assume that your code has the following include statements:
```cpp
#include "CakeIO/CakeMixLibrary.h"
#include "CakeIO/CakePath.h"
#include "CakeIO/CakeDir.h"
#include "CakeIO/CakeFile.h"
```

{: .warning }
This library and its documentation deals with advanced usage of the CakeIO API and assumes the reader is well-acquainted with the fundamentals of CakeIO and its core objects. 

## Introduction
**CakeMixLibrary** is a utility library that offers a variety of extra functionality to core CakeIO objects. Its primary purpose is to make more advanced IO operations easily achievable via a single function call. It also serves as an experimental ground that might influence CakeIO's future API evolution. For instance, if a particular function meant for **FCakeDir** becomes quite popular, then it might be promoted to a standard member function in the future.

{: .note }
CakeMixLibrary also provides valuable insight into advanced usage for CakeIO objects. Studying the implementation can be quite valuable for your usage of CakeIO objects!


## Library Map
**CakeMixLibrary** is organized as a namespace with freestanding functions instead of a class with static functions. Within the **CakeMixLibrary** namespace are other namespaces, each with an association to various objects in the CakeIO API. The following lists the namespaces and their associated objects:

1. **Dir**: Contains all functions that utilize the **FCakeDir** object.
2. **File**: Contains all functions that utilize the **FCakeFile** object.
3. **Path**: Contains all functions that utilize the **FCakePath** object. This currently is empty, but the namespace has been reserved for future expansion.
4. **Results**: This contains utility functions that operate on various CakeIO result / error code / iteration outcome types. 

{: .hint }
Many of the following functions have a dizzying policy parameter list if you need to deviate from the defaults; if the defaults aren't what you need and you find yourself specifying the same policies across many calls, write a convenience function that does the verbose work for you automatically!

## Library Tour
We will now tour CakeMixLibrary's various namespaces with some basic examples of usage.

### Dir
The following examples will showcase the utility functions offered for **FCakeDir** objects. The following examples will assume we have declared the following **FCakeDir** object:
```cpp
FCakeDir IntDir{ FPaths::ProjectIntermediateDir(), TEXT("json|bin") };
```
#### Gathering Items into an Array
We can gather `FCakeFile` or `FCakeDir` objects into a `TArray` with the Gather family of functions. 

{% assign policy_id="OpDepth" %}
The simplest form of these functions is `Gather<Type>`, which all take an **FCakeDir** argument representing the directory we wish to gather items from and an {% include link_policy.md %} policy parameter which determines the depth the gather function should traverse when collecting items. 
```cpp
TArray<FCakeFile> Files{};
TArray<FCakeDir> Subdirs{};

ECakePolicyOpDepth CurrentDepth = ECakePolicyOpDepth::Shallow;
Files = CakeMixLibrary::Dir::GatherFiles(IntDir, CurrentDepth);
Files = CakeMixLibrary::Dir::GatherFilesWithFilter(IntDir, CurrentDepth);
Subdirs = CakeMixLibrary::Dir::GatherSubdirs(IntDir, CurrentDepth);
```

As we can see from the examples above, `GatherFiles` returns a `TArray<FCakeFile>` and `GatherSubdirs` returns a `TArray<FCakeDir>`. Futhermore, we can also use IntDir's extension filter on a `GatherFiles` operation via `GatherFilesWithFilter`.

There is a more specialized version of **Gather** which will gather UP TO a specific amount of items. This specialized version is the **GatherSome** family of functions, which take an extra parameter that indicates the maximum number of items that should be gathered:
```cpp
constexpr int32 MaxItems{ 4 };
Files = CakeMixLibrary::Dir::GatherSomeFiles(IntDir, MaxItems, CurrentDepth);
Files = CakeMixLibrary::Dir::GatherSomeFilesWithFilter(IntDir, MaxItems, CurrentDepth);
Subdirs = CakeMixLibrary::Dir::GatherSomeSubdirs(IntDir, MaxItems, CurrentDepth);
```

The examples above function just like the previous set of gather functions, except now they will terminate early if they have gathered the maximum number of items as specified by `MaxItem`.

{: .note }
The parameter that indicates the maximum number of items is inclusive, which means we will gather up to 4 items in the examples above.

#### Counting Items Contained in a Directory
Sometimes we might want to know just the amount of files or subdirectories contained in a directory, and for that we can use the **Count** family of functions. We submit a source **FCakeDir** object that represents the directory we wish to iterate and an {% include link_policy.md %} policy that determines how deep the iteration should traverse.

```cpp
int64 CountResult{ 0 };
CountResult = CakeMixLibrary::Dir::CountFiles(IntDir, CurrentDepth);
CountResult = CakeMixLibrary::Dir::CountFilesWithFilter(IntDir, CurrentDepth);
CountResult = CakeMixLibrary::Dir::CountSubdirs(IntDir, CurrentDepth);
```
#### Copying / Moving Files Contained in a Directory
Sometimes we might want to copy or move only specific files from one directory to another without having to copy the entire directory and its contents. **CakeMixLibrary** offers us copy and move functions for files that can be used with or without the source **FCakeDir**'s file extension filter. 

{: .note }
For the sake of brevity, we are only covering usage for `CopyFiles`. `MoveFiles` usage is identical.

{% assign subsec_link="fcakedirbatchresult" %}
{% assign link_desc="FCakeDirBatchResult"%}
These functions return an {% include rlinks/error_handling_native.md %}, if you are unfamiliar with them please read the documentation.

```cpp
FCakeDir DestDir{ TEXT("x/game/data/archives") };
FCakeDirBatchResult CopyResult{};

auto OpDepth = ECakePolicyOpDepth::Shallow;
CopyResult   = CakeMixLibrary::Dir::CopyFiles(DestDir, IntDir, OpDepth);

if (CopyResult.DidAnyWork())
{
    UE_LOG(LogTemp, Warning, TEXT("Copied [%d] file(s)."), CopyResult.ItemsProcessed);
}
else
{
    UE_LOG(LogTemp, Warning, TEXT("No files to copy!"))
}
```
This will copy all shallow files from `IntDir` to `DestDir`. However, `CopyFiles` introduces some extra CakePolicies that afford us greater customization of this copy process. There are three "hidden" policies that have been given default values. The following code is equivalent to the previous examples, as these policies share the default values.
```cpp
auto OverwritePolicy       = ECakePolicyOverwriteItems::OverwriteExistingItems;
auto ErrorPolicy           = ECakePolicyErrorHandling::AbortOnError;
auto RelativeParentsPolicy = ECakePolicyFileRelativeParents::MaintainRelativeParents;

CopyResult = CakeMixLibrary::Dir::CopyFiles(DestDir, IntDir, OpDepth, 
    OverwritePolicy, ErrorPolicy, RelativeParentsPolicy);

```
{% assign policy_id="OverwriteItems" %}
{% include link_policy.md %} is a policy which you should be quite familiar with, so we'll focus on the other two policies. 

{% assign policy_id="ErrorHandling" %}
{% include link_policy.md %} is a policy that relies heavily on the context of its associated function. We can either abort on an error or continue on an error; the way that an error is defined will depend upon the function. In the case of CopyFiles or MoveFiles, the error we are talking about is when a single file copy/move fails. There may be situations where this is acceptable and we should continue attempting the rest of the copy/move operations, but by default any failure to copy or move a file will result in the entire operation terminating early.

{% assign policy_id="MaintainRelativePaths" %}
{% include link_policy.md %} is a policy used to determine how we should treat files that are children of subdirectories. This policy only has effect when we are performing deep iterations. In essence, we get to decide if a nested file like `data/items.db` should be moved into the destination directory as `data/items.db` (creating the subdirectory data if necessary) or if we should strip the parent path and place `items.db` directly in the destination directory.

```cpp
OpDepth               = ECakePolicyOpDepth::Deep;
ErrorPolicy           = ECakePolicyErrorHandling::ContinueOnError;
RelativeParentsPolicy = ECakePolicyFileRelativeParents::FlattenRelativeParents;

CopyResult = CakeMixLibrary::Dir::CopyFiles(DestDir, IntDir, OpDepth, 
    OverwritePolicy, ErrorPolicy, RelativeParentsPolicy);
```
Here is an example of settings that deviate from the defaults. There are two key differences: 
1. CopyFiles will now attempt to copy all files regardless whether individual files fail to copy.
2. All files will be placed directly in the destination directory, removing any relative subdirectory trees that might have existed in the source directory.

{: .note }
There are also `WithFilter` variations available for CopyFiles/MoveFiles. Outside of filter policy parameters, their usage is identical. 


#### Deleting Items Contained in a Directory
**CakeMixLibrary** offers some utility methods to allow targeted deletion of files or subdirectories. 

We can delete all files at a specific depth via `DeleteFiles`:
```cpp
FCakeDir OldBinaries{ TEXT("x/game/binaries/old") };
auto DeleteDepth = ECakePolicyOpDepth::Shallow;

FCakeDirBatchResult DeleteResult = CakeMixLibrary::Dir::DeleteFiles(OldBinaries, DeleteDepth);

if (DeleteResult.DidAnyWork())
{
    UE_LOG(LogTemp, Warning, TEXT("Deleted [%d] old binary file(s)."), DeleteResult.ItemsProcessed);
}
else
{
    UE_LOG(LogTemp, Warning, TEXT("No old binaries to delete!"))
}
```
We can use the following policies to further customize this delete operation:
{% assign policy_id="FileDelete" %}
* {% include link_policy.md %}
{% assign policy_id="ErrorHandling" %}
* {% include link_policy.md %}

```cpp
auto FileDeletePolicy = ECakePolicyFileDelete::UnlessReadOnly;
ErrorPolicy = ECakePolicyErrorHandling::AbortOnError;

DeleteResult = CakeMixLibrary::Dir::DeleteFiles(OldBinaries, DeleteDepth, FileDeletePolicy, ErrorPolicy);
```

These are the default values for these policy parameters, so this call is the same as the original example; by default DeleteFiles will not delete read only files and it will abort if any single delete operation fails.

We can adjust the parameters to our desired goals:
```cpp
FileDeletePolicy = ECakePolicyFileDelete::EvenIfReadOnly;
ErrorPolicy = ECakePolicyErrorHandling::ContinueOnError;

DeleteResult = CakeMixLibrary::Dir::DeleteFiles(OldBinaries, DeleteDepth, FileDeletePolicy, ErrorPolicy);
```
Now the delete operation will delete read only files and will continue to attempt deletion on all files even if an individual delete operation fails.


We can also delete files with the source **FCakeDir**'s file extension filter via `DeleteFilesWithFilter`:
```cpp
DeleteResult = CakeMixLibrary::Dir::DeleteFilesWithFilter(OldBinaries, DeleteDepth);
```
This shares all the same policy parameters and defaults as **DeleteFiles** and also includes the standard filter modification policies.

If we'd like to only delete subdirectories, we can do so via `DeleteSubdirs`:

```cpp
DeleteResult = CakeMixLibrary::Dir::DeleteSubdirs(OldBinaries, ErrorPolicy);
```

{: .note }
`DeleteSubdirs` only takes an error handling policy since depth is irrelevant (deleting all subdirectories contained directly within the source directory is implicitly a deep operation).

Finally, if we want to delete all items contained within a directory but keep the source directory itself intact, we can use `DeleteAllItems`:
```cpp
DeleteResult = CakeMixLibrary::Dir::DeleteAllItems(OldBinaries, FileDeletePolicy, ErrorPolicy);
```
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

```cpp
FCakeDirBatchResult CreateSubdirsResult = 
    CakeMixLibrary::Dir::CreateSubdirsUnder(ExtraDir, SubdirsToCreate);

UE_LOG(LogTemp, Warning, TEXT("Created [%d] subdirectories under [%s]."),
    CreateSubdirsResult.ItemsProcessed, *ExtraDir.CloneDirName());
```

{% assign policy_id="ErrorHandling" %}
We can use the {% include link_policy.md %} policy to control whether or not we should abort the operation if any of the subdirectories cannnot be created. The default value for this parameter is **AbortOnError**.

```cpp
ErrorPolicy = ECakePolicyErrorHandling::AbortOnError;
CreateSubdirsResult = CakeMixLibrary::Dir::CreateSubdirsUnder(
    ExtraDir, SubdirsToCreate, ErrorPolicy);

ErrorPolicy = ECakePolicyErrorHandling::ContinueOnError;
CreateSubdirsResult = CakeMixLibrary::Dir::CreateSubdirsUnder(
    ExtraDir, SubdirsToCreate, ErrorPolicy);
```
#### Finding the First File with Extension in a Directory
We can get the first file selected by an **FCakeDir**'s file extension filter via `FindFirstFileWithFilter`:
```cpp
if (TOptional<FCakeFile> FirstFile = 
    CakeMixLibrary::Dir::FindFirstFileWithFilter(IntDir, CurrentDepth))
{
    UE_LOG(LogTemp, Warning, TEXT("Got first file: [%s]"), *FirstFile.GetValue().GetFileName())
}
```
The function returns a `TOptional<FCakeFile>` that contains the file if one was found. The usual filter modification policies can be submitted via arguments if the caller wants to adjust the filter logic.

#### Finding Files by File Name in a Directory
There are a few utility functions that can help us retrieve files whose file names match a particular query. 

Before we look at the functions, it is important to understand the underlying logic behind comparing the file names against a query. This logic can be altered by the caller via arguments to the function. In short, a directory iteration for files will occur; each file will have its file name extracted and then that file name will be compared against the query submitted by the caller. The elements that a caller can control are the following:
{% assign subsec_link="file-name-types" %}
{% assign link_desc="this section"%}

{% assign policy_id="NameComparison" %}
1. Whether the query and file name must match exactly, or if the file name merely must contain the query somewhere within it. The is controlled via the {% include link_policy.md %} policy parameter.
2. If the comparison between the query and the file name should be case sensitive. This is controlled via the Unreal core type `ESearchCase`.
3. What type of file name should be extracted from each file. This is controlled via an `ECakeFileNameType` enum, which allows us to select between each of the types (Full, Root, Bare). If you are unfamiliar with file name types, please see {% include rlinks/cakefile_native.md %} for a detailed explanation.

The functions all have the following default settings: the query and file name must match exactly, the comparison is case sensitive, and the full file name should be extracted:
```cpp
auto NameCmpDefault      = ECakePolicyNameComparison::ExactName;
auto CmpCaseDefault      = ESearchCase::CaseSensitive;
auto FileNameTypeDefault = ECakeFileNameType::FullName;
```

```cpp
const FString FileNameQueryExact{ TEXT("player_config.cfg") };

if (TOptional<FCakeFile> FirstFile = 
    CakeMixLibrary::Dir::FindFirstFileNamed(IntDir, FileNameQueryExact, CurrentDepth))
{
    UE_LOG(LogTemp, Warning, TEXT("Got player config file!"))
}
else
{
    UE_LOG(LogTemp, Error, TEXT("Unable to find player config file, aborting!"))
}
```

We can achieve a much broader search by changing the name comparison to `ContainedInName` and making the query more generalized:

```cpp
auto NameCmpContained{ ECakePolicyNameComparison::ContainedInName };
const FString QueryContained{ TEXT("config") };

if (TOptional<FCakeFile> FirstFile = 
    CakeMixLibrary::Dir::FindFirstFileNamed(IntDir, QueryContained, 
        CurrentDepth, NameCmpContained))
{
    UE_LOG(LogTemp, Warning, TEXT("Found a config file!"))
}
else
{
    UE_LOG(LogTemp, Error, TEXT("No config files found!"))
}
```

However, if we are using such broad search terms, we likely are interested in more than one file. For these situations we can use `FindFilesNamed`, which will return a `TArray<FCakeFile>` containing all files that matched against the query:


```cpp
TArray<FCakeFile> FilesNamed{};
auto NameCmpContained{ ECakePolicyNameComparison::ContainedInName };
const FString QueryContained{ TEXT("config") };

FilesNamed = CakeMixLibrary::Dir::FindFilesNamed(IntDir, 
    QueryContained, CurrentDepth, NameCmpContained);
const int32 NumFound{ FilesNamed.Num();
if (NumFound > 0)
{
    UE_LOG(LogTemp, Warning, TEXT("Found [%d] config file(s)."), NumFound)
}
else
{
    UE_LOG(LogTemp, Warning, TEXT("No config files were found!"))
}
```

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

Let's take a look at some example code that uses `RenameFileExtOnly`:
```cpp
FCakeFile ExampleFile { TEXT("/x/game/data/enemies/goblin.obj") };

FCakeFileOpResult RenameResult = 
    CakeMixLibrary::File::RenameFileExtOnly(ExampleFile, TEXT("dat"));
if (!RenameResult)
{
    UE_LOG(LogTemp, Error, 
        TEXT("Failed renaming test file via RenameFileExtOnly. Aborting."))
    return;
}
else 
{
    // ExampleFile is now /x/game/data/enemies/goblin.dat
    UE_LOG(LogTemp, Warning, TEXT("[%s]"), *ExampleFile.GetFileName());
}
```

{: .note }
Assuming `RenameFileExtOnly` / `RenameFileExtOnlySingle` are successful, the associated **FCakeFile**'s path information is automatically updated to reflect the changes.

### Path
Path currently has no functions defined. This may change in the future.

### Results
Currently, the **Results** namespace only has utility functions that convert result / error code / iteration outcome types into human readable strings. For details on how to use these functions, please see the following sections from **Error Handling**:

{% assign link_desc="IO Operation Results" %}
{% assign subsec_link="human-readable-strings" %}
{% include rlinks/error_handling_native.md %}

{% assign link_desc="Iteration Outcome Results" %}
{% assign subsec_link="human-readable-strings-1" %}
{% include rlinks/error_handling_native.md %}
