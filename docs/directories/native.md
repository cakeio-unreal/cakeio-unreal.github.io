---
title: Native
parent: Directories
nav_order: 1
---

{% assign in_source="CakeDir" %}
{% include components/source_info.html %}

{% assign filter_syntax_link = "[Extension Filter Syntax](#file-extension-filter-syntax)" %}

## FCakeDir
{% include components/default_toc.md %}

## Introduction
The native directory object in CakeIO is **FCakeDir**. **FCakeDir** primary purpose is to provide a comprehensive interface for directory iteration and common IO operations.

## Required Includes
All source code examples going forward will assume that your code has the following include statement:
```cpp
#include "CakeIO/CakePath.h"
#include "CakeIO/CakeDir.h"
```

## Basic Usage

### The File Extension Filter
**FCakeDir** contains a member field called the file extension filter. The file extension filter is used to selectively visit files during file iteration. Many functions throughout **FCakeDir** will involve the file extension filter in some way. 

{: .note }
The file extension filter is implemented via the type `FFileExtFilter`. In most situations you will never have to use this type directly; however, if the event arises you can find its fully documented source code at `CakeIO/Misc/FileExtFilter.h`.

#### File Extension Filter Syntax
Functions that involve modifying the file extension filter use a special syntax via strings. This allows us to add or remove multiple file extensions within a single filter command. The syntax is very simple: we simply must separate each file extension element via the `|` (pipe) character. 

As an example, if we wanted to modify both `.txt` and `.bin` in the same command, we would use the string "txt|bin" for the extension command:
```cpp
FCakeDir DirectoryGame{ TEXT("x/game") };

DirectoryGame.SetExtensionFilter("txt|bin");
```
The order doesn't matter, so we just as easily could have used "bin|txt":
```cpp
FCakeDir DirectoryGame{ TEXT("x/game") };

DirectoryGame.SetExtensionFilter("bin|txt");
```

It doesn't matter if we include the leading `.` character for extensions, it will be added for us afterward. Thus, all of the following calls will parse into the same file extension list: `[.txt, .bin]`:
```cpp
DirectoryGame.SetExtensionFilter("txt|bin");
DirectoryGame.SetExtensionFilter(".txt|bin");
DirectoryGame.SetExtensionFilter(".txt|.bin");
DirectoryGame.SetExtensionFilter("txt|.bin");
```

The leading `.` is also not required for {% glossary ext_multi, display: multi extensions %}:
```cpp
DirectoryGame.AddExtensionsToFilter("dat|.cdr.txt|tar.zip");
```

As the example above shows, if we were trying to add `.cdr.txt` to the extension filter, we could do so either with `cdr.txt` or `.cdr.txt`.

{: .note }
>The extension filter is extremely lenient when parsing file extension lists. It can handle extra symbols and empty entries without incident (it will merely skip them). For example, `|.|..cdr.|txt|bin||` will correctly parse the command into the following extension list `[.cdr, .txt, .bin]`. Therefore, you do not have to do exhaustive syntax checking when accepting filter commands from outside sources (like from a GUI).


### FCakeDir Creation
We can create an **FCakeDir** via its constructor by submitting the path to the directory **FCakeDir** should hold. We can submit either an **FString** or an **FCakePath**.
```cpp
FCakeDir DirectoryGame{ TEXT("x/game") };
    // Path: "x/game"
    // File Extension Filter: []

FCakePath PathGameDir{ TEXT("x/game") };
FCakeDir DirGame{ PathGameDir };
    // Path: "x/game"
    // File Extension Filter: []
```
We can pass a second FString argument to **FCakeDir**'s constructors, and this will set the starting elements in the file extension filter:

```cpp
FCakeDir DirectoryGame{ TEXT("x/game"), TEXT("bin|dat") };
    // Path: "x/game"
    // File Extension Filter: [.bin, .dat]

FCakePath PathGameDir{ TEXT("x/game") };
FString ExtFilterStr{ TEXT("dat|bin|cdr.txt") };

FCakeDir DirGame{ PathGameDir, ExtFilterStr };
    // Path: "x/game"
    // File Extension Filter: [.dat, .bin, .cdr.txt]
```

{: .note }
This example uses file extension filter syntax; see {{ filter_syntax_link }} for more information.

We can get a copy of an existing **FCakeDir** via `Clone`:


```cpp
FCakeDir DirectoryGame{ TEXT("x/game"), TEXT("bin|dat") };
    // Path: "x/game"
    // File Extension Filter: [.bin, .dat]

FCakeDir GameCloned = DirectoryGame.Clone();
    // Path: "x/game"
    // File Extension Filter: [.bin, .dat]
```
{% assign policy_id="ExtFilterClone" %}
By default, this function will also ensure that the cloned **FCakeDir** has an identical file extension filter. If we do not want the cloned **FCakeDir** to inherit the file extension filter, we can change this behavior via the {% include link_policy.md %} policy.

