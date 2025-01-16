## Overview
CakeIO provides CakeDir objects that offer a comprehensive and ergonomic interface for directory traversal and other common directory IO operations. Just like CakeFile objects, CakeDir objects store their paths using CakePath objects. In addition to their path, however, CakeDir objects also have a special array of [CakeFileExt](file-extensions.md) objects, called the **file extension filter**, which can be used to filter the results when traversing through the files of a directory.

--8<-- "native-bp-diff.md"

=== "C++"
    The native directory object in CakeIO is **FCakeDir**. FCakeDir is defined in `CakeDir.h`, and all code examples will assume the following include:

    ``` c++
    #include "CakeIO/CakeDir.h"
    ```

=== "Blueprint"
    The Blueprint directory object in CakeIO is **UCakeDir**. UCakeDir is defined in `Blueprint/CakeDir_BP.h`:

    ``` c++
    #include "CakeIO/Blueprint/CakeDir_BP.h"
    ```

## Basic Usage

### Building CakeDir Objects
=== "C++"
    We can build an **FCakeDir** via its constructor by submitting an `FCakePath` argument that represents the directory location.
	```c++ 
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };
        // Path: "x/game"
        // File Extension Filter: []
	```
    We can pass a string-like object as the second argument to an **FCakeDir** constructor if we want to also set the starting elements in its [file extension filter](#file-extension-filter):

	```c++ 
    FCakeDir DirectoryGame{ 
        FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("txt|bin")};
        // Path: "x/game"
        // File Extension Filter: [.txt, .bin]
	```
=== "Blueprint"
    We can build a CakeDir object via `BuildCakeDir`:

	{{ bp_img_dir('Build Cake Dir') }}

    The second argument is a string that represents the extensions we want in its file extension filter: 

    {{ bp_img_dir('Build Cake Dir Ext Filter') }}
    
    !!! info 
        Please see the [file extension filter](#file-extension-filter) section for details on the extension filter and the syntax used here to specify extensions

    To build a CakeDir with an empty path and extension filter, we use `BuildCakeDirEmpty`:

    {{ bp_img_dir('Build Cake Dir Empty') }}

We can get a copy of an existing **FCakeDir** via `Clone`:
=== "C++"
    ```cpp
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("bin|dat") };
        // Path: "x/game"
        // File Extension Filter: [.bin, .dat]

    FCakeDir GameCloned{ DirectoryGame.Clone() };
        // Path: "x/game"
        // File Extension Filter: [.bin, .dat]
    ```

    ```c++ hl_lines="5"
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("bin|dat") };
        // Path: "x/game"
        // File Extension Filter: [.bin, .dat]

    FCakeDir ClonedWithoutExtFilter{ 
        DirectoryGame.Clone(ECakePolicyExtFilterClone::DoNotCloneFilter)};
        // Path: "x/game"
        // File Extension Filter: []
    ```

    !!! tip
        In general, Clone functions in CakeIO behave identically to copy constructors. However, `FCakeDir`'s Clone function is an exception since it provides more control than its copy constructor counterpart.

=== "Blueprint"
    {{ bp_img_dir('Clone') }}

By default, this function will also ensure that the cloned **FCakeDir** has an identical file extension filter. We can control this directly via the [ExtFilterClone](special-types/policies.md#extfilterclone) policy parameter. (This parameter is optional in C++).

### Accessing the Directory Path
=== "C++"
    We can access an **FCakeDir**'s associated **FCakePath** via `operator*` or `GetPath`:
	```c++ hl_lines="6-7"
    auto PrintPath = [](const FCakePath& Path) { 
        UE_LOG(LogTemp, Warning, TEXT("Path: [%s]"), **Path);
    };
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("bin|dat") };

    PrintPath(*DirectoryGame);
    PrintPath(DirectoryGame.GetPath());
	```
    When we just want to use the directory path as a string, we can use the convenience function `GetPathString`:
	```c++ hl_lines="7"
    auto PrintPathStr = [](const FString& Path) { 
        UE_LOG(LogTemp, Warning, TEXT("Path: [%s]"), *Path);
    };

    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("bin|dat") };

    PrintPathStr(DirectoryGame.GetPathString());
	```

=== "Blueprint"
    To read the directory path as a string, we use `GetPathString`:

	{{ bp_img_dir('Get Path String') }}

    To get a copy of the CakePath object that holds the directory path, we use `ClonePath`:

	{{ bp_img_dir('Clone Path') }}


### Modifying the Directory Path
=== "C++"
    We can change the path an **FCakeDir** is using via `SetPath` or `StealPath`. `SetPath` operates on `const FCakePath&`, and `StealPath` operates on `FCakePath&&`.  

    ```c++ hl_lines="4-5"
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("bin|dat") };
    FCakePath NewPath{ TEXTVIEW("y/archive/data") };

    DirectoryGame.SetPath(NewPath);
    DirectoryGame.StealPath( FCakePath{TEXTVIEW("x/other/archive")} );
    ```
    !!! tip
        Favor `StealPath` unless you are copying from a source `FCakePath` that needs to be used elsewhere.

    We can check if an **FCakeDir**'s directory path is empty via `PathIsEmpty`:

    ```c++ hl_lines="3"
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("bin|dat") };

    const bool bPathIsEmpty{ DirectoryGame.PathIsEmpty() }; // => false
    ```

    We can reset the directory path to be empty via `ResetPath`:

    ```c++ hl_lines="1"
    DirectoryGame.ResetPath();

    const bool bPathIsEmpty{ DirectoryGame.PathIsEmpty() }; // => true
    ```
    --8<-- "ad-newreservedsize.md"

=== "Blueprint"
    To change the path of an existing CakeDir object, we use `SetPath`:

	{{ bp_img_dir('Set Path') }}

    To see if the path a CakeDir object holds is empty, we use `PathIsEmpty`:

	{{ bp_img_dir('Path Is Empty') }}

    To clear the path a CakeDir object holds, we use `ResetPath`:

	{{ bp_img_dir('Reset Path') }}

    --8<-- "note-bp-newreservedsize.md"

### Accessing the Directory Name
We can get the directory name as a string via `CloneDirName`:

=== "C++"
	```c++ hl_lines="3"
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("bin|dat") };

    FString DirName{ DirectoryGame.CloneDirName() }; // => "game"
	```
=== "Blueprint"
	{{ bp_img_dir('Clone Dir Name') }}

--8<-- "warn-maybe-empty.md"

### Directory Equality
Directory equality mirrors path equality: two CakeDir objects are equal if they refer to the same directory location on the filesystem. The extension filters are not taken into consideration for equality since this would lead to unintuitive, misleading results.
=== "C++"
    We use `operator==` and `operator!=` for **FCakeDir** equality, and can compare them against other **FCakeDir** or **FCakePath** objects.

	```c++ hl_lines="8 9 11 12"
    FCakePath PathData{ TEXTVIEW("X:/game/data") };

    FCakeDir DirData{ PathData };
    FCakeDir DirArc { FCakePath{TEXTVIEW("X:/arc")} };

    bool bAreEqual{ false };

    bAreEqual = DirData == PathData; // => true
    bAreEqual = DirData == DirArc; // => false

    bAreEqual = DirData != PathData; // => false
    bAreEqual = DirData != DirArc; // => true
	```
=== "Blueprint"
    We can check if two CakeDir objects are equal via `Is Equal To`:

	{{ bp_img_dir('Is Equal To') }}

    We can check if two CakeDir objects are not equal via `Is Not Equal To`:

	{{ bp_img_dir('Is Not Equal To') }}

### File Extension Filter
All CakeDir objects have their own file extension filter, which contains a collection of unique file extensions stored as [FCakeFileExt](file-extensions.md) objects. This filter is used on specialized variations of file traversal and allows callers to decide which files in a directory are visited based upon their file extensions.

=== "C++"
    We can get access to either a const or mutable reference to the file extension filter via `GetExtFilter` and `GetExtFilterMut`, respectively:

    ```c++
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("bin|dat") };

	const FCakeExtFilter& FilterConst  { DirectoryGame.GetExtFilter()    };
	      FCakeExtFilter& FilterMutable{ DirectoryGame.GetExtFilterMut() };
    ```

    For details on how to use the extension filter, please see the [FCakeExtFilter documentation](special-types/cakeextfilter.md).

=== "Blueprint"
    Blueprint users will access the file extension filter via specific **UCakeDir** member functions. More details can be found [here](special-types/cakeextfilter.md).


### Clearing All Data
To clear the path and the file extension filter on a CakeDir object, we use `Reset`:
=== "C++"

    ```c++ hl_lines="5"
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("bin|dat") };
        // Path: "x/game"
        // File Extension Filter: [.bin, .dat]

    DirectoryGame.Reset();
        // Path: ""
        // File Extension Filter: []
    ```
    --8<-- "ad-newreservedsize.md"

=== "Blueprint"
	{{ bp_img_dir('Reset') }}

    --8<-- "note-bp-newreservedsize.md"

## IO Operations
--8<-- "disclaimer-error-handling.md"

--8<-- "ad-policies.md"

### Checking Directory Existence
To check if a CakeDir object's referenced directory exists on the filesystem, we use `Exists`:
=== "C++"

    ```c++
	FCakeDir DirectoryGame { FCakePath{TEXTVIEW("X:/game")} };

	if (DirectoryGame.Exists())
	{
		UE_LOG(LogTemp, Warning, 
			TEXT("The game directory exists on the filesystem!"))
	}
	else
	{
		UE_LOG(LogTemp, Warning, 
			TEXT("The game directory does not exist on the filesystem!"))
	}
    ```

=== "Blueprint"
	{{ bp_img_dir('Exists') }}

### Creating Directories
To create the directory a CakeDir object references, we use `CreateDir`:
=== "C++"
    ```c++
        FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };

        if (!DirectoryGame.Exists())
        {
            if (!DirectoryGame.CreateDir())
            {
                UE_LOG(LogTemp, Error, TEXT("Failed creating game directory."));
            }
        }
    ```

=== "Blueprint"
	{{ bp_img_dir('Create Dir') }}

We can use the [MissingParents](policies.md#missingparents) policy parameter to control whether or not missing parent directories are allowed to be created. (This parameter is optional in C++).

`ExistsOrCreate` is a convenience function that checks if a directory exists and tries to create it for us if it doesn't. This function is ideal to use when you need a directory to exist before proceeding, but you aren't sure if it already exists.

=== "C++"
    ```c++
    if (!DirectoryGame.ExistsOrCreate())
    {
        UE_LOG(LogTemp, Error, TEXT("Directory game does not exist and could not be created."));
    }
    ```
=== "Blueprint"
	{{ bp_img_dir('Exists Or Create') }}

!!! note
    `ExistsOrCreate` always creates any missing parent directories.

### Deleting Directories
We can delete a CakeDir's referenced directory and all of its contents via `DeleteDir`:
=== "C++"
    ```c++ hl_lines="3"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };

	if (!DirectoryGame.DeleteDir())
	{
		UE_LOG(LogTemp, Error, TEXT("Failed deleting [%s]!"), *DirectoryGame.CloneDirName())
	}
    ```
=== "Blueprint"
	{{ bp_img_dir('Delete Dir') }}

### Copying Directories
To copy the directory a CakeDir represents to another location on the filesystem, use `CopyDir`, which takes a CakePath argument that represents the destination directory for the copied directory:
=== "C++"

    ```c++ hl_lines="5"
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };

    FCakePath PathDestDir{ TEXT("Z:/archive/") };

    if (!DirectoryGame.CopyDir(PathDestDir))
    {
        UE_LOG(LogTemp, Error, TEXT("Failed copying game directory to archives!"))
    }
    ```

	--8<-- "ad-settings-createitem.md"

=== "Blueprint"
	{{ bp_img_dir('Copy Dir') }}

We can give the copied directory a new name easily via `CopyDirAliased`. In addition to a destination path, we also need to provide a new name that the copied directory should have: 

=== "C++"

    ```c++ hl_lines="5"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };

	FCakePath PathDestDir{ TEXT("Z:/archive/") };

	if (!DirectoryGame.CopyDirAliased(PathDestDir, TEXTVIEW("game_archive")))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed copying game directory to archives!"))
	}
    ```
	--8<-- "ad-settings-createitem.md"

=== "Blueprint"
	{{ bp_img_dir('Copy Dir Aliased') }}

Assuming the copy succeeds, the copied directory's path would be `Z:/archive/game_archive`.


### Moving Directories
To move the directory a CakeDir represents to another location on the filesystem, use `MoveDir`, which takes a CakePath argument that represents the destination directory for the moved directory:

=== "C++"

    ```c++ hl_lines="5"
    FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };

    FCakePath PathDestDir{ TEXT("Z:/archive/") };

    if (!DirectoryGame.MoveDir(PathDestDir))
    {
        UE_LOG(LogTemp, Error, TEXT("Failed moving game directory to archives!"))
    }
    ```

	--8<-- "ad-settings-createitem.md"

=== "Blueprint"
	{{ bp_img_dir('Move Dir') }}

We can give the moved directory a new name easily via `MoveDirAliased`. In addition to a destination path, we also need to provide a new name that the moved directory should have: 

=== "C++"

    ```c++ hl_lines="5"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };

	FCakePath PathDestDir{ TEXT("Z:/archive/") };

	if (!DirectoryGame.MoveDirAliased(PathDestDir, TEXTVIEW("game_archive")))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed moving game directory to archives!"))
	}
    ```
	--8<-- "ad-settings-createitem.md"

=== "Blueprint"
	{{ bp_img_dir('Move Dir Aliased') }}

Assuming the move succeeds, the moved directory's path would be `Z:/archive/game_archive`.

### Changing Directory Name 
To change the name of a directory on the filesystem, use `ChangeDirName`:

=== "C++"
    ```c++ hl_lines="4"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };
	FString NewName{ TEXT("game_main") };

	if (!DirectoryGame.ChangeDirName(NewName))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed renaming [%s] to [%s]."), *DirectoryGame.CloneDirName(), *NewName)
	}
    ```
=== "Blueprint"
	{{ bp_img_dir('Delete Dir') }}

We can control whether or not the name change is allowed to overwrite existing directories via the second parameter, which is an [OverwriteItems](policies.md#overwriteitems) policy. (This parameter is optional in C++.)


### Retrieving Directory OS Stat Information
=== "C++"
    We can get the `FFileStatData` for an **FCakeDir** via `QueryStatData`:

    ```c++ hl_lines="3"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };

	if (TCakeOrderDir<FFileStatData> DirStatOpt = DirectoryGame.QueryStatData())
	{
		FFileStatData& DirStat = *DirStatOpt;
		bool bIsDir = DirStat.bIsDirectory; // => true
		FDateTime CreationTimestamp = DirStat.CreationTime;
		// ...
	}
    ```
    `QueryStatData` will return a `TCakeOrderDir<FFileStatData>` that holds both the [FCakeResultDirIO](special-types/results.md#fcakeresultdirio) and the `FFileStatData`, which will be valid only if the query operation doesn't fail. For more information about TCakeOrder types and their usage, see [this section](special-types/orders.md#tcakeorder).


=== "Blueprint"
    We can get the stat data for a CakeDir's referenced directory via `QueryStatData`:

	{{ bp_img_dir('Query Stat Data') }}

    This returns a CakeFileStatData object. Please note that some of the fields only apply to files, such as file size. They will not hold meaningful values even when the stat data is successfully retrieved for a directory.

	{{ bp_img_dir('Cake File Stat Data') }}

    !!! warning
        It is imperative to ensure the query operation succeeded before using any of the values in the stat data struct. They will not hold accurate information when the query operation fails.

## Directory Traversal 
Directory traversal is a vital part of working with file systems, and Cake Directory objects offer a comprehensive set of traversal interfaces. At its core, a traversal operation involves invoking a user-supplied callback function on each directory element (file or subdirectory) that is being visited by the traversal function.

### Traversal Overview
Before we examine the traversal interfaces, it is important to understand some terminology and guiding principles behind CakeIO's traversal design. A traversal has three main traits that define its behavior: 

1. **Style**: Determines the behavior of the traversal operation.
1. **Target**: Determines what kind of element (directories, files, or both) will be visited by a traversal operation.
1. **Depth**: Determines if a traversal is allowed to continue down into children subdirectories.

Each of these traits is independent of one another, and so they can be freely mixed in any combination the caller needs. Now, let's look a bit more in depth into each of the traits.

#### Traversal Depth
Traversal depth is controlled via the [OpDepth](policies.md#opdepth) policy. Full details about each setting can be found in its documentation.

#### Traversal Targets
There are three targets a caller can select for a traversal operation to visit at the specified depth: items will visit all files and directories, files will visit only files, and subdirectories will only visit subdirectories. The callback signature for traversals will change based on the target selected. For each target element visited, an items traversal will produce a [CakePath](paths.md) object and a boolean indicating if it is a directory, a files traversal will produce a [CakeFile](files.md) object, and a subdirectory traversal will produce a CakeDir object.

#### Traversal Styles
There are three styles of traversal that are offered by CakeIO, listed from simplest to the most advanced: unguarded traversal, guarded traversal, and search traversals.

Unguarded traversal will visit every target element at the specified depth. The caller has no ability to terminate the traversal early. In essence, this is traversal with no error handling. 

Guarded traversal will attempt to visit every target element at a specified depth, but it can be stopped early by the caller if an error is encountered. In essence, this is traversal with error handling enabled. The goal of a guarded traversal is still to visit all target elements at the specified depth.

Search traversal visits target elements at the specified depth until some conditions is met -- the caller is in complete control of this condition. As the name implies, a search traversal does not always expect to visit every target element within a directory -- it wishes to terminate as soon as it finds what it is looking for. Search traversals can be terminated early in two states -- if an error is encountered or if the search has found what it needs. If a search traversal visits all target elements and the search is not satisfied, then this traversal will be considered a failure (in terms of searching, not in terms of errors).

#### Traversal Function Naming
Traversal functions utilize the following naming pattern: `Traverse<style><target>`. Unguarded traversals do not have a style identifier in their name because they are the simplest form. Let's say we wish to traverse the files of a directory. We could use the following functions to traverse the files with each style:

1. Unguarded Traversal: `TraverseFiles`
1. Guarded Traversal: `TraverseGuardedFiles`
1. Search Traversal: `TraverseSearchFiles`

#### Traversal Callbacks
Every traversal function will require a callback that is meant to handle each target element that is visited. The signature is based upon two factors: the return type of the callback is determined by the traversal style, and the parameter list is determined by the target element.

>Return Types

| Traversal Style | Return Type|
| :-------------- | :----------|
| Unguarded       | void       |
| Guarded         | [ECakeSignalGuarded](special-types/signals.md#ecakesignalguarded) |
| Search          | [ECakeSignalSearch](special-types/signals.md#ecakesignalsearch) | 

>Parameter Lists


| Target | Parameter List                    |
| :----- | :-------------------------------- |
| Item   | [CakePath](paths.md), bool bIsDir |
| File   | [CakeFile](files.md)              |
| Subdir | CakeDir                           | 


### Using Traversals
--8<-- "disclaimer-error-handling-traversal.md"

Using traversals with Cake Directory objects follows a common pattern: we select a style and target by using a particular function, and then we submit an [OpDepth](policies.md#opdepth) policy parameter that determines the traversal depth and a callback parameter that will be called each time a target element is visited. The callback signature will change based upon the style and target element, and some functions will accept more parameters beyond the depth and callback. We will now look at examples using each traversal style.

#### Unguarded Traversals
Unguarded Traversals are the simplest form of traversal. Unless the traversal fails to launch due to an error, it will visit every target element at a specified depth for a given Cake Directory object. The user has no control over the traversal operation's termination, and the traversal will not stop until all elements at the specified depth are visited.
The callback signature for unguarded traversals must accept the input parameters for the target element, and the callback should return void since no traversal control is granted to the caller.

=== "C++"
    The callback signatures for **FCakeDir** are described via the following `TFunction` template aliases:

    ```c++ 
        /** Callback signature for an unguarded item traversal. */
        using FTraversalCbItem    = TFunction< void (FCakePath Path, bool bIsDir) >;

        /** Callback signature for an unguarded file traversal. */
        using FTraversalCbFile    = TFunction< void (FCakeFile File) >;

        /** Callback signature for an unguarded subdirectory traversal. */
        using FTraversalCbSubdir  = TFunction< void (FCakeDir Subdir) >;
    ```

=== "Blueprint"
    When making Unguarded Traversal callbacks, we can use either Events or Functions since we don't need to return a value. The examples shown below are events that would match an Unguarded Callback signature, but we could just as easily have used functions here instead.

	{{ bp_img_dir('Traversal Callbacks Unguarded') }}

For now, let's say we just want to print the name of each file or directory. We'll start by defining our callback:

=== "C++"
    ```c++ 
	auto PrintItemLeaf = [](FCakePath ItemPath, bool bIsDir) -> void
	{
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
    ```
=== "Blueprint"
	{{ bp_img_dir('Traversal Example Unguarded Callback Definition') }}


We're now ready to launch our traversal, choosing the desired traversal depth when we call the appropriate traversal function:

=== "C++"

    ```c++ hl_lines="17"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };

	auto PrintItemLeaf = [](FCakePath ItemPath, bool bIsDir) -> void
	{
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

	if (!DirectoryGame.TraverseItems(ECakePolicyOpDepth::Shallow, PrintItemLeaf))
	{
		UE_LOG(LogTemp, Error, TEXT("Unguarded item traveral failed to launch!"))
	}

    ```
    
=== "Blueprint"
	{{ bp_img_dir('Traversal Example Unguarded Launch') }}

#### Guarded Traversals
Guarded Traversals are just like unguarded traversals, except the callers can terminate the traversal early if an error is encountered. Outside of this difference, the traversal's effect remains the same -- its goal is to visit all elements at the specified depth. Because the caller has gained some control over the traversal operation, we now must return an [ECakeSignalGuarded](special-types/signals.md#ecakesignalguarded) signal type to indicate if the traversal is allowed to proceed.

=== "C++"
    The callback signatures for Guarded Traversals are described via the following `TFunction` template aliases:

    ```c++ 
	/** Callback signature for a guarded item traversal. */
	using FGuardedCbItem   = TFunction< ECakeSignalGuarded(FCakePath Path, bool bIsDir) >;

	/** Callback signature for a guarded file traversal. */
	using FGuardedCbFile   = TFunction< ECakeSignalGuarded(FCakeFile File) >;

	/** Callback signature for a guarded subdirectory traversal. */
	using FGuardedCbSubdir = TFunction< ECakeSignalGuarded(FCakeDir Subdir) >;
    ```

=== "Blueprint"
    Starting with Guarded Traversals, our callbacks need to return signals that will control how the traversal operation will proceed after each step. Since we need to return values back to the traversal operation via our callback, we now can only use functions. Outside of that, the only thing that changes is the return type, all signatures remain exactly the same as with the Unguarded callbacks.

	{{ bp_img_dir('Traversal Callback Sig Guarded Items') }}

	{{ bp_img_dir('Traversal Callback Sig Guarded Files') }}

	{{ bp_img_dir('Traversal Callback Sig Guarded Subdirs') }}

For this example, we'll use a guarded traversal over files to query the file size of each file, and abort the traversal if any of the query operations fail. 

=== "C++"

    ```c++ 
	auto QueryFileSizeGuarded = [](FCakeFile File) -> ECakeSignalGuarded
	{
		if (TCakeOrderFile<int64> FileSizeOrder = File.QueryFileSizeInBytes())
		{
			UE_LOG(LogTemp, Warning, TEXT("[%s] ([%d] bytes)"), *File.CloneFileName(), *FileSizeOrder);
			return ECakeSignalGuarded::Continue;
		}

		return ECakeSignalGuarded::Abort;
	};
    ```
=== "Blueprint"
	{{ bp_img_dir('Traversal Example Guarded Callback Definition') }}

Using [ECakeSignalGuarded](special-types/signals.md#ecakesignalguarded) is simple, we return the `Continue` signal when no errors are encountered which will advance the traversal to the next element, or we return the `Abort` signal when an error is encountered, which will stop the traversal at this step.

We're now ready to launch our traversal, choosing the desired traversal depth when we call the appropriate traversal function:

=== "C++"

    ```c++ hl_lines="14"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };

	auto QueryFileSizeGuarded = [](FCakeFile File) -> ECakeSignalGuarded
	{
		if (TCakeOrderFile<int64> FileSizeOrder = File.QueryFileSizeInBytes())
		{
			UE_LOG(LogTemp, Warning, TEXT("[%s] ([%d] bytes)"), *File.CloneFileName(), *FileSizeOrder);
			return ECakeSignalGuarded::Continue;
		}

		return ECakeSignalGuarded::Abort;
	};

	if (!DirectoryGame.TraverseGuardedFiles(ECakePolicyOpDepth::Shallow, QueryFileSizeGuarded))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed to check all file sizes!"))
	}
    ```
    
=== "Blueprint"
	{{ bp_img_dir('Traversal Example Guarded Launch') }}

--8<-- "ad-error-handling-traversal.md"
#### Search Traversals
Search Traversals are an advanced traversal operation that allow callers to terminate a traversal as soon as they have accomplished a particular goal. They allow the traversal operation to be terminated early in either an error state or a success state, allowing for optimized performance in situations where an entire directory doesn't necessarily need to be traversed. A search traversal operation's goal is to satisfy the caller's search goal and then immediately terminate the traversal. 

A search traversal can end in three states: 

1. Failure: All target elements were visited at the specified depth and the search goal was not met.
2. Success: The search goal was met.
3. Aborted: The search traversal was terminated due to an error.

Search traversal callbacks return [ECakeSignalSearch](special-types/signals.md#ecakesignalguarded) signals in order to inform the traversal operation of the search's state at each step of the traversal.

=== "C++"
    The callback signatures for search traversals are described via the following `TFunction` template aliases:

    ```c++ 
	/** Callback signature for a search item traversal. */
	using FSearchCbItem    = TFunction< ECakeSignalSearch(FCakePath Path, bool bIsDir)  >;

	/** Callback signature for a search file traversal. */
	using FSearchCbFile    = TFunction< ECakeSignalSearch(FCakeFile File)  >;

	/** Callback signature for a search subdirectory traversal. */
	using FSearchCbSubdir  = TFunction< ECakeSignalSearch(FCakeDir Subdir) >;
    ```

=== "Blueprint"
    Similar to Guarded Traversals, we need to return a signal to the traversal operation. This means we can only change functions. All that changes is the signal type we need to return -- an ECakeSignalSearch, which will inform the traversal operation of the search's context. 

	{{ bp_img_dir('Traversal Callback Sig Search Items') }}

	{{ bp_img_dir('Traversal Callback Sig Search Files') }}

	{{ bp_img_dir('Traversal Callback Sig Search Subdirs') }}



For this example, we'll use a search traversal to attempt to find a subdirectory named "config" contained somewhere within our source directory.

=== "C++"

    ```c++ 
	FCakeDir ConfigDir{};
	FString ConfigName{ TEXT("config") };

	auto ConfigDirSearch = [&ConfigDir, &ConfigName](FCakeDir Subdir) -> ECakeSignalSearch
	{
		if (Subdir.CloneDirName().Equals(ConfigName, ESearchCase::IgnoreCase))
		{
			ConfigDir = MoveTemp(Subdir);
			return ECakeSignalSearch::Success;
		}

		return ECakeSignalSearch::Continue;
	};
    ```
=== "Blueprint"
	{{ bp_img_dir('Traversal Example Search Callback Definition') }}

When using [ECakeSignalSearch](special-types/signals.md#ecakesignalguarded), we return `Success` when the search is satisfied and the traversal should end. In our case, this is when the subdirectory name matches "config". Otherwise, we return `Continue`, which means the search is not yet satisfied and the next element should be visited.

!!! note
    We can also return an `Abort` signal, just like we can in a guarded traversal. However, it is not required -- we don't have any IO failure or other errors that could occur within our callback, and so we can safely leave that out.

We're now ready to launch our traversal, choosing the desired traversal depth when we call the appropriate search traversal function:

=== "C++"

    ```c++ hl_lines="17"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")} };

	FCakeDir ConfigDir{};
	FString ConfigName{ TEXT("config") };

	auto ConfigDirSearch = [&ConfigDir, &ConfigName](FCakeDir Subdir) -> ECakeSignalSearch
	{
		if (Subdir.CloneDirName().Equals(ConfigName, ESearchCase::IgnoreCase))
		{
			ConfigDir = MoveTemp(Subdir);
			return ECakeSignalSearch::Success;
		}

		return ECakeSignalSearch::Continue;
	};

	if (DirectoryGame.TraverseSearchSubdirs(ECakePolicyOpDepth::Deep, ConfigDirSearch))
	{
		UE_LOG(LogTemp, Warning, TEXT("Found config at path: [%s]"), *ConfigDir.GetPathString())
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("No config directory was found!"))
	}

    ```
    The result from a search traversal will only return true if the search was successful, so we can branch on the result and safely use `ConfigDir` when it returns true. This is the most basic way to use the results from a search traversal, please see [traversal error handling](error-handling.md#traversal-error-handling) for a more detailed look at how to work with search traversal results.
=== "Blueprint"
	{{ bp_img_dir('Traversal Example Search Launch') }}

#### Filtered Traversals
Filtered traversals are a special kind of traversal that only works with files and uses the CakeDir object's file extension filter to select which files to visit. A filtered traversal works with file traversals of any style. Every style has a files function that has the suffix `WithFilter`:

1. `TraverseFilesWithFilter`
1. `TraverseGuardedFilesWithFilter`
1. `TraverseSearchFilesWithFilter`

These functions behave exactly like their non-filtered counterparts, however, they take one extra (optional) [FCakeSettingsExtFilter](special-types/settings.md#fcakesettingsextfilter) settings struct. These settings control how the filter should be used to select which files to visit. 

Unless you have changed the [default policy values](policies.md#default-policy-values) manually, the default behavior of the extension filter is to select any files whose file extensions are in the extension filter set.

Let's start with a basic example: we'll use the filter to visit only `.txt` files in a directory and read the text data. Since we're using a file IO operation during each traversal step, we should use a guarded traversal so we can respond to errors.

=== "C++"

    ```c++ hl_lines="13-14"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("txt") };

	auto ReadTextFiles = [](FCakeFile File) -> ECakeSignalGuarded
	{
		if (TCakeOrderFile<FString> ReadOrder = File.ReadTextFile())
		{
			UE_LOG(LogTemp, Warning, TEXT("[%s]: [%s]"), *File.CloneFileName(), **ReadOrder);
			return ECakeSignalGuarded::Continue;
		}
		return ECakeSignalGuarded::Abort;
	};

	if (!DirectoryGame.TraverseGuardedFilesWithFilter(
		ECakePolicyOpDepth::Deep, ReadTextFiles))
	{
		UE_LOG(LogTemp, Error, TEXT("An error occurred while reading the text files."));
	}
    ```

=== "Blueprint"
	{{ bp_img_dir('Traversal Example Filtered Read Text Callback Definition') }}

	{{ bp_img_dir('Traversal Example Filtered Read Text Launch') }}

We can change the filter behavior by submitting our own [FCakeSettingsExtFilter](special-types/settings.md#fcakesettingsextfilter) argument. In this next example, we'll invert the filter logic so that our traversal skips any files whose extensions are in the extension set. For this example, we'll collect all files from a target build directory, ignoring any build artifacts that we don't care about. Since we want all files in the directory and we are just going to be adding CakeFile objects to an array within the callback, we don't need any error handling, so we can just use a unguarded traversal. Note how simple our callback implementation is -- since the filter is being used to exclude build artifacts, we know that any files that we receive are files we are interested in using, so all we need to do is just add each file to the array.

=== "C++"

    ```c++ hl_lines="10-14"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game/build/win64")}, TEXTVIEW("bin|obj|rsp|pdb") };
	
	TArray<FCakeFile> FilesOfInterest{};

	auto GatherFiles = [&FilesOfInterest](FCakeFile File) -> void
	{
		FilesOfInterest.Emplace(MoveTemp(File));
	};

	if (!DirectoryGame.TraverseFilesWithFilter(
		ECakePolicyOpDepth::Deep, 
		GatherFiles,
		{ .FilterMode=ECakePolicyExtFilterMode::ExcludeMatching }
	))
	{
		UE_LOG(LogTemp, Error, TEXT("An error occurred while reading the text files."));
	}
	else
	{
		for (const FCakeFile& File : FilesOfInterest)
		{
			UE_LOG(LogTemp, Warning, TEXT("Doing work with file: [%s]"), *File.CloneFileName())
			// ... do some work
		}
	}

    ```
=== "Blueprint"
	{{ bp_img_dir('Traversal Example Filtered Collect Files') }}

## Advanced Usage

### Checking if a Directory Contains Elements
Sometimes we want to know whether or not a directory contains any of a specific element. We can use the `ContainsAny` family of functions, which return a `bool` indicating whether or not the CakeDir object contains at least one of the desired element. We can check for items, files, files with filter, or subdirectories.

=== "C++"

    ```c++ 
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game")}, TEXTVIEW("txt") };

	const bool bHasAnyItems    { DirectoryGame.ContainsAnyItems()           };
	const bool bHasAnyFiles    { DirectoryGame.ContainsAnyFiles()           };
	const bool bHasAnyTextFiles{ DirectoryGame.ContainsAnyFilesWithFilter() };
	const bool bHasAnySubdirs  { DirectoryGame.ContainsAnySubdirs()         };
    ```

=== "Blueprint"
	{{ bp_img_dir('Contains Any Items') }}

	{{ bp_img_dir('Contains Any Files') }}

	{{ bp_img_dir('Contains Any Files With Filter') }}

	{{ bp_img_dir('Contains Any Subdirs') }}

### Advanced CakeDir Clone Functions
#### CloneWithNewPath
This function is meant to be used when we want to copy the extension filter of a preexisting CakeDir object but use a different directory path. We merely need to submit the CakePath object that represents the new path the cloned object should have, and the extension filter will be copied for us.


=== "C++"
    ```c++ hl_lines="4"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game/build/win64")}, TEXTVIEW("txt") };
	FCakePath NewGameDir{ TEXTVIEW("Y:/game/cake-arena/win64") };

	FCakeDir CakeArenaDir{ DirectoryGame.CloneWithNewPath(NewGameDir) };
	// Path: "Y:/game/cake-arena/win64"
	// Ext Filter: [".txt"]
    ```

=== "Blueprint"
	{{ bp_img_dir('Clone With New Path') }}

The returned CakeDir object will hold the new path `Y:/game/cake-arena/win64`, but its extension filter will contain one extension `.txt`, just like the source directory.


#### CloneWithNewParent
Sometimes we might want to clone a CakeDir object and just change its parent path. `CloneWithNewParent` allows us to submit a new [CakePath](paths.md) object that represents the parent, and it will return a CakeDir that has the new parent, but maintains the same directory name as the source CakeDir object. We can control whether the source CakeDir's extension filter should be copied as well via an [ExtFilterClone](special-types/policies.md#extfilterclone) policy argument, which by default will copy the extension filter.

=== "C++"

    ```c++ hl_lines="5 10"
	FCakeDir DirectoryGame{ FCakePath{TEXTVIEW("X:/game/build/win64")}, TEXTVIEW("txt") };

	FCakePath OtherParent{ TEXTVIEW("Y:/archive/build") };

	FCakeDir OtherGameDir{ DirectoryGame.CloneWithNewParent(OtherParent) };
	// Path: "Y:/archive/build/win64
	// Ext Filter: [".txt"]

	FCakeDir OtherGameDirNoFilter{ 
		DirectoryGame.CloneWithNewParent(OtherParent, ECakePolicyExtFilterClone::DoNotCloneFilter) 
	};
	// Path: "Y:/archive/build/win64
	// Ext Filter: []
    ```

    As the example above shows, in C++ the [ExtFilterClone](special-types/policies.md#extfilterclone) policy parameter is optional. The default value is set to clone the filter.

=== "Blueprint"
	{{ bp_img_dir('Clone With New Parent') }}

The cloned directory will hold the path: `Y:/archive/build/win64`.

### Path Utility Functions
#### BuildPathUnder
This convenience function is designed to provide an ergonomic interface for generating paths relative to (under) a specific CakeDir object's path. All we need to do is submit a [CakePath](paths.md) object that represents the desired child path, and `BuildPathUnder` will return a new CakePath object with that child path parented under the target CakeDir object's path:

=== "C++"
    ```c++ hl_lines="4"
	FCakeDir ProjectDir{ FCakePath{TEXTVIEW("X:/cake-arena")} };
	FCakePath AssetsFolder{ TEXTVIEW("data/assets") };

	FCakePath AssetsFullPath{ ProjectDir.BuildPathUnder(AssetsFolder) };
	// Path: "X:/cake-arena/data/assets"
    ```

=== "Blueprint"
	{{ bp_img_dir('Build Path Under') }}

In the example above, the returned CakePath object's path will be `X:/cake-arena/data/assets`.
