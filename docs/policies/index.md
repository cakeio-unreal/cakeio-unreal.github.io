---
title: Policies
nav_order: 9
---

{% assign in_source="CakePolicies" %}
{% include components/source_info.html %}

## CakeIO Policies
{% include components/default_toc.md %}

## Introduction
CakeIO has special policy types that allow users to customize various behaviors across the API. These policies are represented by UENUM types and they are the same in both Blueprint and Native code. This will give a brief overview and explanation of public policies. Please see the source code if you want to view the complete set of policies.

{% assign in_policy="OpDepth" %}
{% include components/cake_policy_header.md %}
OpDepth is used to determine the depth a directory operation is applied. 

> **Shallow** means that the operation will only be applied to the source directory, excluding children of subdirectories.

> **Deep** means that the operation will be applied across the source directory and all children of subdirectories. 

Let's take a look at an example.
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

```cpp
auto OpDepthPolicy = ECakePolicyOpDepth::Shallow;
```
With `Game/` as our source directory, a shallow {% glossary iteration_items, display: items iteration %} will visit `read_me.md` and `Data/`. 

```cpp
auto OpDepthPolicy = ECakePolicyOpDepth::Deep;
```
A deep {% glossary iteration_items, display: items iteration %} will visit `read_me.md`, `Data/`, `map-1.lv`, `map-2.lv`, `Tables/`, and `items.db`.
	

{% assign in_policy="OverwriteItems" %}
{% include components/cake_policy_header.md %}
OverwriteItems is a policy that determines whether an operation can overwrite an item that already exists. An item might refer to either a file or a subdirectory; it will depend on the usage (e.g., if the policy is a parameter in a File operation, it applies to overwriting pre-existing files.)

We can indicate that an overwrite is allowed:
```cpp
auto OverwritePolicy = ECakePolicyOverwriteItems::OverwriteExistingItems;
```

...or forbidden:
```cpp
auto OverwritePolicy = ECakePolicyOverwriteItems::DoNotOverwriteExistingItems;
```


{% assign in_policy="MissingParents" %}
{% include components/cake_policy_header.md %}
MissingParents is a policy that determines whether missing parent directories in a destination path should be created during file or directory operations. 

Let's give a concrete example: 
Let's pretend directory `x/game/data/models` exists.
The file `x/game/data/models/hero/hero_main.obj` does not exist, nor does its parent directory `hero`.
In this case, the subdirectory `hero` in `x/game/data/models/hero/` is classified as a missing parent. 
The MissingParents policy will be used to decide whether or not various operations are allowed to create any missing parents in addition to their target file or subdirectory. 

```cpp
auto MissingParentsPolicy = ECakePolicyMissingParents::CreateMissing;
```
If we attempted to create `hero_main.obj` and we set the MissingParentsPolicy to `CreateMissing`, the final result would create both the subdirectory `hero` and the file `hero_main.obj`. 

```cpp
auto MissingParentsPolicy = ECakePolicyMissingParents::DoNotCreateMissing;
```
If we set the MissingParents policy to `DoNotCreateMissing`, the entire operation will fail. 


{% assign in_policy="ExtFilterMode" %}
{% include components/cake_policy_header.md %}
ExtFilterMode determines how a Cake Directory object will utilize its file extension filter to select files to visit during iteration.

```cpp
auto FilterMode = ECakePolicyExtFilterMode::SelectMatchingOnly;
```
**SelectMatchingOnly** means that only files with extensions that are contained in the extension filter will be visited.

```cpp
auto FilterMode = ECakePolicyExtFilterMode::ExcludeMatching;
```
**ExcludeMatching** means that only files whose extensions are NOT contained in the extension filter will be visited.


{% assign in_policy="ExtMatchMode" %}
{% include components/cake_policy_header.md %}
ExtMatchMode determines how a Cake Directory object examines file extensions when selecting files during a filtered file iteration.

```cpp
auto MatchMode = ECakePolicyExtMatchMode::ExactMatch;
```
In ExactMatch mode, a file's extension is compared against every entry in the extension set and a match occurs only if the extension is exactly equal to an entry. 

```
Example: ExactMatch (Failure)
    File Extension Set: [".json", ".cdr.txt", ".jpg"]
    File Extension: ".txt"
```
In the example above, `.txt` will fail to match because no entry in the set is exactly `".txt"`.

```
Example: ExactMatch (Success)
    File Extension Set: [".json", ".cdr.txt", ".txt"]
    File Extension: ".txt"
```
In the example above, `".txt"` will match since `".txt"` is an entry in the set.

```cpp
auto MatchMode = ECakePolicyExtMatchMode::MultiOrSingle;
```

In **MultiOrSingle** mode, a file's extension is compared in two passes:
1. If the file's extension is a {% glossary ext_multi, display: multi extension %}, the multi extension is compared against the set. If the multi extension is found in the extension set, the file is selected.
2. If the full extension does not match, then the file's {% glossary ext_single, display: single extension %} is examined.

```
Example: MultiOrSingle (Failure)
File Extension Set: [".json", ".txt.dat", ".txt.bin"]
File Extension: ".bin.txt"
```
In the example above, step 1 will fail to match, because `".bin.txt"` is not in the extension set.
On step 2, `".bin.txt"` will be converted into its single form: `".txt"`. `.txt.` will fail to match since it does not exist in the set.