```cpp
FCakeDir DirectoryGame{ TEXT("x/game"), TEXT("bin|dat") };
    // Path: "x/game"
    // File Extension Filter: [.bin, .dat]

FCakeDir ClonedWithoutExtFilter = DirectoryGame.Clone(ECakePolicyExtFilterClone::DoNotCloneFilter);
    // Path: "x/game"
    // File Extension Filter: []
```
### Directory Path and Name

We can gain access to the **FCakePath** representing an **FCakeDir** via `operator*` or `GetPath`:

```cpp
FCakeDir DirectoryGame{ TEXT("x/game"), TEXT("bin|dat") };

UE_LOG(LogTemp, Warning, TEXT("Parent path: [%s]"), **DirectoryGame.GetPath().CloneParentPath())
UE_LOG(LogTemp, Warning, TEXT("Directory Path: [%s]"), ***DirectoryGame);
```

When we just need to get an **FCakeDir**'s directory path as a string, we can use the convenience function `GetPathString`:
```cpp
UE_LOG(LogTemp, Warning, TEXT("Directory Path: [%s]"), *DirectoryGame.GetPathString());
```
To read the directory name as a string, we can use `GetDirName`:
```cpp
UE_LOG(LogTemp, Warning, TEXT("Directory Name: [%s]"), *DirectoryGame.GetDirName());
```

We can change the path an **FCakeDir** is using via `SetPath`. It is overloaded to accept either `FString` or `FCakePath` arguments.
```cpp
FString NewPathString { TEXT("y/archive/data") };
FCakePath NewPath{ NewPathString };

DirectoryGame.SetPath(NewPathString);
DirectoryGame.SetPath(NewPath);
```

We can check if an **FCakeDir**'s directory path is empty via `PathIsEmpty`:
```cpp
FCakeDir DirectoryGame{ TEXT("x/game"), TEXT("bin|dat") };
bool bPathIsEmpty{ true };

bPathIsEmpty = DirectoryGame.PathIsEmpty(); // => false
```

We can reset the directory path to be empty via `ResetPath`:
```cpp
DirectoryGame.ResetPath();
bPathIsEmpty = DirectoryGame.PathIsEmpty(); // => true
```

### Modifying the File Extension Filter
We can change and modify the elements in the file extension filter after we have created an **FCakeDir**.

{: .note }
All of the examples in this section use file extension filter syntax; see {{ filter_syntax_link }} for more information.

It is important to understand that the file extension filter only stores unique file extension entries. 

When we want to add extensions to the filter we use `AddExtensionsToFilter`. This function returns the number of extensions successfully added.
```cpp
FCakeDir DirectoryGame{ TEXT("x/game"), TEXT("bin|dat") };

int32 ExtensionsAdded = DirectoryGame.AddExtensionsToFilter("png|jpeg");
UE_LOG(LogTemp, Warning, TEXT("Added [%d] extensions to the filter set!"), ExtensionsAdded);
```
The number added will be less than the number submitted if any of the submitted extensions already exist in the filter.


{% assign link_desc="FCakeFileExt" %}
We can gain read-only access to the filter set. Internally each entry of the filter set is stored as an {% include rlinks/cakefileext_native.md %}:
```cpp
UE_LOG(LogTemp, Warning, TEXT("Printing Extensions"))
for (FCakeFileExt const& FileExt : IntDir.GetExtensionFilter().GetExtSet())
{
    UE_LOG(LogTemp, Warning, TEXT("    *[%s]"), **FileExt)
}
```

{: .note }
`GetExtensionFilter` returns a read-only reference to an `FFileExtFilter`, which is the object `FCakeDir` uses for its file extension filter. Its fully documented source code can be found at `CakeIO/Misc/FileExtFilter.h`.

We can remove extensions from the filter via `RemoveExtensionsFromFilter`. This function returns the amount of extensions successfully removed from the filter set:
```cpp
FCakeDir DirectoryGame{ TEXT("x/game"), TEXT("bin|dat") };

int32 ExtensionsRemoved = DirectoryGame.RemoveExtensionsFromFilter("png|jpeg|gif");
UE_LOG(LogTemp, Warning, TEXT("Removed [%d] extensions from the filter set!"), ExtensionsRemoved);
```

{: .hint }
The Add/Remove extension filter functions are not marked as `[[nodiscard]]`, so they can easily be called without caching the amount added/removed.

To remove all entries from the extension filter, we can use `ResetExtensionFilter`:
```cpp
DirectoryGame.ResetExtensionFilter();
```

We can use `SetExtensionFilter` to ensure the extension filter only contains entries found in the command string argument:
```cpp
FCakeDir DirectoryGame{ TEXT("x/game"), TEXT("bin|dat") };
    // Path: "x/game"
    // File Extension Filter: [.bin, .dat]

DirectoryGame.SetExtensionFilter("json|txt");
    // Path: "x/game"
    // File Extension Filter: [.json, .txt]
```

