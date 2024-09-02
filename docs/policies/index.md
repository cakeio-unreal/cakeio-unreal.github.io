---
title: Policies
nav_order: 9
---

{% assign in_source="CakePolicies" %}
{% include components/source_info.html %}

## CakeIO Policies
{: .no_toc .text-delta }
1. TOC
{:toc}

## Introduction
CakeIO has various policies that allow users to customize various behaviors across the API. These policies are represented by UENUM types and they are the same in both Blueprint and Native code. This will give a brief overview and explanation of the common policies and some of their settings. As always, for an exhaustive view, please see the documented source code.

{% assign in_policy="OpDepth" %}
{% include components/cake_policy_header.md %}
A very commonly used policy, this is used to determine at what depth a directory operation is applied. 
**Shallow** means that the operation will only be applied to local items, or items that are directly contained within the target directory (and not within a subdirectory).
**Deep** means that the operation will be applied across all items found within the target directory, with subdirectories being visited recursively. 

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
Looking at the example directory tree above and using Game as our source directory, a shallow items iteration will visit `read_me.md` and `Data`. 

```cpp
auto OpDepthPolicy = ECakePolicyOpDepth::Deep;
```
A deep items iteration will visit `read_me.md`, `Data`, `map-1.lv`, `map-2.lv`, `Tables`, and `items.db`.
	

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
