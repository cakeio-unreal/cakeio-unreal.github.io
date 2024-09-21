---
title: Blueprint
parent: Directories
nav_order: 2
---

{% assign in_source="CakeDir_BP" %}
{% include components/source_info_blueprint.html %}

{% assign filter_syntax_link = "[Extension Filter Syntax](#file-extension-filter-syntax)" %}

{% assign bp_path="dir" %}

## UCakeDir
{% include components/default_toc.md %}

## Introduction
The Blueprint directory object in CakeIO is **UCakeDir**. **UCakeDir**'s primary purpose is to provide a comprehensive interface for directory iteration and common IO operations involving directories.

{% include components/src_advert_blueprint.md %}

## Basic Usage

### The File Extension Filter
**UCakeDir** contains a member field called the file extension filter. The file extension filter is used to selectively visit files during file iteration. Many functions throughout **UCakeDir** will involve the file extension filter in some way. 

#### File Extension Filter Syntax
Functions that involve modifying the file extension filter use a special syntax via strings. This allows us to add or remove multiple file extensions within a single filter command. The syntax is very simple: we simply must separate each file extension element via the `|` (pipe) character. 

As an example, if we wanted to modify both `.txt` and `.bin` in the same command, we would use the string `"txt|bin"` for the extension command:

{% assign bp_file_id="filter-example-single" %}
{% include components/blueprint_image.md %}

The order of extensions doesn't matter, and it also doesn't matter if we include the leading `.` character for extensions, because it will be added for us afterward. Thus, all of the following variations will parse into the same file extension list: `[.txt, .bin]`:
```
"txt|bin"
".txt|bin"
".txt|.bin"
"txt|.bin"
```

The leading `.` is also not required for {% glossary ext_multi, display: multi extensions %}:
{% assign bp_file_id="filter-example-multi" %}
{% include components/blueprint_image.md %}

As the example above shows, if we are trying to add `.cdr.txt` to the extension filter, we could do so either with `cdr.txt` or `.cdr.txt`.

{: .hint }
>The extension filter is extremely lenient when parsing file extension lists. It can handle extra symbols and empty entries without incident (it will merely skip them). For example, `|.|..cdr.|txt|bin||` will correctly parse the command into the following extension list `[.cdr, .txt, .bin]`. Therefore, you do not have to do exhaustive syntax checking when accepting filter commands from outside sources (like from a GUI).


### UCakeDir Creation
We can create a **UCakeDir** object via `BuildCakeDir` or `BuildCakeDirViaPath`. In addition to providing the path to the directory, we can also submit a string that contains uses file extension filter syntax to set the starting elements in the **UCakeDir**'s file extension filter:

{% assign bp_file_id="build-cake-dir" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="build-cake-dir-via-path" %}
{% include components/blueprint_image.md %}

{: .note }
These examples use file extension filter syntax; see {{ filter_syntax_link }} for more information.

If we want to create a **UCakeDir** with no initial path data or extension filter, we can use `BuildCakeDirEmpty`:

{% assign bp_file_id="build-cake-dir-empty" %}
{% include components/blueprint_image.md %}


We can get a copy of an existing **UCakeDir** via `Clone`:
{% assign bp_file_id="clone" %}
{% include components/blueprint_image.md %}

{% assign policy_id="ExtFilterClone" %}
By default, this function will also ensure that the cloned **UCakeDir** has an identical file extension filter. If we do not want the cloned **UCakeDir** to inherit the file extension filter, we can change this behavior via the {% include link_policy.md %} policy.

### Directory Path and Name
To get the directory path as a string, we can use `GetPathString`:
{% assign bp_file_id="get-path-string" %}
{% include components/blueprint_image.md %}

{% assign link_desc="UCakePath" %}
To get a {% include rlinks/cakepath_blueprint.md %} copy that contains the directory path, we can use `ClonePath`.
{% assign bp_file_id="clone-path" %}
{% include components/blueprint_image.md %}