As we can see in the example above, the call to `SetExtensionFilter` results in the previous entries `.bin` and `.dat` being removed from the filter and only the entries from the command string `.json` and `.txt` are in the set.

We can check if an **FCakeDir**'s extension filter is empty via `ExtensionFilterIsEmpty`:
```cpp
bool bFilterIsEmpty = DirectoryGame.ExtensionFilterIsEmpty(); // => false
```
### Directory Comparison Operators
All comparison operators are tested against the **FCakeDir**'s directory path. Equality is defined via `operator==` and `operator!=`. It is overloaded to accepted **FCakeDir**, **FCakePath**, or **FString**. 

Just like **FCakePath**, an **FCakeDir** is equal to another directory/path/string if it refers to the same location on the filesystem.

```cpp
FString PathStringData{ TEXT("x/game/data") };
FCakePath PathDataDir{ PathStringData };
FCakeDir DirData{ PathDataDir };
FCakeDir DirMisc{ TEXT("x/game/misc") };

bool bIsEqual{ false };

bIsEqual = DirData == DirMisc;
bIsEqual = DirData == PathDataDir;
bIsEqual = DirData == PathStringData;

bool bIsNotEqual{ false };

bIsNotEqual = DirData != DirMisc;
bIsNotEqual = DirData != PathDataDir;
bIsNotEqual = DirData != PathStringData;
```

{: .note }
Operators `<`, `<=`, `>`, `>=` are defined for **FCakeDir** so that they can be sorted in collections. Internally they just use **FString**'s definition for the operators on the **FCakeDir**'s file path. Thus, an **FCakeDir** will sort exactly like an **FString**.

### Resetting All Data
In the situation where we want to reset all data on **UCakeDir**, we can use `Reset`. This will reset both the path and the extension filter for us:
```cpp
UCakeDir DirectoryGame{ TEXT("x/game"), TEXT("bin|dat") };
    // Path: "x/game"
    // File Extension Filter: [.bin, .dat]

DirectoryGame.Reset();
    // Path: ""
    // File Extension Filter: []
```

## IO Operations
{% include components/disclaimer_error_handling.md %}

### Directory Existence
We can check if the directory represented by an **FCakeDir** exists on the file system via `Exists`:

```cpp
FCakeDir DirectoryGame{ TEXT("x/game") };

if (DirectoryGame.Exists())
{
    // ...
}
```

### Creating Directories
We can attempt to create the directory represented by an **FCakeDir** via `CreateDir`:
```cpp
FCakeDir DirectoryGame{ TEXT("/x/game") };

if (!DirectoryGame.Exists())
{
    if (!DirectoryGame.CreateDir())
    {
        UE_LOG(LogTemp, Error, TEXT("Failed creating game directory."));
    }

}
```

{% assign policy_id="MissingParents" %}
By default, `CreateDir` will ensure that any missing parent directories in the directory's path will also be created. You can control this behavior directly via the {% include link_policy.md %} policy.

```cpp
if (!DirectoryGame.Exists())
{
    if (!DirectoryGame.CreateDir(ECakePolicyMissingParents::DoNotCreateMissing))
    {
        UE_LOG(LogTemp, Error, TEXT("Failed creating game directory."));
    }
}
```

For situations where we aren't certain a directory exists and would like it created if it doesn't exist, we can use the convenience function `ExistsOrCreate`:

```cpp
if (!DirectoryGame.ExistsOrCreate())
{
    UE_LOG(LogTemp, Error, TEXT("Directory game does not exist and could not be created."));
}
```
### Copying Directories
We can copy a directory and its contents to another location via `CopyDir`. This takes an `FCakePath` or an `FCakeDir` argument that represents the source directory into which the directory should be copied.

```cpp
FCakeDir DirectoryGame{ TEXT("/x/game") };

FCakePath PathDestDir{ TEXT("/y/archive/") };
FCakeDir DestDir{ PathDestDir };

// FCakePath 
if (!DirectoryGame.CopyDir(PathDestDir))
{
    UE_LOG(LogTemp, Error, TEXT("Failed copying game directory to archives!"))
}

// FCakeDir 
if (!DirectoryGame.CopyDir(DestDir))
{
    UE_LOG(LogTemp, Error, TEXT("Failed copying game directory to archives!"))
}
```
{% assign policy_id="OverwriteItems" %}
By default, `CopyDir` will overwrite a pre-existing directory if it shares the same location. We can control this via the {% include link_policy.md %} policy:
```cpp
auto OverwritePolicy = ECakePolicyOverwriteItems::DoNotOverwriteExistingItems;
if (!DirectoryGame.CopyDir(DestDir, OverwritePolicy))
{
    UE_LOG(LogTemp, Error, TEXT("Failed copying game directory to archives!"))
}
```
{% assign policy_id="MissingParents" %}
By default, `CopyDir` will create any missing parents contained in `DestDir`. We can control that via the {% include link_policy.md %} policy: 
```cpp
auto MissingParentsPolicy = ECakePolicyMissingParents::DoNotCreateMissing;
if (!DirectoryGame.CopyDir(DestDir, OverwritePolicy, MissingParentsPolicy))
{
    UE_LOG(LogTemp, Error, TEXT("Failed copying game directory to archives!"))
}
```

