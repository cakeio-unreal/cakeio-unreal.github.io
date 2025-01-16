## Introduction
CakeIO has special policy types that allow users to customize various behaviors across the API. These policies are represented by UENUM types and they are the same in both Blueprint and C++ code. This will give a brief overview and explanation of public policies. Please see the source code if you want to view the complete set of policies.

All Cake Policy enums are defined in the header `CakePolicies.h`:
```c++
#include "CakeIO/CakePolicies.h"
```

## Default Policy Values
Within the `CakePolicies.h` header file, the namespace `CakePolicies` defines default values for each Cake Policy enum. Any function parameter with a default value uses these default values, so if you wish to change the default CakeIO behavior for your project, you only have to change one place in the source code to accomplish this.

!!! note
    The `CakePolicies` namespace also contains some utility functions that can make working with the enums a bit more ergonomic; if you are curious, please browse the source code for more information!

## OpDepth
OpDepth is used to determine the depth an IO operation is applied in relation to the target directory. 

{{ read_csv(csv_policy('OpDepth')) }}

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

```c++
auto OpDepthPolicy = ECakePolicyOpDepth::Shallow;
```
With `Game/` as our source directory, a shallow items traversal will visit `read_me.md` and `Data/`. 

```c++
auto OpDepthPolicy = ECakePolicyOpDepth::Deep;
```
A deep items traversal will visit `read_me.md`, `Data/`, `map-1.lv`, `map-2.lv`, `Tables/`, and `items.db`.

## OverwriteItems	
OverwriteItems is a policy that determines whether an operation can overwrite an item that already exists. An item might refer to either a file or a directory; it will depend on the usage (e.g., if the policy is a parameter in a File operation, it applies to overwriting pre-existing files.)

{{ read_csv(csv_policy('OverwriteItems')) }}

We can indicate that an overwrite is allowed:
```c++
auto OverwritePolicy = ECakePolicyOverwriteItems::OverwriteExistingItems;
```

...or forbidden:
```c++
auto OverwritePolicy = ECakePolicyOverwriteItems::DoNotOverwriteExistingItems;
```

## MissingParents
MissingParents is a policy that determines whether missing parent directories in a destination path should be created during file or directory operations. 

{{ read_csv(csv_policy('MissingParents')) }}

Let's consider a concrete example: 
Assume directory `x/game/data/models` exists, and that we want to create the following file: `x/game/data/models/hero/hero_main.obj`.

Assume the file does not exist, nor does its parent directory `hero`.

In this case, the subdirectory `hero` in `x/game/data/models/hero/` is classified as a missing parent. In order to successfully create `hero_main.obj`, we need to first create the parent directory `hero`. 

```c++
auto MissingParentsPolicy = ECakePolicyMissingParents::CreateMissing;
```
If we attempted to create `hero_main.obj` and we set the MissingParentsPolicy to `CreateMissing`, the final result would create both the subdirectory `hero` and the file `hero_main.obj`. 

```c++
auto MissingParentsPolicy = ECakePolicyMissingParents::DoNotCreateMissing;
```
If we set the MissingParents policy to `DoNotCreateMissing`, the entire operation will fail. 

## ExtFilterMode
ExtFilterMode determines how a Cake Directory object will utilize its file extension filter to select files to visit during a traversal operation.

{{ read_csv(csv_policy('ExtFilterMode')) }}

```c++
auto FilterMode = ECakePolicyExtFilterMode::SelectMatchingOnly;
```
**SelectMatchingOnly** means that only files with extensions that are contained in the extension filter will be visited.

```c++
auto FilterMode = ECakePolicyExtFilterMode::ExcludeMatching;
```
**ExcludeMatching** means that only files whose extensions are NOT contained in the extension filter will be visited.

## ExtMatchMode
ExtMatchMode determines how a Cake Directory object examines file extensions when selecting files during a filtered file iteration.

{{ read_csv(csv_policy('ExtMatchMode')) }}


--8<-- "ad-file-extension-classification.md"

```c++
auto MatchMode = ECakePolicyExtMatchMode::Exact;
```
In `Exact` mode, a file's extension is compared against every entry in the extension set and a match occurs only if the extension is exactly equal to an entry. 

```
Example: Exact (Failure)
    File Extension Set: [".json", ".cdr.txt", ".jpg"]
    File Extension: ".txt"
```
In the example above, `.txt` will fail to match because no entry in the set is exactly `".txt"`.

```
Example: Exact (Success)
    File Extension Set: [".json", ".cdr.txt", ".txt"]
    File Extension: ".txt"
```
In the example above, `".txt"` will match since `".txt"` is an entry in the set.

```c++
auto MatchMode = ECakePolicyExtMatchMode::Relaxed;
```

In `Relaxed` mode, a file's extension is compared in two passes:

1.  If the file's extension is a multi extension, the multi extension is compared against the set. If the multi extension is found in the extension set, the file is selected.
1.  Otherwise the the file's single extension is compared against the set. If the single extension matches an entry in the set, the file is selected.

```
Example: Relaxed (Failure)
File Extension Set: [".json", ".txt.dat", ".txt.bin"]
File Extension: ".bin.txt"
```
In the example above, step 1 will fail to match, because `".bin.txt"` is not in the extension set.
On step 2, `".bin.txt"` will be converted into its single form: `".txt"`. `.txt.` will fail to match since it does not exist in the set.

```
Example: Relaxed (Success)
File Extension Set: [".json", ".txt"]
File Extension: ".bin.txt"
```
In the example above, step 1 will fail to match, because `".bin.txt"` is not in the extension set.
On step 2, `".bin.txt"` will be converted into its single form: `".txt"`. `.txt.` will match since it is in the extension set and the file will be selected.

## DeleteFile
`DeleteFile` determines whether a file delete operation is allowed to delete a file marked as read-only.

{{ read_csv(csv_policy('DeleteFile')) }}

```c++
auto DeletePolicy = ECakePolicyDeleteFile::UnlessReadOnly;
```
With **UnlessReadOnly**, a delete operation is not authorized to delete a read-only file.

```c++
auto DeletePolicy = ECakePolicyDeleteFile::EvenIfReadOnly;
```
With **EvenIfReadOnly**, a delete operation is authorized to delete a read-only file.


## ExtFilterClone
When cloning Cake Directory objects, this policy lets a user control whether or not the extension filter is also cloned. 

{{ read_csv(csv_policy('ExtFilterClone')) }}

```
Source Directory Object
    Path: "x/game/data"
    File Extension Filter: [".json", ".bin"] 
```

```c++
auto FilterClonePolicy = ECakePolicyExtFilterClone::CloneFilter;
```
When CloneFilter is selected, the elements in the File Extension Filter will also be copied.

```
Cloned Directory Object (CloneFilter):
    Path: "x/game/data"
    File Extension Filter: [".json", ".bin"] 
```

```c++
auto FilterClonePolicy = ECakePolicyExtFilterClone::DoNotCloneFilter;
```
When DoNotCloneFilter is selected, the copied object will have an empty extension filter.
```
Cloned Directory Object (DoNotCloneFilter)
    Path: "x/game/data"
    File Extension Filter: [] 
```
## Text Encoding
Determines how text data should be encoding when writing FStrings to files.

{{ read_csv(csv_policy('TextEncoding')) }}