{: .note }
This is just a copy of the directory path, no changes made the to returned **UCakePath** will be reflected in the source **UCakeDir**.

To read the directory name as a string, we can use `GetDirName`:
{% assign bp_file_id="get-dir-name" %}
{% include components/blueprint_image.md %}


We can change the path a **UCakeDir** is using via `SetPath` or `SetPathViaPath`.
{% assign bp_file_id="set-path" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="set-path-via-path" %}
{% include components/blueprint_image.md %}

We can check if **UCakeDir**'s directory path is empty via `PathIsEmpty`:
{% assign bp_file_id="path-is-empty" %}
{% include components/blueprint_image.md %}

We can reset the directory path to be empty via `ResetPath`:
{% assign bp_file_id="reset-path" %}
{% include components/blueprint_image.md %}

### Modifying the File Extension Filter
We can change and modify the elements in the file extension filter after we have created **UCakeDir**.

{: .note }
All of the examples in this section use file extension filter syntax; see {{ filter_syntax_link }} for more information.

It is important to understand that the file extension filter only stores unique file extension entries. 

When we want to add extensions to the filter we use `AddExtensionsToFilter`. This function returns the number of extensions successfully added.

{% assign bp_file_id="add-extensions-to-filter" %}
{% include components/blueprint_image.md %}

The number added will be less than the number submitted if any of the submitted extensions already exist in the filter.


{% assign link_desc="UCakeFileExt" %}
We can get an array of {% include rlinks/cakefileext_blueprint.md %} that contains all the file extensions currently in the **UCakeDir**'s file extension set via `CloneExtensionFilter`. 

{% assign bp_file_id="clone-extension-filter" %}
{% include components/blueprint_image.md %}

{: .note }
As the name implies, `CloneExtensionFilter` gives us a copy of all the file extensions currently in the filter. Changing anything in the returned array will not result in any changes being made the the **UCakeDir**'s file extension filter.

We can remove extensions from the filter via `RemoveExtensionsFromFilter`. This function returns the amount of extensions successfully removed from the filter set:
{% assign bp_file_id="remove-extensions-from-filter" %}
{% include components/blueprint_image.md %}

To remove all entries from the extension filter, we can use `ResetExtensionFilter`:
{% assign bp_file_id="reset-extension-filter" %}
{% include components/blueprint_image.md %}

We can use `SetExtensionFilter` to ensure the extension filter only contains entries found in the command string argument:
{% assign bp_file_id="set-extension-filter" %}
{% include components/blueprint_image.md %}

In the example above, the call to `SetExtensionFilter` results in the previous entries `.bin` and `.dat` being removed from the filter and the entries from the command string `.json` and `.txt` are added to the set.

We can check if **UCakeDir**'s extension filter is empty via `ExtensionFilterIsEmpty`:
{% assign bp_file_id="extension-filter-is-empty" %}
{% include components/blueprint_image.md %}

### Resetting All Data
In the situation where we want to reset all data on **UCakeDir**, we can use `Reset`. This will reset both the path and the extension filter for us:

{% assign bp_file_id="reset" %}
{% include components/blueprint_image.md %}

### Directory Equality Comparison
In equality comparisons, we compare the directory path stored by a **UCakeDir** against another path. The paths are equal if they refer to the same location on the filesystem.

We can use `IsEqualToOther` or `IsNotEqualToOther` to compare two **UCakeDir**s against each other:
{% assign bp_file_id="is-equal-to-other" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="is-not-equal-to-other" %}
{% include components/blueprint_image.md %}

We can use `IsEqualToPath` or `IsNotEqualToPath` to compare a **UCakeDir** against a **UCakePath**:
{% assign bp_file_id="is-equal-to-path" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="is-not-equal-to-path" %}
{% include components/blueprint_image.md %}

We can use `IsEqualTo` or `IsNotEqualTo` to compare a **UCakeDir** against a path string:
{% assign bp_file_id="is-equal-to" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="is-not-equal-to" %}
{% include components/blueprint_image.md %}