Sometimes we might want to copy a directory but give the copied directory a different name, and for that we can use `CopyDirAliased`. In addition to a destination path, we also need to provide a new name that the copied directory should have:
```cpp
FString DirAlias{ TEXT("game_archive") };

if (!DirectoryGame.CopyDirAliased(DestDir, DirAlias))
{
    UE_LOG(LogTemp, Error, TEXT("Failed copying aliased game directory to archives!"))
}
```
In the example above, assuming the copy succeeds, the copied directory's path will be `/y/archive/game_archive`.

{: .note }
`CopyDirAliased` shares the same policy parameters and policy defaults as `CopyDir`.

### Moving Directories
We can move a directory and its contents to another location via `MoveDir`. This takes an `FCakePath` or an `FCakeDir` argument that represents the source directory into which the directory should be moved.

```cpp
FCakeDir DirectoryGame{ TEXT("/x/game") };

FCakePath PathDestDir{ TEXT("/y/archive/") };
FCakeDir DestDir{ PathDestDir };

// FCakePath 
if (!DirectoryGame.MoveDir(PathDestDir))
{
    UE_LOG(LogTemp, Error, TEXT("Failed moving game directory to archives!"))
}

// FCakeDir 
if (!DirectoryGame.MoveDir(DestDir))
{
    UE_LOG(LogTemp, Error, TEXT("Failed moving game directory to archives!"))
}
```
{% assign policy_id="OverwriteItems" %}
By default, `MoveDir` will overwrite a pre-existing directory if it shares the same location. We can control this via the {% include link_policy.md %} policy:
```cpp
auto OverwritePolicy = ECakePolicyOverwriteItems::DoNotOverwriteExistingItems;
if (!DirectoryGame.MoveDir(DestDir, OverwritePolicy))
{
    UE_LOG(LogTemp, Error, TEXT("Failed moving game directory to archives!"))
}
```
{% assign policy_id="MissingParents" %}
By default, `MoveDir` will create any missing parents contained in `DestDir`. We can control that via the {% include link_policy.md %} policy: 
```cpp
auto MissingParentsPolicy = ECakePolicyMissingParents::DoNotCreateMissing;
if (!DirectoryGame.MoveDir(DestDir, OverwritePolicy, MissingParentsPolicy))
{
    UE_LOG(LogTemp, Error, TEXT("Failed moving game directory to archives!"))
}
```

Sometimes we might want to move a directory but give the moved directory a different name, and for that we can use `MoveDirAliased`. In addition to a destination path, we also need to provide a new name that the moved directory should have:
```cpp
FString DirAlias{ TEXT("game_archive") };

if (!DirectoryGame.MoveDirAliased(DestDir, DirAlias))
{
    UE_LOG(LogTemp, Error, TEXT("Failed copying aliased game directory to archives!"))
}
```
In the example above, assuming the move succeeds, the moved directory's path will be `/y/archive/game_archive`.

{: .note }
`MoveDirAliased` shares the same policy parameters and policy defaults as `MoveDir`.

We can also rename a directory with `RenameDir`.
```cpp
FCakeDir DirectoryGame{ TEXT("/x/game") };
FString DirAlias{ TEXT("game_archive") };

if (!DirectoryGame.RenameDir(DirAlias))
{
    UE_LOG(LogTemp, Error, TEXT("Failed renaming [%s] to [%s]."), *DirectoryGame.GetDirName(), *DirAlias)
}
```
{% assign policy_id="OverwriteItems" %}
By default, `RenameDir` will overwrite an existing directory if it shares the same name as the new name. We can control that behavior directly via the {% include link_policy.md %} policy: 
```cpp
auto OverwritePolicy = ECakePolicyOverwriteItems::DoNotOverwriteExistingItems;

if (!DirectoryGame.RenameDir(DirAlias, OverwritePolicy))
{
    UE_LOG(LogTemp, Error, TEXT("Failed renaming [%s] to [%s]."), *DirectoryGame.GetDirName(), *DirAlias)
}
```

{: .note }
Whenever a move / rename succeeds, the **FCakeDir** will automatically update all of its path information to reflect its new location.

### Deleting Directories
We can delete the directory and all of its contents via `DeleteDir`:
```cpp
if (!DirectoryGame.DeleteDir())
{
    UE_LOG(LogTemp, Error, TEXT("Failed deleting [%s]!"), *DirectoryGame.GetDirName())
}
```
### Retrieving Directory OS Information
We can get the `FFileStatData` for an **FCakeDir** via `GetStatData`:

