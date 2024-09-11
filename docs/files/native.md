---
title: Native
parent: Files
nav_order: 1
---

{% assign in_source="CakeFile" %}
{% include components/source_info.html %}

## FCakeFile
{% include components/default_toc.md %}

## Introduction
The native file object in CakeIO is **FCakeFile**. **FCakeFile** is designed to provide an ergonomic and comprehensive interface for common file operations.

## Required Includes
All source code examples going forward will assume that your code has the following include statement:
```cpp
#include "CakeIO/CakePath.h"
#include "CakeIO/CakeFile.h"
```
## Basic Usage
The following covers some of the core interfaces required to utilize and manipulate FCakeFile objects.

### FCakeFile Creation
We can create an FCakeFile through its constructor with either **FString** or **FCakePath** arguments:

```cpp
FCakeFile ViaString{ TEXT("x/game/data/items.db") };

FCakePath PathItemsDatabase{ TEXT("x/game/data/items.db") };
FCakeFile ViaCakePath{ PathItemsDatabase };
```
### File Paths
{% assign link_desc="FCakePath" %}
**FCakeFile** stores its full file path as an {% include rlinks/cakepath_native.md %}.
We can gain access to it via either `operator*` or `GetPath`.

```cpp
FCakeFile ItemsDb{ TEXT("x/game/data/items.db") };

FCakePath FilePath = *ItemsDb;
FCakePath PathMiscDb = ItemsDb.GetPath().CloneWithNewLeaf(TEXT("misc.db"));
```

If we just need to read the full file path as an **FString**, we can use the convenience function `GetPathString`:

```cpp
FCakeFile ItemsDb{ TEXT("x/game/data/items.db") };

UE_LOG(LogTemp, Warning, TEXT("Full file path: [%s]"), *FilePath.GetPathString())
```

To change the file path represented by an FCakeFile object, we can use `SetPath`, which takes **FString** or **FCakePath** as arguments.

```cpp
FCakeFile ItemsDb{ TEXT("x/game/data/items.db") };

FString NewPathString{ TEXT("y/archives/data.zip") };
FCakePath NewPath{ NewPathString };

ItemsDb.SetPath(NewPathString);
ItemsDb.SetPath(NewPath);
```

### File Name
If we want to read the full file name by itself as an **FString**, we can use the member function `GetFileName`:

```cpp
FCakeFile ItemsDb{ TEXT("x/game/data/items.db") };
UE_LOG(LogTemp, Warning, TEXT("The filename is: [%s]"), *ItemsDb.GetFileName());
```

