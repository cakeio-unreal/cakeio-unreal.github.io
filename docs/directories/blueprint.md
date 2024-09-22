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

### Sequential Iterations Usage
{% include common_bp_itr_errors.md %}

Let's first examine the callback signatures for all three directory element types, starting with items.
{% assign bp_file_id="callback-seq-item" %}
{% include components/blueprint_image.md %}

When we iterate through items, the callback will be sent a **UCakePath** that contains the current item's path, and a boolean that indicates if the item is a directory.

Now let's look at the callback for file iteration: 
{% assign bp_file_id="callback-seq-file" %}
{% include components/blueprint_image.md %}

This one is simple, since we know we are only visiting files, the callback is passed a single argument: a **UCakeFile** containing the file that is currently being visited.

And finally, let's look at the subdir iteration callback:
{% assign bp_file_id="callback-seq-subdir" %}
{% include components/blueprint_image.md %}

Like the callback for files, this one is equally simple: we are handed a **UCakeDir** that contains the subdirectory currently being visited. 


Now that we've seen all callback function forms, let's see how to run our own iteration. We'll start with items. Sequential iteration functions have an easy naming pattern: `Iterate<Element>`, where `<Element>` is the directory element we wish to visit.

{% assign policy_id="OpDepth" %}
Thus, to run a Sequential iteration for items, we would use `IterateItems`. We need to submit two arguments to this function: an iteration depth and the callback function we want to use. The iteration depth is controlled via the {% include link_policy.md %} policy.

{% assign bp_file_id="itr-launch-seq-items" %}
{% include components/blueprint_image.md %}

To iterate over files or subdirectories instead, we need to use either `IterateFiles` or `IterateSubdirs` respectively:
{% assign bp_file_id="itr-launch-seq-files" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="itr-launch-seq-subdirs" %}
{% include components/blueprint_image.md %}

### Guarded Iteration Usage
{% include common_bp_itr_errors.md %}
Guarded iterations work much like Sequential iterations: they are meant to visit all target elements of a given directory. However, they have one key difference: Guarded iterations allow the caller to terminate the iteration early if an error is encountered. 

Let's look at the callback signatures required for **Guarded** iterations, starting with items. The parameter list is unchanged per directory element type, but our callbacks now have to return a signal of type `ECakeDirIterationSignal` that indicates if an iteration should continue.

{% assign bp_file_id="callback-guarded-item" %}
{% include components/blueprint_image.md %}

When we return the **Continue** signal, the iteration will advance to the next element. When we return the **Abort** signal, the iteration will immediately terminate.

Let's look at some examples for the remaining two element types:

{% assign bp_file_id="callback-guarded-file" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="callback-guarded-subdir" %}
{% include components/blueprint_image.md %}

As all of the examples show us, we are free to define anything as an error worth terminating the iteration over. These example "errors" are quite unrealistic for the sake of brevity, but they also make it clear that caller is in complete control over the iteration.

Launching a Guarded iteration is simple, we just need to use the function family `IterateGuarded<Element>`, where `<Element>` refers to the directory element type being visited.

{% assign bp_file_id="itr-launch-guarded-items" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="itr-launch-guarded-files" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="itr-launch-guarded-subdirs" %}
{% include components/blueprint_image.md %}

### Search Iteration Usage
{% include common_bp_itr_errors.md %}
The final iteration style, Search Iteration, is also the most complex. A **Search Iteration** allows the user to set a custom goal and terminate the iteration when the goal has been satisfied or when a halting error has been encountered. The iteration will continue visiting elements until the callback indicates that it should stop. If all items are visited and the callback has not indicated success, the search is considered a failure. 

 Let's start by looking at the items callback signature. Again, we find that the parameter list is the exact same (we get our UCakePath and the boolean indicating if the path is a directory). Our return type is unique, however, as we need our callback to return a signal to inform the iteration about the search's progress.

{% assign bp_file_id="callback-search-item" %}
{% include components/blueprint_image.md %}
In this callback, our goal is to collect a particular number of paths and store them in an array. This target number is saved in the member variable `TargetPathCount`. When we have stored enough paths, we return the **Complete** signal because our goal has been met. While we still need to collect paths, we return the **Continue** signal to advance to the next path.

All search callbacks _must_ at minimum use the **Complete** signal in order to be a valid search (otherwise, the search is doomed). There are real-world scenarios where we might not need a **Continue** signal, such as if we are checking if there are any files in a directory: there we could simply search files and call complete on the first item found (a search will default to failed if no elements are visited). However, most callbacks you encounter will probably use both **Complete** and **Continue** signals. 

