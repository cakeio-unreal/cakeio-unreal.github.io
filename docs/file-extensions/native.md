---
title: Native
parent: File Extensions
nav_order: 1
---

{% assign in_source="CakeFile" %}
{% include components/source_info.html %}

## FCakeFileExt
{% include components/default_toc.md %}

## Introduction
The native object for dealing with file extensions is **FCakeFileExt**. This object is meant to represent a file extension and ensures that the file extension is represented in a standard, common form. Furthermore, it provides various utilities for working with file extensions.

## Basic Usage
### Construction
To create an FCakeFileExt, all we need to do is supply an FString of the file extension we want it to store:
```cpp
FCakeFileExt ExtExample{ TEXT(".txt") };
```

{: .note }
FCakeFileExt is very lenient when it comes to file extension input strings; it doesn't matter if you include a leading '.' or not, the final result will be converted into the standard form.


To create a FCakeFileExt by extracting the file extension from a file name, we can use the static function `BuildFileExtFromFileName`.
```cpp
FCakeFileExt ExtFromFile{ FCakeFileExt::BuildFileExtFromFileName(TEXT("example_file.txt")) };
```

{: .warning }
Make sure you are sending input strings that are only file names into `BuildFileExtFromFileName`. While the function can technically extract file extensions from paths, there is a danger of an erroneous extraction since the file extension separator '.' is valid to use in directory names in most major operating systems. 

We can create an **FCakeFileExt** copy of an **FCakeFileExt** via `Clone`:
```cpp
FCakeFileExt ExtA{ TEXT(".txt") };

FCakeFileExt ExtACopy = ExtA.Clone();
```

We can create an **FString** copy of an **FCakeFileExt** via `CloneAsString`:
```cpp
FCakeFileExt ExtA{ TEXT(".txt") };

FString ExtAString = ExtA.CloneAsString();
```

### Reading the file extension
To read the file extension as an **FString**, we can use either `operator*` or `GetExtString`:
```cpp
PrintFileExt( *ExtExample );
PrintFileExt( ExtExample.GetExtString() );
```
### Changing the file extension
We can change the file extension to a different extension via `SetFileExt`, which accepts either an **FString** or another **FCakeFileExt**:

```cpp
FCakeFileExt ExtExample{ TEXT(".txt") };
FCakeFileExt ExtOther{ TEXT("bin.dat") };

ExtExample.SetFileExt( TEXT("bin") );
ExtExample.SetFileExt(ExtOther);
```

We can also extract the extension from a file name and set our extension to the extracted result via `SetFileExtFromFileName`:
```cpp
ExtExample.SetFileExtFromFileName(TEXT("spells.db"));
```

{: .warning }
Only send file names without other path components to `SetFileExtFromFileName` in order to ensure the extraction is correct.


We can check if an **FCakeFileExt** currently has a non-empty file extension via `IsEmpty`:

```cpp
ExtExample.SetFileExt(TEXT(".bin"));
bool bIsEmpty = ExtExample.IsEmpty(); // => false
```
We can clear an **FCakeFileExt**'s file extension via `Reset`:
```cpp
ExtExample.Reset();
bIsEmpty = ExtExample.IsEmpty(); // => true
```
### Combining file extensions
We can build combined extensions with `operator+`:
```cpp
FCakeFileExt ExtA{ TEXT(".txt") };
FCakeFileExt ExtB{ TEXT(".cdr") };

FCakeFileExt ExtCombined = ExtB + ExtA; // => ".cdr.txt"
ExtCombined = ExtA + TEXT("bin"); // => ".txt.bin"
```
We can also use `BuildCombined` instead of `operator+`:
```cpp
FCakeFileExt ExtA{ TEXT(".txt") };
FCakeFileExt ExtB{ TEXT(".cdr") };

FCakeFileExt ExtCombined = ExtB.BuildCombined(ExtA); // => ".cdr.txt"
ExtCombined = ExtA.BuildCombined( TEXT("bin") ); // => ".txt.bin"
```

We can append a file extension onto an FCakeFileExt with either `operator+=` or `CombineInline`:
```cpp
FCakeFileExt ExtA{ TEXT(".txt") };
FCakeFileExt ExtB{ TEXT(".cdr") };

ExtA += ExtB; // => ".txt.cdr"
ExtA.CombineInline( TEXT(".bin.dat") ); // => ".txt.cdr.bin.dat"
```

### Comparing file extensions
We can use equality comparison against **FCakeFileExt** via `operator==` and `operator!=`. We can check equality against other **FCakeFileExt**s and **FString**s.

```cpp
FCakeFileExt ExtA{ TEXT(".txt") };
FCakeFileExt ExtB{ TEXT(".cdr") };

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


An **FCakeFileExt** stores its file extension type via the enum `ECakeFileExtType`:
```cpp
auto ExtTypeNone    = ECakeFileExtType::EFT_None;
auto ExtTypeSingle  = ECakeFileExtType::EFT_Single;
auto ExtTypeMulti   = ECakeFileExtType::EFT_Multi;
```
The `None` type is used when an **FCakeFileExt**'s file extension is empty. When an **FCakeFileExt** is non-empty, it will be classified as either `Single` or `Multi`.

We can get the type of a particular **FCakeFileExt** via `GetExtType`:
```cpp
FCakeFileExt ExtNone{};
FCakeFileExt ExtSingle{ TEXT(".txt") };
FCakeFileExt ExtMulti{ TEXT(".cdr.txt") };

ECakeFileExtType ExtType = ExtNone.GetExtType(); // => EFT_None
ExtType = ExtSingle.GetExtType(); // => EFT_Single
ExtType = ExtMulti.GetExtType(); // => EFT_Multi
```

When working with multi file extensions, there may be times when we want to consider just its trailing extension. We can use the member function `CloneAsSingle` to get an **FCakeFileExt** copy that only contains the trailing file extension component:

```cpp
FCakeFileExt ExtMulti{ TEXT(".cdr.txt") };

FCakeFileExt ExtAsSingle = ExtMulti.CloneAsSingle();
PrintFileExt(*ExtAsSingle); // => ".txt"
```

{: .note }
Calling `CloneAsSingle` on an **FCakeFileExt** that is not a multi file extension is effectively the same as calling `Clone`. 