```cpp
if (TOptional<FFileStatData> DirStatOpt = DirectoryGame.GetStatData())
{
    FFileStatData& DirStat = *DirStatOpt;
    bool bIsDir = DirStat.bIsDirectory; // => true
    FDateTime CreationTimestamp = DirStat.CreationTime;
}
```

{: .warning }
`FFileStatData` is used for both files and directories; as such, some fields (such as file size) will not apply to a directory.


{% include common_cakedir_iteration.md %}

### Iteration Callbacks
{% assign policy_id="OpDepth" %}
All iteration processes offered by **FCakeDir** will require at least two arguments: An {% include link_policy.md %} that determines the iteration depth and a callback that will be invoked each time an item is visited. This callback's signature will changed based upon two factors: the target directory element type will determine the callback's parameter list (e.g., a file iteration will pass an **FCakeFile** argument per file visited) and the iteration style will determine the callback's return type (e.g., a Search iteration style returns an `ECakeDirSearchSignal`.). The following sections will go into more specific details about using each iteration style. 

### Sequential Iterations Usage
{% include assumed_fcakedir.md %}

Let's first examine the callback signatures for all three directory element types:
```cpp
// Sequential Iteration (Items)
auto ItemSequentialCallback = [](FCakePath ItemPath, bool bIsDir) -> void
{
    // Any iteration callback for Items will be sent an FCakePath representing 
    // the current element visited, and a boolean to indicate whether that path 
    // is a directory.

    const FString Leaf { ItemPath.CloneLeafAsString() };
    if (bIsDir)
    {
        UE_LOG(LogTemp, Warning, TEXT("Visited directory: [%s]"), *Leaf);
    }
    else
    {
        UE_LOG(LogTemp, Warning, TEXT("Visited file: [%s]"), *Leaf);
    }
};

// Sequential Iteration (Files)
auto FileSequentialCallback = [](FCakeFile File) -> void
{
    // Any iteration callback for files will be sent an FCakeFile 
    // representing the current file being visited.
    UE_LOG(LogTemp, Warning, TEXT("Visited file: [%s]"), *File.GetFileName());
};

// Sequential Iteration (Subdirs)
auto SubdirSequentialCallback = [](FCakeDir Subdir) -> void
{
    // Any iteration callback for subdirectories will be sent 
    // an FCakeDir representing the current subdirectory being visited.
    UE_LOG(LogTemp, Warning, TEXT("Visited subdirectory: [%s]"), *Subdir.GetDirName());
};

```

We should emphasize two things: firstly, the callbacks' parameter lists change based on the directory element type we are visiting. This will hold true across all iteration style callbacks, and the parameter list will always be the same for a given directory element type regardless of the iteration style being used. Secondly, all callbacks for a Sequential iteration return `void`. This is because Sequential iteration offers no way for a caller to terminate the iteration early; once launched, the iteration will visit _all_ target elements at the specified depth.

With our callbacks defined, we must decide upon a depth that the iteration should traverse. We control iteration depth via the policy {% include link_policy.md %}:
```cpp
auto DesiredDepth = ECakePolicyOpDepth::Shallow;
```
We are now ready to launch an iteration on our directory. Sequential iteration function names take the form `Iterate<Element>`, where `<Element>` is the directory element type we are visiting. For arguments, we only need pass the depth followed by the appropriate callback:

```cpp
if (!IntDir.IterateItems(DesiredDepth, ItemSequentialCallback))
{
    UE_LOG(LogTemp, Warning, TEXT("IterateItems failed to launch!"));
}

if (!IntDir.IterateFiles(DesiredDepth, FileSequentialCallback))
{
    UE_LOG(LogTemp, Warning, TEXT("IterateFiles failed to launch!"));
}

if (!IntDir.IterateSubdirs(DesiredDepth, SubdirSequentialCallback))
{
    UE_LOG(LogTemp, Warning, TEXT("IterateSubdirs failed to launch!"));
}
```
Sequential iterations return an `FCakeDirIterationResult` indicating the outcome of the iteration. We can use it as a boolean via `operator bool` as shown in the preceding examples, or we can store the result and handle the outcomes explicitly:

```cpp
FCakeDirIterationResult ItrSequentialResult = 
	IntDir.IterateSubdirs(DesiredDepth, SubdirSequentialCallback);

switch (ItrSequentialResult.Outcome)
{
    case ECakeDirIterationOutcome::DIO_DidNotLaunch:
        UE_LOG(LogTemp, Warning, TEXT("IterateSubdirs failed to launch!"));
        break;

    case ECakeDirIterationOutcome::DIO_Completed:
        UE_LOG(LogTemp, Warning, TEXT("IterateSubdirs completed without incident!"));
        break;

    case ECakeDirIterationOutcome::DIO_Aborted:
        UE_LOG(LogTemp, Warning, TEXT("This should never happen with a sequential iteration."));
        break;
}

```
Since callers cannot stop a Sequential iteration once it has launched, an outcome of **Aborted** should never occur. That outcome is reserved for **Guarded** iterations, which are covered in the next section.