We also can send one more signal: **Abort**. This works exactly like the **Abort** from Guarded iterations -- it should be used when an error is encountered that renders the search meaningless. When sent an **Abort** signal, the iteration will immediately halt, and the search result will be **Aborted**. Let's see an example with a file callback that uses all three signals at once:

{% assign bp_file_id="callback-search-file" %}
{% include components/blueprint_image.md %}

In this search, we are looking for a file name that exactly matches `game.cfg`. If the file names do not match, we return **Continue** to move to the next file. Once we find a match, we need to ensure that the file has data in it. If the file has no data, this is an error and we will fail the result. We return **Abort** to cancel the termination. Otherwise, the search has succeeded and we can use the file as necessary. We return **Complete** to indicate that the goal has been met.

Being able to abort a search iteration early has two benefits -- the first is that we don't need to do any unnecessary work. The second benefit is that callers can easily distinguish between a search that failed (all elements were visited but the goal was not met) and a search that was aborted (an error occurred which prevented the search from meeting its goal). In many scenarios, this distinction might not matter, but when it does matter, you'll be glad you can tell the difference!

Finally, let's look at a special "doomed" search as we examine our final callback signature: 
{% assign bp_file_id="callback-search-subdir" %}
{% include components/blueprint_image.md %}

First, we'll quickly note that the parameter list is the same as all other iteration styles. Secondly, let's notice the absence of a **Complete** condition. This is a doomed search -- it will fail every time it launches -- because it will iterate through all items and never receive a **Completed** signal. Always remember to carefully check your callbacks, and make sure that search callbacks always have at least one branch where **Completed** is possible!


We launch a search iteration via the function family `IterateSearch<Element>`, where `<Element>` is the directory element type being visited:

{% assign bp_file_id="itr-launch-search-items" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="itr-launch-search-files" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="itr-launch-search-subdirs" %}
{% include components/blueprint_image.md %}

### Filtered Iteration Usage
{% include common_bp_itr_errors.md %}
Filtered Iteration is a special iteration variant that only applies to file iterations. Filtered Iteration uses **UCakeDir**'s file extension filter to selectively visit files during an iteration. 

Every style of iteration that targets files has a filtered version; the filtered iteration function will share the name of the non-filtered version, but will have the added suffix `WithFilter`. For example, the filtered version of `IterateFiles` is named `IterateFilesWithFilter`.

{: .warning }
A filtered iteration will fail to launch if there are no entries in the source **FCakeDir**'s file extension filter.

All filtered iteration functions take the exact same callback signature as the non-filtered version; however, the filtered iteration function has extra parameters associated with the filter logic.

Let's first look at an example of filtered iteration using a Sequential iteration:
{% assign bp_file_id="itr-launch-seq-filtered" %}
{% include components/blueprint_image.md %}

This function looks a bit different -- we still need to select an iteration depth and provide a callback, but we also have two new policies we can set. These policies control how files are selected:
{% assign policy_id="ExtFilterMode" %}
* {% include link_policy.md %}
{% assign policy_id="ExtMatchMode" %}
* {% include link_policy.md %}

The default setup supports a common need in directory traversal: only visiting files that have specific file extensions. With the default settings, any files that have file extensions that are listed in **UCakeDir**'s file extension filter will be visited. So, in our example, only files that have the extension `.bin` or `.dat` will be visited.

However, this filter logic can be inverted if you want -- we can instead exclude any files whose extensions are in the filter. We can accomplish this by changing the `FilterMode` argument:

{% assign bp_file_id="itr-filtered-exclude" %}
{% include components/blueprint_image.md %}

With the `FilterMode` argument set to `ExcludeMatching`, now our iteration will visit any files whose extensions are NOT `.bin` or `.dat`. 

Finally we can use the `MatchMode` argument to determine how strict we need to be about matching file extensions. If you want to learn all the gritty details about extension matching, please see the policy documentation that was linked a bit earlier. However, the rough explanation for `MatchMode` is that `MultiOrSingle` represents a more permissive matching logic. When a file has multiple extension components, like `.cdr.bin`, the full extension will be checked against the filter as well as the single extension (`.bin` in this case). Since our filter is using `.bin` for one of its extensions, a file with the extension `.cdr.bin` would still match, since the last extension was `.bin`. 

If we decided to change `MatchMode` to `ExactMatch`, that means that only files with exactly the extension `.bin` or `.dat` would be selected:

{% assign bp_file_id="itr-filtered-exact" %}
{% include components/blueprint_image.md %}

And that's all there is to filtered iteration! For the sake of completeness, here are examples of launching filtered versions of Guarded and Search iteration styles. 

{% assign bp_file_id="itr-launch-guarded-filtered" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="itr-launch-search-filtered" %}
{% include components/blueprint_image.md %}