## IO Operations

{: .note }
This section does not include examples about how to handle errors from directory IO operations. This is to keep the focus entirely on the interfaces offered by **UCakeDir**.
{% assign link_desc="Error Handling" %} See {% include rlinks/error_handling.md %} for a detailed examination of error types and error handling strategies.

### Directory Existence
We can check if the directory represented by **UCakeDir** exists on the file system via `Exists`:

{% assign bp_file_id="exists" %}
{% include components/blueprint_image.md %}

### Creating Directories
We can attempt to create the directory represented by **UCakeDir** via `CreateDir`:
{% assign bp_file_id="create-dir" %}
{% include components/blueprint_image.md %}

{% assign policy_id="MissingParents" %}
By default, `CreateDir` will ensure that any missing parent directories in the directory's path will also be created. You can control this behavior directly via the {% include link_policy.md %} policy.

For situations where we aren't certain a directory exists and would like it created if it doesn't exist, we can use the convenience function `ExistsOrCreate`:

{% assign bp_file_id="exists-or-create" %}
{% include components/blueprint_image.md %}

### Copying Directories
We can copy a directory and its contents to another location via `CopyDir` or `CopyDirViaOther`. The argument we send for `DestDir` should hold the path to the directory we want to copy our directory into.

{% assign bp_file_id="copy-dir" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="copy-dir-via-other" %}
{% include components/blueprint_image.md %}

{% assign policy_id="OverwriteItems" %}
By default, `CopyDir` will overwrite a pre-existing directory if it shares the same location. We can control this via the {% include link_policy.md %} policy.
{% assign policy_id="MissingParents" %}
By default, `CopyDir` will create any missing parents contained in `DestDir`. We can control that via the {% include link_policy.md %} policy.

Sometimes we might want to copy a directory but give the copied directory a different name, and for that we can use `CopyDirAliased` or `CopyDirAliasedViaOther`. In addition to a destination path, we also need to provide a new name that the copied directory should have:

{% assign bp_file_id="copy-dir-aliased" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="copy-dir-aliased-via-other" %}
{% include components/blueprint_image.md %}

In the examples above, assuming the copy operations succeed, the copied directory's path will be `/y/archive/game_archive`.

{: .note }
`CopyDirAliased` and `CopyDirAliasedViaOther` share the same policy parameters and policy defaults as `CopyDir` and `CopyDirViaOther`.

### Moving Directories
We can move a directory and its contents to another location via `MoveDir` or `MoveDirViaOther`. The argument we send for `DestDir` should hold the path to the directory we want to move our directory into.

{% assign bp_file_id="move-dir" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="move-dir-via-other" %}
{% include components/blueprint_image.md %}

{% assign policy_id="OverwriteItems" %}
By default, `MoveDir` / `MoveDirViaOther` will overwrite a pre-existing directory if it shares the same location. We can control this via the {% include link_policy.md %} policy.
{% assign policy_id="MissingParents" %}
By default, `MoveDir` / `MoveDirViaOther` will create any missing parents contained in `DestDir`. We can control that via the {% include link_policy.md %} policy.

Sometimes we might want to move a directory but give the copied directory a different name, and for that we can use `MoveDirAliased` or `MoveDirAliasedViaOther`. In addition to a destination path, we also need to provide a new name that the copied directory should have:

{% assign bp_file_id="move-dir-aliased" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="move-dir-aliased-via-other" %}
{% include components/blueprint_image.md %}

In the examples above, assuming the move operations succeed, the moved directory's path will be `/y/archive/game_archive`.

{: .note }
`MoveDirAliased` and `MoveDirAliasedViaOther` share the same policy parameters and policy defaults as `MoveDir` and `MoveDirViaOther`.

We can also change just the name of a directory via `RenameDir`. 
{% assign bp_file_id="rename-dir" %}
{% include components/blueprint_image.md %}