{% assign link_desc="this section" %}
{% assign subsec_link="failure-to-launch" %}
{: .note }
All iteration outcomes can return a `DidNotLaunch` value, which means the iteration never started. For a detailed explanation about how this can occur, please see {% include rlinks/error_handling_native.md %} of error handling.


Even though we declared our callbacks and depth prior to the iterate call, we could just as easily have submitted our arguments inline:

```cpp
ItrSequentialResult = IntDir.IterateSubdirs(
ECakePolicyOpDepth::Deep,
[](FCakeDir Subdir) -> void 
    {
        UE_LOG(LogTemp, Warning, TEXT("Visited subdir: [%s]"), *Subdir.GetDirName());
    }
);

```

{% assign subsec_link="fcakediriterationresult" %}
{: .note }
For a deep dive in `FCakeDirIterationResult` usage, see {% include rlinks/error_handling_native.md %} of error handling.

### Guarded Iteration Usage
{% include assumed_fcakedir.md %}
Let's first examine the callback signatures required for **Guarded** iterations:

```cpp
// Guarded Iteration (Items)
auto ItemGuardedCallback = [](FCakePath ItemPath, bool bIsDir) -> ECakeDirIterationSignal
{
    if (!bIsDir)
    {
        // We return the Abort signal when we want the 
        // iteration to abort early.
        return ECakeDirIterationSignal::DIS_Abort;
    }
    // We return the Continue signal whenever we want the 
    // iteration to continue and the next element to be visited.
    return ECakeDirIterationSignal::DIS_Continue;
};

// Guarded Iteration (Files)
auto FileGuardedCallback = [](FCakeFile File) -> ECakeDirIterationSignal
{
    // The caller is in complete control as to what is considered 
    // an "error" worth terminating over.
    if (File.GetFileExt() != FString(".jpg"))
    {
        // We return the Abort signal when we want the 
        // iteration to abort early.
        return ECakeDirIterationSignal::DIS_Abort;
    }
    // We return the Continue signal whenever we want the 
    // iteration to continue and the next element to be visited.
    return ECakeDirIterationSignal::DIS_Continue;
};

// Guarded Iteration (Subdirs)
auto SubdirGuardedCallback = [](FCakeDir Subdir) -> ECakeDirIterationSignal
{
    // The caller is in complete control as to what is considered 
    // an "error" worth terminating over.
    if (Subdir.CloneDirName() != TEXT("SpecialDir"))
    {
        // We return the Abort signal when we want the 
        // iteration to abort early.
        return ECakeDirIterationSignal::DIS_Abort;
    }
    // We return the Continue signal whenever we want the 
    // iteration to continue and the next element to be visited.
    return ECakeDirIterationSignal::DIS_Continue;
};

```

Compared to Sequential callbacks, only the return type has changed. Because the caller can stop an iteration early, we must return a signal that indicates whether the iteration should proceed to the next item. The signal type is `ECakeDirIterationSignal` and it holds only two meaningful values: **Continue** and **Abort**. When we need to terminate an iteration due to an error, we should return `ECakeDirIterationSignal::DIS_Abort`. Otherwise, we should return `ECakeDirIterationSignal::DIS_Continue`.

As with all iteration styles, we need to choose a depth that this iteration should traverse:
```cpp
auto DesiredDepth = ECakePolicyOpDepth::Shallow;
```

To launch a Guarded iteration, we use the function family `IterateGuarded<Element>`, where `<Element>` refers to the directory element type being visited.


```cpp
if (!IntDir.IterateGuardedItems(DesiredDepth, ItemGuardedCallback))
{
    UE_LOG(LogTemp, Error, TEXT("IterateGuardedItems encountered an error!"));
}

if (!IntDir.IterateGuardedFiles(DesiredDepth, FileGuardedCallback))
{
    UE_LOG(LogTemp, Error, TEXT("IterateGuardedFiles encountered an error!"));
}
```

Just like Sequential iterations, Guarded iterations return an `FCakeDirIterationResult` that indicates the outcome of the iteration. Unlike Sequential iterations, the **Aborted** value now is actually used; it will be returned whenever one of our callbacks sends the `Abort` signal.

```cpp
FCakeDirIterationResult ItrGuardedResult = 
    IntDir.IterateGuardedSubdirs(DesiredDepth, SubdirGuardedCallback);
switch (ItrGuardedResult.Outcome)
{
    case ECakeDirIterationOutcome::DIO_DidNotLaunch:
        UE_LOG(LogTemp, Warning, TEXT("SubdirsGuarded iteration failed to start."))
            break;
    case ECakeDirIterationOutcome::DIO_Completed:
        UE_LOG(LogTemp, Warning, TEXT("SubdirsGuarded iteration completed without incident."))
            break;
    case ECakeDirIterationOutcome::DIO_Aborted:
        UE_LOG(LogTemp, Warning, TEXT("SubdirsGuarded iteration was aborted early!"))
            break;
}
```