```
Example: MultiOrSingle (Success)
File Extension Set: [".json", ".txt"]
File Extension: ".bin.txt"
```
In the example above, step 1 will fail to match, because `".bin.txt"` is not in the extension set.
On step 2, `".bin.txt"` will be converted into its single form: `".txt"`. `.txt.` will match since it is in the extension set and the file will be selected.


{% assign in_policy="FileDelete" %}
{% include components/cake_policy_header.md %}
FileDelete determines whether a file delete operation is allowed to delete a file marked as read-only.

```cpp
auto DeletePolicy = ECakePolicyFileDelete::UnlessReadOnly;
```
With **UnlessReadOnly**, a delete operation is not authorized to delete a read-only file.

```cpp
auto DeletePolicy = ECakePolicyFileDelete::EvenIfReadOnly;
```
With **EvenIfReadOnly**, a delete operation is authorized to delete a read-only file.


{% assign in_policy="ExtFilterClone" %}
{% include components/cake_policy_header.md %}
When cloning Cake Directory objects, this policy lets a user control whether or not the extension filter is also cloned. 

```
Source Directory Object
    Path: "x/game/data"
    File Extension Filter: [".json", ".bin"] 
```

```cpp
auto FilterClonePolicy = ECakePolicyExtFilterClone::CloneFilter;
```
When CloneFilter is selected, the elements in the File Extension Filter will also be copied.

```
Cloned Directory Object (CloneFilter):
    Path: "x/game/data"
    File Extension Filter: [".json", ".bin"] 
```

```cpp
auto FilterClonePolicy = ECakePolicyExtFilterClone::DoNotCloneFilter;
```
When DoNotCloneFilter is selected, the copied object will have an empty extension filter.
```
Cloned Directory Object (DoNotCloneFilter)
    Path: "x/game/data"
    File Extension Filter: [] 
```

{% assign in_policy="ErrorHandling" %}
{% include components/cake_policy_header.md %}
ErrorHandling is a policy that is used to determine if an operation should proceed if an error is encountered. It allows the user to choose between continuing or aborting the operation when an error occurs.
Currently this is rarely used, but a pragmatic example can be found in CakeMixLibrary functions that involve copying/moving/deleting files in a directory. This policy is critical in determining how a failed copy/move/delete should be handled -- in some scenarios it might be acceptable to just move on to the next file, but in other situations callers might want the entire operation to halt.

We can allow an operation to continue when it encounters an error...
```cpp
auto ErrorHandlingPolicy = ECakePolicyErrorHandling::ContinueOnError;
```

...or we can force an operation to abort when it encounters an error:
```cpp
auto ErrorHandlingPolicy = ECakePolicyErrorHandling::AbortOnError;
```

{% assign in_policy="NameComparison" %}
{% include components/cake_policy_header.md %}
This policy determines how file names are matched against user queries. 

```cpp
auto NameCmp = ECakePolicyNameComparison::ContainedInName;
```
The setting **ContainedInName** means that a file will be selected if the query is contained in its name; e.g., given query `readme` would match against the name `readme_file`.

```cpp
auto NameCmp = ECakePolicyNameComparison::ExactName;
```
The setting **ExactName** means only files whose names match the query exactly will be selected; e.g., given query `readme` would match against the name `readme` but would fail against `readme_file`.
{% include components/policy_only_cakemix.md %}


{% assign in_policy="FileRelativeParents" %}
{% include components/cake_policy_header.md %}
This policy determines how a file's relative parent paths should be treated when moving or copying the file to another directory. 

```
Source Directory Tree 
📁 Game
    📁 Data
        📄 map-1.lv

Destination Directory Tree
📁 Other
```

```cpp
auto RelativePathPolicy = ECakePolicyFileRelativeParents::MaintainRelativeParents;
```
If we are moving `map-1.lv` from `Game` to `Other`, we are attempting to move `Data/map-1.lv` from `Game` to `Other`. With a policy of **MaintainRelativeParents**, `Other` will contain `Data/map-1.lv` after the copy/move:

```
Destination Directory Tree (MaintainRelativeParents)
📁 Other
    📁 Data
        📄 map-1.lv
```

There might be situations where we don't want the subdirectory parents of a file to be preserved (e.g., perhaps we are trying to move all ".cpp" files scattered across multiple subdirectories into a single "src" directory).

```cpp
auto RelativePathPolicy = ECakePolicyFileRelativeParents::FlattenRelativeParents;
```
If we are moving `map-1.lv` from `Game` to `Other`, we are attempting to move `Data/map-1.lv` from `Game` to `Other`. With a policy of **FlattenRelativeParents**, `Other` will contain `map-1.lv` after the copy/move:

```
Destination Directory Tree (FlattenRelativeParents)
📁 Other
    📄 map-1.lv
```
{% include components/policy_only_cakemix.md %}


{% assign in_policy="FileWriteMode" %}
{% include components/cake_policy_header.md %}
FileWriteMode is a policy that determines whether data should replace (overwrite) the source file's previous data or if it should be appended to the source file's previous data.

We can overwrite a file's pre-existing data...
```cpp
auto WriteMode = ECakePolicyFileWriteMode::OverwriteData;
```
...or append to it.
```cpp
auto WriteMode = ECakePolicyFileWriteMode::AppendData;
```