{% assign policy_id="OverwriteItems" %}
By default, `RenameDir` will overwrite an existing directory if it shares the same name as the new name. We can control that behavior directly via the {% include link_policy.md %} policy.

{: .note }
Whenever a move / rename succeeds, the **UCakeDir** will automatically update all of its path information to reflect its new path information.

### Deleting Directories
We can delete the directory and all of its contents via `DeleteDir`:
{% assign bp_file_id="delete-dir" %}
{% include components/blueprint_image.md %}

### Retrieving Directory OS Information
We can get a `UCakeFileStatData` which contains various system information about the source directory via `GetStatData`:

{% assign bp_file_id="get-stat-data" %}
{% include components/blueprint_image.md %}

{: .warning }
`UCakeFileStatData` is used for both files and directories; as such, some fields (such as file size) will not apply to a directory.

{: .note }
`UCakeFileStatData` is merely a struct that wraps Unreal's own `FFileStatData`, which is not exposed to Blueprints.

{% include common_cakedir_iteration.md %}

### Iteration Callbacks
{% assign policy_id="OpDepth" %}
All iteration processes offered by **UCakeDir** will require at least two arguments: An {% include link_policy.md %} that determines the iteration depth and a callback that will be invoked each time an item is visited. This callback's signature will changed based upon two factors: the target directory element type will determine the callback's parameter list (e.g., a file iteration will pass one **UCakeFile** object per file visited) and the iteration style will determine the callback's return type (e.g., a search iteration style returns an `ECakeDirSearchSignal`.). The following sections will go into more specific details about using iterations. 

However, creating an appropriate iteration callback is extremely easy in Blueprint. 
1. Call the iteration function you want from a **UCakeDir** object.
2. Click and drag off the `ItrOp` function parameter.
3. From the Blueprint context menu, select `Create Event`.
4. Select either Matching Function or Matching Event depending on your needs.

Below is an example using IterateItems, but this will work for any callback and any iteration function:
{% assign bp_file_id="spawn-iteration" %}
{% include components/blueprint_anim.md %}

{: .note }
Because both Guarded and Search iteration callbacks need to return values, you cannot use a Blueprint event and instead must use a Blueprint function.

### Sequential Iteration

Let's first examine the callback signatures for all three element types:
```cpp
	// Standard Iteration (Items)
	auto ItemsStandardIteration = [](FCakePath ItemPath, bool bIsDir) -> void
	{
		// Any iteration callback for Items will be sent an FCakePath representing 
		// the current element visited, and a boolean to indicate whether that path 
		// is a directory.
		FString Leaf = ItemPath.CloneLeafAsString();
		if (bIsDir)
		{
			UE_LOG(LogTemp, Warning, TEXT("Visited directory: [%s]"), *Leaf);
		}
		else
		{
			UE_LOG(LogTemp, Warning, TEXT("Visited file: [%s]"), *Leaf);
		}
	};

	// Standard Iteration (Files)
	auto FilesStandardIteration = [](FCakeFile File) -> void
	{
		// Any iteration callback for files will be sent an FCakeFile 
		// representing the current file being visited.
		UE_LOG(LogTemp, Warning, TEXT("Visited file: [%s]"), *File.GetFileName());
	};

	// Standard Iteration (Subdirs)
	auto SubdirStandardIteration = [](UCakeDir Subdir) -> void
	{
		// Any iteration callback for subdirectories will be sent 
		// an UCakeDir representing the current subdirectory being visited.
		UE_LOG(LogTemp, Warning, TEXT("Visited subdirectory: [%s]"), *Subdir.GetDirName());
	};

```

We should emphasize two things: the input parameters changed based on the directory element type we are visiting, and callbacks return `void`. This is because standard iteration offers no way for a caller to terminate the iteration early; the iteration will visit all target elements at the specified depth.

With our callbacks defined, we must decide upon a depth that the iteration should traverse. We control iteration depth via the policy {% include link_policy.md %}:
```cpp
auto DesiredDepth = ECakePolicyOpDepth::Shallow;
```