{% assign link_desc="this section" %}
{% assign subsec_link="failure-to-launch" %}
{: .note }
All iteration outcomes can return a `DidNotLaunch` value, which means the iteration never started. For a detailed explanation about how this can occur, please see {% include rlinks/error_handling_native.md %} of error handling.

We can also easily inline all of our arguments to a Guarded iteration if we prefer that style:
```cpp
ItrGuardedResult = IntDir.IterateGuardedSubdirs(
    ECakePolicyOpDepth::Deep,
    [](FCakeDir NextDir)
    {
        if (NextDir.GetDirName() == TEXT("AbortDir"))
        {
            return ECakeDirIterationSignal::DIS_Abort;
        }

        return ECakeDirIterationSignal::DIS_Continue;
    }
);
```


{% assign subsec_link="fcakediriterationresult" %}
{: .note }
For a closer look at `FCakeDirIterationResult` and its usage, see {% include rlinks/error_handling_native.md %} of error handling.


### Search Iteration Usage
{% include assumed_fcakedir.md %}

The final iteration style, Search Iteration, is also the most complex. A **Search Iteration** allows the user to set a custom goal and terminate the iteration when the goal has been satisfied or when a halting error has been encountered. Let's start by looking at the callback signatures:


```cpp
// Search callbacks return ECakeDirSearchSignal to control iteration flow.

constexpr int32 SearchLimit{ 3 };
int32 ItemCount{ 0 };

// Search Iteration (Items)
auto ItemSearchCallback = [SearchLimit, &ItemCount](FCakePath ItemPath, bool bIsDir) -> ECakeDirSearchSignal
{
    // There are three signal values we can return.
    if (SearchLimit <= 0)
    {
        // If we encounter a situation we consider an error worth 
        // aborting the iteration over, we can return the Abort signal.
        UE_LOG(LogTemp, Warning, TEXT("Search limit is set to a value <= 0. Aborting."));
        return ECakeDirSearchSignal::DSS_Abort;
    }

    ++ItemCount;
    // When we have accomplished our goal for this iteration, we 
    // return the Complete signal.
    if (ItemCount > SearchLimit) { return ECakeDirSearchSignal::DSS_Complete; }

    // When our requirements have not been met and we want 
    // to keep visiting elements, we return the Continue signal.
    return ECakeDirSearchSignal::DSS_Continue;
};

// As with Items, the only changes we need to make to File and Subdir 
// variants involve the return types.

// Search Iteration (Files)
auto FileSearchCallback = [](FCakeFile File) -> ECakeDirSearchSignal
{
    // We can send an abort Signal if we want to stop 
    // the iteration due to an error.
    return ECakeDirSearchSignal::DSS_Abort;
};

// Search Iteration (Subdirs)
auto SubdirSearchCallback = [](FCakeDir Subdir) -> ECakeDirSearchSignal
{
    // A search iteration that never returns DSS_Complete will result in 
    // a Failed search outcome.
    return ECakeDirSearchSignal::DSS_Continue;
};
```

As the code above shows, search iteration callbacks return an `ECakeDirSearchSignal`, which is used to control the iteration flow. During the iteration, when we visit an item and still have not yet completed our goal, we return a **Continue** signal. If we accomplish our goal after the current item is visited, we should instead return **Complete**. If we encounter a halting error during the search, we can also return the **Abort** signal to terminate early.

As with all iteration styles, we need to choose a depth that this iteration should traverse:
```cpp
auto DesiredDepth = ECakePolicyOpDepth::Shallow;
```

We launch a search iteration via the function family `IterateSearch<Element>`, where `<Element>` is the directory element type being visited:
```cpp
FCakeDirSearchResult ItrSearchResult = IntDir.IterateSearchItems(DesiredDepth, ItemSearchCallback);
switch (ItrSearchResult.Outcome)
{
    case ECakeDirSearchOutcome::DSO_DidNotLaunch:
        UE_LOG(LogTemp, Warning, TEXT("ItemSearch iteration failed to start."))
        break;
    case ECakeDirSearchOutcome::DSO_Succeeded:
        UE_LOG(LogTemp, Warning, TEXT("ItemSearch found all target elements."))
        break;
    case ECakeDirSearchOutcome::DSO_Failed:
        UE_LOG(LogTemp, Warning, TEXT("ItemSearch failed to find all target elements."))
        break;
    case ECakeDirSearchOutcome::DSO_Aborted:
        UE_LOG(LogTemp, Warning, TEXT("ItemSearch was aborted early due to an error."))
        break;
}
```
A search iteration will return an `FCakeDirSearchResult` which holds an outcome. There are three outcomes specifically related to a search:
1. **Succeeded**: The goal was accomplished during the search iteration.
2. **Failed**: All target elements were visited and the goal was not satisfied.
3. **Aborted**: A halting error was encountered and the iteration was aborted.