{: .note }
There are other functions for generating different versions of a filename (e.g., one without its file extension data). For more information, please see the [File Name Types](#file-name-types) section.

### File Extension
{% assign link_desc="FCakeFileExt" %}
**FCakeFile** stores an {% include rlinks/cakefileext_native.md %} to represent its file extension. We can gain access to this object via `GetFileExt`:

```cpp
FCakeFile ItemsDb{ TEXT("x/game/data/items.db") };

FCakeFileExt FileExt = ItemsDb.GetFileExt();
```

To get the file extension as an FString, we can use the convenience function GetFileExtString:

```cpp
FCakeFile ItemsDb{ TEXT("x/game/data/items.db") };

UE_LOG(LogTemp, Warning, TEXT("The file ext is: [%s]"), *ItemsDb.GetFileExtString());
```

### File Path Empty/Reset
We can check if an **FCakeFile**'s file path is empty via `PathIsEmpty`, and we can clear an **FCakeFile**'s path via `Reset`:
```cpp
FCakeFile ItemsDb{ TEXT("x/game/data/items.db") };
bool bIsEmpty = ItemsDb.PathIsEmpty(); // => false

ItemsDb.Reset();
bIsEmpty = ItemsDb.PathIsEmpty(); // => true
```

## IO Operations
{% include components/disclaimer_error_handling.md %}

### File Existence
We can check if a file exists on the filesystem via `Exists`:
```cpp
FCakeFile ItemsDb{ TEXT("x/game/data/items.db") };

const bool bExists = ItemsDb.Exists();
```

### Read/Write Operations
**FCakeFile** provides interfaces for handling files as text files or binary (data) files. Text files will use `FString` for read/write operations, and binary files will use `TArray<uint8>` for read/write operations. 

#### Creating Files
The file creation interface is meant to be used on files that do not already exist. To create a text or binary file, we use `CreateTextFile` or `CreateBinaryFile`:

```cpp
FCakeFile ExampleFileText  { FPaths::ProjectIntermediateDir() / TEXT("example_file.txt") };
FCakeFile ExampleFileBinary{ FPaths::ProjectIntermediateDir() / TEXT("example_file.bin") };

FString SourceDataText{ TEXT("This is the source data.") };
TArray<uint8> SourceDataBytes{ 0x99, 0x98, 0x97, 0x96 };

if (!ExampleFileText.CreateTextFile(SourceDataText))
{
    UE_LOG(LogTemp, Error, TEXT("Failed creating example text file."));
}
if (!ExampleFileBinary.CreateBinaryFile(SourceDataBytes))
{
    UE_LOG(LogTemp, Error, TEXT("Failed creating example binary file."));
}
```
{% assign policy_id="OverwriteItems" %}
By default, the create interface will overwrite any pre-existing file. You can control this via the {% include link_policy.md %} policy:
```cpp
ECakePolicyOverwriteItems OverwritePolicy = ECakePolicyOverwriteItems::DoNotOverwriteExistingItems;
if (!ExampleFileText.CreateTextFile(SourceDataText, OverwritePolicy))
{
    UE_LOG(LogTemp, Warning, TEXT("Didn't overwrite existing file as expected."));
}
```
{% assign policy_id="MissingParents" %}
By default, the create interface will ensure that any missing parent directories in the file's path will also be created. You can control this behavior via the {% include link_policy.md %} policy.
```cpp
FCakeFile ExampleFile{ FPaths::ProjectIntermediateDir() / TEXT("m/p/file_dat.txt") };

ECakePolicyMissingParents MissingParentPolicy = ECakePolicyMissingParents::DoNotCreateMissing;
OverwritePolicy = ECakePolicyOverwriteItems::OverwriteExistingItems;

if (!ExampleFile.CreateTextFile(SourceDataText, OverwritePolicy, MissingParentPolicy))
{
    UE_LOG(LogTemp, Warning, TEXT("File creation failed: missing parents."));
}
```

If a file already exists, we generally should use the WriteTextFile or WriteBinaryFile interfaces. However, there are convenience functions that will either create the file if it does not exist or overwrite the file if it does exist via `CreateOrWriteTextFile` and `CreateOrWriteBinaryFile`:

```cpp
FCakeFile ExampleFileText  { FPaths::ProjectIntermediateDir() / TEXT("example_file.txt") };
FCakeFile ExampleFileBinary{ FPaths::ProjectIntermediateDir() / TEXT("example_file.bin") };

FString SourceDataText{ TEXT("This is the source data.") };
TArray<uint8> SourceDataBytes{ 0x99, 0x98, 0x97, 0x96 };

if (!ExampleFileText.CreateOrWriteTextFile(SourceDataText))
{
    UE_LOG(LogTemp, Error, TEXT("Failed creating or writing example text file."));
}
if (!ExampleFileBinary.CreateOrWriteBinaryFile(SourceDataBytes))
{
    UE_LOG(LogTemp, Error, TEXT("Failed creating or writing example binary file."));
}
```
#### Reading Files
To read the data from a text or binary file, we use `ReadFileAsString` or `ReadFileAsBytes`:
```cpp
FString FileDataString{};
if (ExampleFileText.ReadFileAsString(FileDataString))
{
    UE_LOG(LogTemp, Warning, TEXT("Text file data: [%s]"), *FileDataString)
}

TArray<uint8> FileDataBytes{};
if (ExampleFileBinary.ReadFileAsBytes(FileDataBytes))
{
    UE_LOG(LogTemp, Warning, TEXT("Read [%d] bytes of data."), FileDataBytes.Num())
}
```

There is a second version of the read interface which returns a `TOptional` of the desired data type; with this version we lose specific error information but we still will know if the read operation failed when the optional type is unset: 
```cpp
if (TOptional<FString> TextData = ExampleFileText.ReadFileAsString())
{
    UE_LOG(LogTemp, Warning, TEXT("Text file data: [%s]"), **TextData)
}

if (TOptional<TArray<uint8>> ByteData = ExampleFileBinary.ReadFileAsBytes())
{
    UE_LOG(LogTemp, Warning, TEXT("Read [%d] bytes of data."), ByteData.GetValue().Num())
}
```

#### Writing Files
We use the writing interfaces when a file exists and we want to overwrite its contents with new contents.

```cpp
FString WriteDataText { TEXT("This is data from write that has overwritten the source data.") };
TArray<uint8> WriteDataBytes { 0x80, 0x80, 0x80, 0x80 };

if (!ExampleFileText.WriteTextToFile(WriteDataText))
{
    UE_LOG(LogTemp, Error, TEXT("Failed WriteTextToFile. Aborting."))
    return;
}
if (!ExampleFileBinary.WriteBytesToFile(WriteDataBytes))
{
    UE_LOG(LogTemp, Error, TEXT("Failed WriteBytesToFile. Aborting."))
    return;
}
```

If we want to append data to the file instead of overwriting its old contents, we use `AppendTextToFile` or `AppendBytesToFile` :

```cpp
FString AppendDataText{ TEXT("\nThis is an extra line from append!") };
TArray<uint8> AppendDataBytes{ 0xCA, 0xFE };

if (!ExampleFileText.AppendTextToFile(AppendDataText))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed appending data to text file!"));
}

if (!ExampleFileBinary.AppendBytesToFile(AppendDataBytes))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed appending data to binary file!"));
}
```

### Copying Files
We can copy a file to another location via `CopyFile`. This takes an `FCakePath` argument that represents the source directory into which the file should be copied.

```cpp
FCakeFile SourceFile{ TEXT("abilities/magic/spells.db") };
FCakePath DestDir{ TEXT("some/other/dir") };

if (!SourceFile.CopyFile(DestDir))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed copying file to dest dir."))
}
```
{% assign policy_id="OverwriteItems" %}
By default, `CopyFile` will overwrite a pre-existing file if it shares the same location. We can control this via the {% include link_policy.md %} policy:
```cpp
if (!SourceFile.CopyFile(DestDir, ECakePolicyOverwriteItems::DoNotOverwriteExistingItems))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed copying file to dest dir."))
}
```
{% assign policy_id="MissingParents" %}
By default, `CopyFile` will create any missing parents contained in `DestDir`. We can control that via the {% include link_policy.md %} policy: 
```cpp
auto OverwritePolicy = ECakePolicyOverwriteItems::DoNotOverwriteExistingItems;
auto MissingParentsPolicy = ECakePolicyMissingParents::DoNotCreateMissing;

if (!SourceFile.CopyFile(OtherDir, OverwritePolicy, MissingParentsPolicy))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed copying file to dest dir."))
}
```
Sometimes we might want to copy a file with a new name, and for that we can use `CopyFileAliased`. In addition to a destination path, we also need to provide a new name that the copied file should have:
```cpp
FCakeFile SourceFile{ TEXT("abilities/magic/spells.db") };
FCakePath DestDir{ TEXT("/s/other/dir") };
FString CopyAlias{ TEXT("spells_archive.db") };

if (!SourceFile.CopyFileAliased(DestDir, CopyAlias))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed copying file with alias to dest dir."))
}
```
In the example above, assuming the copy succeeds, the copied file's path will be `/s/other/dir/spells_archive.db`.

{: .note }
`CopyFileAliased` shares the same policy parameters and policy defaults as `CopyFile`.


### Moving Files

{: .note }
It is important to understand that a move is actually a compound IO operation -- a source file is copied to the desired location, and then that source file is deleted. This is important to keep in mind when examining the error codes from failed moves -- in terms of IO operations, a move could fail during the copy operation or the delete operation, but there is no dedicated error code for a "move" failure.

We can move a file to another location via `MoveFile`. This takes an `FCakePath` argument that represents the source directory into which the file should be moved.

```cpp
FCakeFile SourceFile{ TEXT("abilities/magic/spells.db") };
FCakePath DestDir{ TEXT("some/other/dir") };

if (!SourceFile.MoveFile(DestDir))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed moving file to dest dir."))
    return;
}
```
{% assign policy_id="OverwriteItems" %}
By default, `MoveFile` will overwrite a pre-existing file if it shares the same location. We can control this via the {% include link_policy.md %} policy:
```cpp
if (!SourceFile.MoveFile(DestDir, ECakePolicyOverwriteItems::DoNotOverwriteExistingItems))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed moving file to dest dir."))
}
```
{% assign policy_id="MissingParents" %}
By default, `MoveFile` will create any missing parents contained in `DestDir`. We can control this via the {% include link_policy.md %} policy:
```cpp
auto OverwritePolicy = ECakePolicyOverwriteItems::DoNotOverwriteExistingItems;
auto MissingParentsPolicy = ECakePolicyMissingParents::DoNotCreateMissing;

if (!SourceFile.MoveFile(OtherDir, OverwritePolicy, MissingParentsPolicy))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed moving file to dest dir."))
}
```
Sometimes we might want to move a file and change its name, and for that we can use `MoveFileAliased`. In addition to a destination path, we also need to provide a new name for the file after it has been moved:
```cpp
FCakeFile SourceFile{ TEXT("abilities/magic/spells.db") };
FCakePath DestDir{ TEXT("/s/other/dir") };
FString MoveAlias{ TEXT("spells_archive.db") };

if (!SourceFile.MoveFileAliased(DestDir, MoveAlias))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed moving file with alias to dest dir."))
}
```
In the example above, assuming the move succeeds, the final file path will be `/s/other/dir/spells_archive.db`.

{: .note }
`MoveFileAliased` shares the same policy parameters and policy defaults as `MoveFile`.


We can also rename a file with `RenameFile`.
```cpp
FCakeFile SourceFile{ TEXT("abilities/magic/spells.db") };

FString NewName{ TEXT("magic_spells.db") };

if (!SourceFile.RenameFile(NewName))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed renaming spells.db!"))
}
```
{% assign policy_id="OverwriteItems" %}
By default, `RenameFile` will overwrite any pre-existing file. We can control this via the {% include link_policy.md %} policy:
```cpp
if (!SourceFile.RenameFile(NewName, ECakePolicyOverwriteItems::DoNotOverwriteExistingItems))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed renaming spells.db!"))
}
```


### Deleting Files
To delete a file, use `DeleteFile`:


```cpp
FCakeFile SpellsDb{ TEXT("abilities/magic/spells.db") };

if (!SpellsDb.DeleteFile())
{
    UE_LOG(LogTemp, Warning, TEXT("Failed to delete [%s]!"), *SpellsDb.GetFileName());
}
```
{: .note }
In the event that the file does not exist, `DeleteFile` will return a NOP `FCakeFileError`.

{% assign policy_id="FileDelete" %}
By default, `DeleteFile` will not delete a file that is marked as read-only by the operating system. We can change this behavior via the {% include link_policy.md %} policy:

```cpp
ECakePolicyFileDelete DeletePolicy = ECakePolicyFileDelete::EvenIfReadOnly;

if (!SpellsDb.DeleteFile(DeletePolicy))
{
    UE_LOG(LogTemp, Warning, TEXT("Failed to delete [%s]!"), *SpellsDb.GetFileName());
}
```

### Retrieving File OS Information
To get the Unreal `FFileStatData` for an **FCakeFile**, we simply need to call `GetStatData`:

```cpp
FCakeFile TestFile{ TEXT("enemies/ai/goblin.cpp") };

if (TOptional<FFileStatData> StatData = TestFile.GetStatData())
{
    FFileStatData& DataUnwrapped = *StatData;
    UE_LOG(LogTemp, Warning, TEXT("StatData file size: [%d] bytes."), DataUnwrapped.FileSize);
    UE_LOG(LogTemp, Warning, TEXT("StatData access time: [%s]"), *DataUnwrapped.AccessTime.ToString());
    UE_LOG(LogTemp, Warning, TEXT("StatData creation time: [%s]"), *DataUnwrapped.CreationTime.ToString());
}
```

We can also retrieve some individual stats if we don't need the whole `FFileStatData`.

We can attempt to retrieve the size of a file via `GetFileSizeInBytes`:
```cpp
if (TOptional<int64> FileSize = TestFile.GetFileSizeInBytes())
{
    UE_LOG(LogTemp, Warning, TEXT("GetFileSizeInBytes file size: [%d] bytes."), *FileSize);
}
```

We can attempt to retrieve the modified timestamp via `GetModifiedTimestamp`:
```cpp
if (TOptional<FDateTime> ModStamp = TestFile.GetModifiedTimestamp())
{
    FString DateStr{ ModStamp.GetValue().ToString() };
    UE_LOG(LogTemp, Warning, TEXT("GetModifiedTimestamp: [%s]"), *DateStr);
}
```

We can attempt to retrieve the access timestamp via `GetAccessTimestamp`:
```cpp
if (TOptional<FDateTime> AccessStamp = TestFile.GetAccessTimestamp())
{
    FString DateStr{ AccessStamp.GetValue().ToString() };
    UE_LOG(LogTemp, Warning, TEXT("GetAccessTimestamp: [%s]"), *DateStr);
}
```

We can also try to set the modified timestamp to a custom value via `SetModifiedTimestamp`.
```cpp
FDateTime NewMod{ FDateTime::Now() };
NewMod -= FTimespan::FromDays(1.0);
if (TestFile.SetModifiedTimestamp(NewMod))
{
    UE_LOG(LogTemp, Warning, TEXT("SetModifiedTimestamp successful. New mod time: [%s]"), *NewMod.ToString())
}
else
{
    UE_LOG(LogTemp, Warning, TEXT("Failed modifying the test file's modified timestamp."))
}
```

## Advanced Usage
### File Name Types
**CakeIO** classifies file names into three different categories. Using the file name `info.cdr.txt` as an example:
1. **Full Name**: The file name with all of its extensions: `info.cdr.txt`
2. **Root Name**: The file name with its trailing extension removed: `info.cdr`
3. **Bare Name**: The file name without any extensions: `info`

{: .note }
When FileName is used by itself, **Full Name** is implied. Thus, `CloneFileName` will clone the full file name, whereas `CloneFileNameBare` will clone the bare file name.

We can read the full file name of an **FCakeFile** via `GetFileName`:
```cpp
FCakeFile FakeFile{ TEXT("/x/game/data/items.core.db") };

UE_LOG(LogTemp, Warning, TEXT("    GetFileName: [%s]"), *FakeFile.GetFileName());
```

If we need a copy of the full name, we can use `CloneFileName`:
```cpp
FString FullName = FakeFile.CloneFileName();
UE_LOG(LogTemp, Warning, TEXT("    CloneFileName: [%s]"), *FullName);
```

We can get a copy of the root file name via `CloneFileNameRoot`:
```cpp
FString RootName = FakeFile.CloneFileNameRoot();
UE_LOG(LogTemp, Warning, TEXT("    CloneFileNameRoot: [%s]"), *RootName);
```

We can get a copy of the bare file name via `CloneFileNameBare`:
```cpp
FString BareName = FakeFile.CloneFileNameBare();
UE_LOG(LogTemp, Warning, TEXT("    CloneFileNameBare: [%s]"), *BareName);
```

### Low-Level FileHandles
In order to support custom read/write logic, **FCakeFile** provides interfaces to obtain an `IFileHandle` to the file represented by the FCakeFile.

#### Standard IFileHandle 
You can get an `IFileHandle` pointer for the target **FCakeFile** via the member function `GetFileHandle`. 

{: .warning }
`GetFileHandle` will return `nullptr` when the opening fails, so always check to ensure the pointer is valid before using it!

{% assign policy_id="FileWriteMode" %}
We need to submit an ECakeFileOpenMode argument that determines what kind of access the handle should obtain, and we also can control how data will be written in Write/ReadWrite mode via the {% include link_policy.md %} policy:

```cpp
auto OpenMode  = ECakeFileOpenMode::ReadAndWrite;
auto WriteMode = ECakePolicyFileWriteMode::OverwriteData;

if (IFileHandle* ReadWriteHandle = ItemsDb.GetFileHandle(OpenMode, WriteMode))
{
    //...
    delete ReadWriteHandle; // close the handle to the file when we are done
}
```

By default, GetFileHandle will use the `OverwriteData` setting, so the code below is equivalent to the code above:
```cpp
if (IFileHandle* ReadWriteHandle = ItemsDb.GetFileHandle(ECakeFileOpenMode::ReadAndWrite))
{
    //...
    delete ReadWriteHandle; // close the handle to the file when we are done
}
```

When we are getting a read only handle, the FileWriteMode policy is ignored, so there is no need to set it:
```cpp
if (IFileHandle* ReadHandle = ItemsDb.GetFileHandle(ECakeFileOpenMode::Read))
{
    //...
    delete ReadHandle; // close the handle to the file when we are done
}
```

Here is one way we might obtain an appending write handle:
```cpp
if (IFileHandle* AppendHandle = ItemsDb.GetFileHandle(ECakeFileOpenMode::Write, ECakePolicyFileWriteMode::AppendData))
{
    //...
    delete AppendHandle; // close the handle to the file when we are done
}
```

#### Scoped File Handles
There is a second interface to get access to an `IFileHandle` via `GetScopedFileHandle`. This will return an `FFileWarden` object instead of an `IFileHandle` pointer. This object will automatically close its associated `IFileHandle` for us when it goes out of scope.

`FFileWarden` is a very simple object to use. We can use either its `operator bool` or `IsValid` function to ensure that it holds a non-null `IFileHandle` pointer, and then we use `operator*` or `GetRawHandle` to access the `IFileHandle` pointer:


```cpp
{
    FFileWarden ReadHandle = ItemsDb.GetScopedFileHandle(ECakeFileOpenMode::Read);
    if (ReadHandle.IsValid())
    {
        IFileHandle* InnerHandle = ReadHandle.GetRawHandle();
        //...
    }

    if (ReadHandle)
    {
        IFileHandle* InnerHandle = *ReadHandle;
        // ...
    }
} // ReadHandle will close its internal IFileHandle here via destructor.
```

We can also combine the assignment and `operator bool` check:

```cpp
if (FFileWarden ReadHandle = ItemsDb.GetScopedFileHandle(ECakeFileOpenMode::Read))
{
    // The call to GetRawHandle is safe because we have passed the operator bool check 
    IFileHandle* InnerHandle = ReadHandle.GetRawHandle();
    //...
} // ReadHandle will close its internal IFileHandle here via destructor.
```

{: .warning }
Always use `operator bool` or `IsValid` before attempting to access the `IFileHandle` pointer held by an `FFileWarden`. It will only be non-null when the file is successfully accessed.