Now our callbacks are ready and we have decided upon a depth. We are ready to execute an iteration on our directory. The standard iteration function names take the form `Iterate<Type>`, where `<Type>` is the element type we are visiting. For arguments, we only need pass the depth followed by the appropriate callback:


```cpp
if (!IntDir.IterateItems(DesiredDepth, ItemsStandardIteration))
{
    UE_LOG(LogTemp, Warning, TEXT("IterateItems failed to launch!"));
}

if (!IntDir.IterateFiles(DesiredDepth, FilesStandardIteration))
{
    UE_LOG(LogTemp, Warning, TEXT("IterateFiles failed to launch!"));
}

if (!IntDir.IterateSubdirs(DesiredDepth, SubdirStandardIteration))
{
    UE_LOG(LogTemp, Warning, TEXT("IterateSubdirs failed to launch!"));
}
```
A standard iteration will return an `UCakeDirIterationResult` indicating the outcome of the iteration. We can use it as a boolean via `operator bool` as shown in the preceding examples, or we can store the result and handle the outcomes explicitly:

```cpp
ItrStandardResult = IntDir.IterateSubdirs(DesiredDepth, SubdirStandardIteration);

switch (ItrStandardResult.Outcome)
{
    case ECakeDirIterationOutcome::DIO_Completed:
        UE_LOG(LogTemp, Warning, TEXT("IterateSubdirs completed without incident!"));
        break;

    case ECakeDirIterationOutcome::DIO_Aborted:
        UE_LOG(LogTemp, Warning, TEXT("IterateSubdirs failed to launch!"));
        break;
}
```
Since callers cannot abort a standard iteration, an outcome of aborted indicates that the iteration itself failed to launch. This could happen due to a variety of reasons, such as the **UCakeDir**'s directory not existing on the file system. Otherwise, if the iteration launches, then it will return a **Completed** outcome.


Even though we declared our callbacks and depth before the iterate operation function call, we could just as easily have submitted our arguments inline:

```cpp
ItrStandardResult = IntDir.IterateSubdirs(
ECakePolicyOpDepth::Deep,
[](UCakeDir Subdir) -> void 
    {
        UE_LOG(LogTemp, Warning, TEXT("Visited subdir: [%s]"), *Subdir.GetDirName());
    }
);
```

### Guarded Iteration
Let's first examine the callback signatures required for abortable standard iterations:

```cpp
	// Abortable Standard Iteration (Items)
	auto ItemsAbortableIteration = [](FCakePath ItemPath, bool bIsDir) -> ECakeDirIterationSignal
	{
		if (!bIsDir)
		{
			// We return abort when we want the iteration to abort early.
			return ECakeDirIterationSignal::DIS_Abort;
		}
		// We return continue whenever we want the iteration to continue 
		// and the next element to be visited.
		return ECakeDirIterationSignal::DIS_Continue;
	};

	// Abortable Standard Iteration (Files)
	auto FilesAbortableIteration = [](FCakeFile File) -> ECakeDirIterationSignal
	{
		// The caller is in complete control as to what is considered 
		// an "error" worth terminating over.
		if (File.GetFileExt() != FString(".jpg"))
		{
			// We return abort when we want the iteration to abort early.
			return ECakeDirIterationSignal::DIS_Abort;
		}
		// We return continue whenever we want the iteration to continue 
		// and the next element to be visited.
		return ECakeDirIterationSignal::DIS_Continue;
	};

	// Abortable Standard Iteration (Subdirs)
	auto SubdirAbortableIteration = [](UCakeDir Subdir) -> ECakeDirIterationSignal
	{
		// The caller is in complete control as to what is considered 
		// an "error" worth terminating over.
		if (Subdir.CloneDirName() != TEXT("SpecialDir"))
		{
			// We return abort when we want the iteration to abort early.
			return ECakeDirIterationSignal::DIS_Abort;
		}
		// We return continue whenever we want the iteration to continue 
		// and the next element to be visited.
		return ECakeDirIterationSignal::DIS_Continue;
	};
```