{% assign link_desc="this section" %}
{% assign subsec_link="failure-to-launch" %}
{: .note }
All iteration outcomes can return a `DidNotLaunch` value, which means the iteration never started. For a detailed explanation about how this can occur, please see {% include rlinks/error_handling_native.md %} of error handling.


We can also use the result as a boolean via its `operator bool`, just like the other result types. In this case, `operator bool` will return true only if the result is **Succeeded**, and it will be false otherwise.

```cpp
if (!IntDir.IterateSearchSubdirs(DesiredDepth, SubdirSearch))
{
    UE_LOG(LogTemp, Warning, TEXT("Our subdirectory search failed, as expected."));
}

if (!IntDir.IterateSearchFiles(DesiredDepth, FileSearch))
{
    UE_LOG(LogTemp, Warning, TEXT("Our file search was aborted, as expected."));
}
```
{% assign subsec_link="fcakedirsearchresult" %}
{: .note }
For a more comprehensive look at `FCakeDirSearchResult` usage, see {% include rlinks/error_handling_native.md %} of error handling.


We can also easily call a search iteration with inline arguments:
```cpp
ItrSearchResult = IntDir.IterateSearchSubdirs(
    ECakePolicyOpDepth::Deep,
    [](FCakeDir NextDir)
    {
        return ECakeDirSearchSignal::DSS_Continue;
    }
);
```
### Filtered Iteration Usage
{% include assumed_fcakedir.md %}
Filtered Iteration is a special iteration variant that only applies to file iterations. Filtered Iteration uses **FCakeDir**'s file extension filter to selectively visit files during an iteration.

Every style of iteration that targets files has a filtered version; the filtered iteration function will share the name of the non-filtered version, but will have the added suffix `WithFilter`. For example, the filtered version of `IterateFiles` is named `IterateFilesWithFilter`.

All filtered iteration functions take the exact same callback signature as the non-filtered version; however, the filtered iteration function has extra parameters associated with the filter logic.

Let's look at a brief example using Sequential iteration:

```cpp
auto SequentialFilterCallback = [](FCakeFile InFile) -> void 
{
    UE_LOG(LogTemp, Warning, TEXT("    StandardFilter Found File: [%s]"), *InFile.GetFileName());
};
```
Take note -- the callback for a filtered iteration is the exact same as an unfiltered iteration. A filtered iteration only changes which files are visited, which has nothing do to with our callback.

We'll select a depth, and then launch our filtered iteration via `IterateFilesWithFilter`:
```cpp
ECakePolicyOpDepth CurrentDepth = ECakePolicyOpDepth::Shallow;

FCakeDirIterationResult ItrSequentialRes = 
    IntDir.IterateFilesWithFilter(CurrentDepth, SequentialFilterCallback);
```

{: .warning }
A filtered iteration will fail to launch if there are no entries in the source **FCakeDir**'s file extension filter.

Other than the function name, this doesn't look any different from a call to the non-filtered version. However, filtered iterations use the following two policies to control how files are selected:
{% assign policy_id="ExtFilterMode" %}
* {% include link_policy.md %}
{% assign policy_id="ExtMatchMode" %}
* {% include link_policy.md %}


```cpp
FCakeDirIterationResult IterateFilesWithFilter(
    ECakePolicyOpDepth Depth, 
    FIterateOpFile Callback, 
    ECakePolicyExtFilterMode FilterMode = ECakePolicyExtFilterMode::SelectMatchingOnly, 
    ECakePolicyExtMatchMode   MatchMode = ECakePolicyExtMatchMode::MultiOrSingle
) const;
```

By default, filtered iteration functions will use the filter mode of **SelectMatchingOnly** and the match mode of **MultiOrSingle**. This means that we will only visit files whose extensions are found in the extension filter, and that our matching logic will be more permissive. 

{: .note }
For a detailed description of the matching logic for `ECakePolicyExtMatchMode`, please visit the policy documentation linked previously.

We can invert the filter and ignore files whose extensions are found in the extension filter:

```cpp
ItrSequentialRes = IntDir.IterateFilesWithFilter(
    CurrentDepth, 
    SequentialFilterCallback, 
    ECakePolicyExtFilterMode::ExcludeMatching
);
```

We can also adjust the extension matching logic to be more strict by using the **ExactMatch** match mode policy value:
```cpp
ItrSequentialRes = IntDir.IterateFilesWithFilter(
    CurrentDepth, 
    SequentialFilterCallback, 
    ECakePolicyExtFilterMode::ExcludeMatching, 
    ECakePolicyExtMatchMode::ExactMatch
);
```

{: .note }
The other filtered functions, `IterateGuardedFilesWithFilter` and `IterateSearchFilesWithFilter` share the policy parameters and default settings.
