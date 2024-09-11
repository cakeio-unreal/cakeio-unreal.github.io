---
title: Blueprint
parent: File Extensions
nav_order: 2
---

{% assign in_source="CakeFileExt_BP" %}
{% include components/source_info_blueprint.html %}

{% assign bp_path="file-ext" %}

## UCakeFile
{% include components/default_toc.md %}

## Introduction
The Blueprint object for dealing with file extensions is **UCakeFileExt**. This object is meant to represent a file extension and ensures that the file extension is represented in a standard, common form. Furthermore, it provides various utilities for working with file extensions.

{% include components/src_advert_blueprint.md %}

## Basic Usage
### Construction
To create an UCakeFileExt, all we need to do is supply an FString of the file extension we want it to store:
```cpp
UCakeFileExt ExtExample{ TEXT(".txt") };
```

{: .note }
UCakeFileExt is very lenient when it comes to file extension input strings; it doesn't matter if you include a leading '.' or not, the final result will be converted into the standard form.


To create a UCakeFileExt by extracting the file extension from a file name, we can use the static function `BuildFileExtFromFileName`.
```cpp
UCakeFileExt ExtFromFile{ UCakeFileExt::BuildFileExtFromFileName(TEXT("example_file.txt")) };
```

{: .warning }
Make sure you are sending input strings that are only file names into `BuildFileExtFromFileName`. While the function can technically extract file extensions from paths, there is a danger of an erroneous extraction since the file extension separator '.' is valid to use in directory names in most major operating systems. 

We can create an **UCakeFileExt** copy of an **UCakeFileExt** via `Clone`:
```cpp
UCakeFileExt ExtA{ TEXT(".txt") };

UCakeFileExt ExtACopy = ExtA.Clone();
```

We can create an **FString** copy of an **UCakeFileExt** via `CloneAsString`:
```cpp
UCakeFileExt ExtA{ TEXT(".txt") };

FString ExtAString = ExtA.CloneAsString();
```

### Reading the file extension
To read the file extension as an **FString**, we can use either `operator*` or `GetExtString`:
```cpp
PrintFileExt( *ExtExample );
PrintFileExt( ExtExample.GetExtString() );
```
### Changing the file extension
We can change the file extension to a different extension via `SetFileExt`, which accepts either an **FString** or another **UCakeFileExt**:

```cpp
UCakeFileExt ExtExample{ TEXT(".txt") };
UCakeFileExt ExtOther{ TEXT("bin.dat") };

ExtExample.SetFileExt( TEXT("bin") );
ExtExample.SetFileExt(ExtOther);
```

We can also extract the extension from a file name and set our extension to the extracted result via `SetFileExtFromFileName`:
```cpp
ExtExample.SetFileExtFromFileName(TEXT("spells.db"));
```

{: .warning }
Only send file names without other path components to `SetFileExtFromFileName` in order to ensure the extraction is correct.


We can check if an **UCakeFileExt** currently has a non-empty file extension via `IsEmpty`:

```cpp
ExtExample.SetFileExt(TEXT(".bin"));
bool bIsEmpty = ExtExample.IsEmpty(); // => false
```
We can clear an **UCakeFileExt**'s file extension via `Reset`:
```cpp
ExtExample.Reset();
bIsEmpty = ExtExample.IsEmpty(); // => true
```
### Combining file extensions
We can build combined extensions with `operator+`:
```cpp
UCakeFileExt ExtA{ TEXT(".txt") };
UCakeFileExt ExtB{ TEXT(".cdr") };

UCakeFileExt ExtCombined = ExtB + ExtA; // => ".cdr.txt"
ExtCombined = ExtA + TEXT("bin"); // => ".txt.bin"
```
We can also use `BuildCombined` instead of `operator+`:
```cpp
UCakeFileExt ExtA{ TEXT(".txt") };
UCakeFileExt ExtB{ TEXT(".cdr") };

UCakeFileExt ExtCombined = ExtB.BuildCombined(ExtA); // => ".cdr.txt"
ExtCombined = ExtA.BuildCombined( TEXT("bin") ); // => ".txt.bin"
```

We can append a file extension onto an UCakeFileExt with either `operator+=` or `CombineInline`:
```cpp
UCakeFileExt ExtA{ TEXT(".txt") };
UCakeFileExt ExtB{ TEXT(".cdr") };

ExtA += ExtB; // => ".txt.cdr"
ExtA.CombineInline( TEXT(".bin.dat") ); // => ".txt.cdr.bin.dat"
```

### Comparing file extensions
We can use equality comparison against **UCakeFileExt** via `operator==` and `operator!=`. We can check equality against other **UCakeFileExt**s and **FString**s.

```cpp
UCakeFileExt ExtA{ TEXT(".txt") };
UCakeFileExt ExtB{ TEXT(".cdr") };

FString StringA{ TEXT(".txt") };

bool bIsEqual = ExtA == ExtB; // => false
bIsEqual = ExtA == StringA; // => true

bool bIsNotEqual = ExtA != ExtB; // => true
bIsNotEqual = ExtA != StringA; // => false
```
## Advanced Usage
### File Extension Types
CakeIO defines two major categories of file extensions: **multi** file extensions and **single** file extensions.

> **Single File Extension**: A file extension that contains only one file extension component: e.g., `.txt` or `.bin`

> **Multi File Extension**: A file extension that contains more than one file extension component: e.g., `.cdr.txt` or `.bin.dat.zip`


An **UCakeFileExt** stores its file extension type via the enum `ECakeFileExtType`:
```cpp
auto ExtTypeNone    = ECakeFileExtType::EFT_None;
auto ExtTypeSingle  = ECakeFileExtType::EFT_Single;
auto ExtTypeMulti   = ECakeFileExtType::EFT_Multi;
```
The `None` type is used when an **UCakeFileExt**'s file extension is empty. When an **UCakeFileExt** is non-empty, it will be classified as either `Single` or `Multi`.

We can get the type of a particular **UCakeFileExt** via `GetExtType`:
```cpp
UCakeFileExt ExtNone{};
UCakeFileExt ExtSingle{ TEXT(".txt") };
UCakeFileExt ExtMulti{ TEXT(".cdr.txt") };

ECakeFileExtType ExtType = ExtNone.GetExtType(); // => EFT_None
ExtType = ExtSingle.GetExtType(); // => EFT_Single
ExtType = ExtMulti.GetExtType(); // => EFT_Multi
```

When working with multi file extensions, there may be times when we want to consider just its trailing extension. We can use the member function `CloneAsSingle` to get an **UCakeFileExt** copy that only contains the trailing file extension component:

```cpp
UCakeFileExt ExtMulti{ TEXT(".cdr.txt") };

UCakeFileExt ExtAsSingle = ExtMulti.CloneAsSingle();
PrintFileExt(*ExtAsSingle); // => ".txt"
```

{: .note }
Calling `CloneAsSingle` on an **UCakeFileExt** that is not a multi file extension is effectively the same as calling `Clone`. 