The only major difference between these callbacks and standard iteration callbacks is the return type. Because the caller can abort an iteration early, we must return a signal that indicates whether the iteration should proceed to the next item. The signal type is `ECakeDirIterationSignal` and it holds only two meaningful values: **Continue** and **Abort**. When we need to terminate an iteration due to an error, we should return `ECakeDirIterationSignal::DIS_Abort`. Otherwise, we should return `ECakeDirIterationSignal::DIS_Continue`.

To launch an abortable standard iteration, we use the function family `Iterate<Type>UnlessError`, where `<Type>` refers to the directory element type being visited.


```cpp
if (!IntDir.IterateItemsUnlessError(DesiredDepth, ItemsAbortableIteration))
{
    UE_LOG(LogTemp, Error, TEXT("IterateItemsUnlessError encountered an error!"));
}

if (!IntDir.IterateFilesUnlessError(DesiredDepth, FilesAbortableIteration))
{
    UE_LOG(LogTemp, Error, TEXT("IterateFilesUnlessError encountered an error!"));
}
```

Just like standard iteration, abortable standard iterations return an `UCakeDirIterationResult` that indicate the outcome of the iteration. In this case, however, the **Aborted** has more potential meaning: either the iteration failed to launch or the caller requested early termination. 
```cpp
UCakeDirIterationResult ItrAbortableResult = IntDir.IterateSubdirsUnlessError(DesiredDepth, SubdirAbortableIteration);
switch (ItrAbortableResult.Outcome)
{
    case ECakeDirIterationOutcome::DIO_Completed:
        UE_LOG(LogTemp, Warning, TEXT("SubdirsUnlessError iteration completed without incident."))
            break;
    case ECakeDirIterationOutcome::DIO_Aborted:
        UE_LOG(LogTemp, Warning, TEXT("SubdirsUnlessError iteration was aborted early!"))
            break;
}
```

### Search Iteration
The final iteration style, Search Iteration, is also the most complex. A **Search Iteration** allows the user to set a custom goal and terminate the iteration when the goal has been satisfied or when a halting error has been encountered. Let's start by looking at the callback signatures:

```cpp
// Search callbacks return ECakeDirSearchSignal to control iteration flow.

// Search Iteration (Items)
auto ItemSearch = [SearchLimit, &ItemCount](FCakePath ItemPath, bool bIsDir) -> ECakeDirSearchSignal
{
    // There are three signal values we can return.
    if (SearchLimit <= 0)
    {
        // If we encounter a situation we consider an error worth aborting the iteration over, we can return the Abort signal.
        UE_LOG(LogTemp, Warning, TEXT("Search limit is set to a value <= 0. Aborting."));
        return ECakeDirSearchSignal::DSS_Abort;
    }

    ++ItemCount;
    // When we have accomplished our goal for this iteration, we return the Complete signal.
    if (ItemCount > SearchLimit) { return ECakeDirSearchSignal::DSS_Complete; }

    // When our requirements have not been met and we want to keep visiting elements, we return the Continue signal.
    return ECakeDirSearchSignal::DSS_Continue;
};

// As with Items, the only changes we need to make to File and Subdir variants involve the return types.

// Search Iteration (Files)
auto FileSearch = [](FCakeFile File) -> ECakeDirSearchSignal
{
    // We can abort if we want to indicate a halting error has occurred.
    return ECakeDirSearchSignal::DSS_Abort;
};

// Search Iteration (Subdirs)
auto SubdirSearch = [](UCakeDir Subdir) -> ECakeDirSearchSignal
{
    // A search iteration that never returns DSS_Complete will result in 
    // a Failed outcome.
    return ECakeDirSearchSignal::DSS_Continue;
};
```

As the code above shows, search iteration callbacks return an `ECakeDirSearchSignal`, which is used to control the iteration flow. During the iteration, when we visit an item and still have not yet completed our goal, we return a **Continue** signal. If we accomplish our goal after the current item is visited, we should instead return **Complete**. If we encounter a halting error during the search, we can also return the **Abort** signal to terminate early.


We launch a search iteration via the function family `IterateSearch<Type>`, where `<Type>` is the directory element type being visited:
```cpp
UCakeDirSearchResult ItrSearchResult = IntDir.IterateSearchItems(DesiredDepth, ItemSearch);
switch (ItrSearchResult.Outcome)
{
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
A search iteration will return an `UCakeDirSearchResult` which holds an outcome. There are three outcomes a search can generate:
1. **Succeeded**: The goal was accomplished during the search iteration.
2. **Failed**: All target elements were visited and the goal was not satisfied.
3. **Aborted**: A halting error was encountered and the iteration was aborted.

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

### Filtered Iteration
Filtered Iteration is a special "meta" iteration style that can be applied to any iteration style, but only to iterations that target files. Filtered Iteration uses **UCakeDir**'s file extension filter to selectively visit files during an iteration.

Every style of iteration that targets files has a filtered version; the filtered iteration function will share the name of the non-filtered version, but will have the added suffix `WithFilter`. For example, the filtered version of `IterateFiles` is named `IterateFilesWithFilter`.

All filtered iteration functions take the exact same callback signature as the non-filtered version; however, the filtered iteration function has extra parameters associated with the filter logic.

Let's look at a brief example using standard iteration:

```cpp
auto StandardFilter = [](FCakeFile InFile) -> void 
{
    UE_LOG(LogTemp, Warning, TEXT("    StandardFilter Found File: [%s]"), *InFile.GetFileName());
};

ECakePolicyOpDepth CurrentDepth = ECakePolicyOpDepth::Shallow;

UCakeDirIterationResult ItrStandardRes = IntDir.IterateFilesWithFilter(CurrentDepth, StandardFilter);
```

{: .warning }
A filtered iteration will fail to launch if there are no entries in the source **UCakeDir**'s file extension filter.

Other than the function name, this doesn't look any different from a call to the non-filtered version. However, filtered iterations use the following two policies to control how files are selected:
{% assign policy_id="ExtFilterMode" %}
* {% include link_policy.md %}
{% assign policy_id="ExtMatchMode" %}
* {% include link_policy.md %}


```cpp
UCakeDirIterationResult IterateFilesWithFilter(
    ECakePolicyOpDepth Depth, 
    FIterateOpFile Callback, 
    ECakePolicyExtFilterMode FilterMode = ECakePolicyExtFilterMode::SelectMatchingOnly, 
    ECakePolicyExtMatchMode   MatchMode = ECakePolicyExtMatchMode::MultiOrSingle
) const;
```

By default, filter iteration functions will use the filter mode of **SelectMatchingOnly** and the match mode of **MultiOrSingle**. This means that we will only visit files whose extensions are found in the extension filter, and that our matching logic will be more permissive. 

{: .note }
For a detailed description of the matching logic for `ECakePolicyExtMatchMode`, please visit the policy documentation linked previously.

We can invert the filter and ignore files whose extensions are found in the extension filter:

```cpp
ItrStandardRes = IntDir.IterateFilesWithFilter(
    CurrentDepth, 
    StandardFilter, 
    ECakePolicyExtFilterMode::ExcludeMatching
);
```

We can also adjust the extension matching logic to be more strict by using the **ExactMatch** match mode policy value:
```cpp
ItrStandardRes = IntDir.IterateFilesWithFilter(
    CurrentDepth, 
    StandardFilter, 
    ECakePolicyExtFilterMode::ExcludeMatching, 
    ECakePolicyExtMatchMode::ExactMatch
);
```

{: .note }
The other filtered functions, `IterateFilesUnlessErrorWithFilter` and `IterateSearchFilesWithFilter` share the policy parameters and default settings.
