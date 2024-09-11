---
title: Native
parent: Paths
nav_order: 1
---
{% assign in_source="CakePath" %}
{% include components/source_info.html %}

## FCakePath
{% include components/default_toc.md %}

## Introduction
The native path object in CakeIO is **FCakePath**. **FCakePath** is designed to provide an ergonomic and standardized way to work with filesystem paths. The following documentation will provide usage and guidance instructions; the source code is also an excellent reference as it is fully documented, please consider studying it at some point if you wish to learn even more about CakeIO and its implementation.

## Required Includes
All source code examples going forward will assume that your code has the following include statement:
```cpp
#include "CakeIO/CakePath.h"
```
## Basic Usage
This section covers only fundamental **FCakePath** operations. Once you are comfortable using **FCakePath**s, consider looking at the advanced usage section for examples of more complex (and less common) scenarios.

### Creating Paths
The most straightforward way to create a new **FCakePath** is to use the constructor and submit an **FString**:
```cpp
FCakePath FirstPath{ TEXT("x/game/data") };
```

We can also create an **FCakePath** via constructor with another **FCakePath**:
```cpp
FCakePath SecondPath{ FirstPath };
```

To create a combined path from multiple **FString**s, use the static method `BuildCombinedPath`:
```cpp
FCakePath CombinedPath{ FCakePath::BuildCombinedPath(TEXT("x/game"), TEXT("data")) };
```
### Copying Paths
To get a copy of an existing FCakePath, use `Clone`:
```cpp
FCakePath SourcePath{ TEXT("x/game/data") };

FCakePath ClonedPath{ SourcePath.Clone() };
```

To get a copy of an existing FCakePath as an FString, use `CloneAsString`:
```cpp
FCakePath SourcePath{ TEXT("x/game/data") };

FString ClonedPathString{ SourcePath.CloneAsString() };
```
### Reading Paths as FStrings
To read an **FCakePath**'s path as an **FString**, we can use `operator*` or `GetPathString`:
```cpp
FCakePath PathData{ TEXT("x/game/data") };
PrintPath(*PathData); // => "x/game/data"
PrintPath(PathData.GetPathString()); // => "x/game/data"
```
### Modifying Paths
If we want to change the path an **FCakePath**, we use the `SetPath` member function:
```cpp
FCakePath PathMisc{ TEXT("x/game/data") };
PathMisc.SetPath( TEXT("y/misc/other") );
PrintPath(*PathMisc); // => "y/misc/other"
```
`SetPath` is overloaded to accept both **FString** and **FCakePath** arguments as parameters:
```cpp
FCakePath PathOther{ TEXT("y/misc/other") };
PathMisc.SetPath(PathOther);
PrintPath(*PathMisc); // => "y/misc/other"
```
To check if an **FCakePath**'s path is empty, we can use the `IsEmpty` member function:
```cpp
bool bPathIsEmpty = PathMisc.IsEmpty(); // => false
```
To clear the path contents of an **FCakePath** back to the empty string we use the `Reset` member function:
```cpp
PathMisc.Reset();
bPathIsEmpty = PathMisc.IsEmpty(); // => true
```

### Combining Paths
To make a new path that combines more than one path, use `operator/`.
```cpp
FCakePath PathGame{ TEXT("x/game/") };
FCakePath PathHeroFile{ TEXT("hero/hero.fbx") };

FCakePath PathToHeroFile{ PathGame / PathHeroFile };
PrintPath(*PathToHeroFile);
```

We can combine more than two paths with `operator/`:
```cpp
FCakePath PathDrive{ TEXT("x") };
FCakePath PathGameOnly{ TEXT("game") };
FCakePath PathDataOnly{ TEXT("data") };

FCakePath PathDataCombined = PathDrive / PathGameOnly / PathDataOnly;
PrintPath(*PathDataCombined); // => "x/game/data"
```

We can also use `operator/` on a mixture of **FCakePath** and **FString**:
```cpp
PathToHeroFile = PathGame / TEXT("hero/hero.fbx");
```

However, we must be careful here. If we start with an **FString** path and use `operator/` with an **FCakePath**, this will fail, because it will be calling **FString**'s `operator/`.
```cpp
FString GamePath{ TEXT("x/game/") };
FCakePath PathHeroFile{ TEXT("hero/hero.fbx") };

PathToHeroFile = GamePath / PathHeroFile; // Will fail to compile (FString / FCakePath)
```

To fix this, we can explicitly use **FString**'s `operator/` by getting the path string from the **FCakePath**:
```cpp
PathToHeroFile =  GamePath / *PathHeroFile; // OK, calls FString / FString.
```
Or we can convert the **FString** into an **FCakePath**:
```cpp
PathToHeroFile =  FCakePath(GamePath) / PathHeroFile; // OK, calls FCakePath / FCakePath.
```

{: .hint }
Whenever possible, favor using **FCakePath** over **FString**.

If you prefer to call explicit methods instead of operators, you can use `BuildCombined`:
```cpp
FCakePath PathGame{ TEXT("x/game/") };
FCakePath PathHeroFile{ TEXT("hero/hero.fbx") };

FCakePath PathFullHero{ PathGame.BuildCombined(PathHeroFile) };
PrintPath(*PathFullHero);
```

To append a path directly to a pre-existing path, use `operator/=` or `CombineInline`:
```cpp
FCakePath PathDrive{ TEXT("x") };
FCakePath PathDataOnly{ TEXT("data") };

PathDrive /= TEXT("game");
PathDrive.CombineInline(PathDataOnly);
PrintPath(*PathDrive); // => "x/game/data"
```

### Comparing Paths
Path equality is handled via `operator==`. It is important to understand that path equality is different from string equality; two paths are equal if they both refer to the same absolute location on the filesystem. 
```cpp
FCakePath PathData{ TEXT("x/game/data") };
FCakePath PathDataCopy{ TEXT("x/game/data") };
FCakePath PathMisc{ TEXT("y/game/misc") };

bool bPathsAreEqual{ false };
bPathsAreEqual = PathData == TEXT("x/game"); // => false
bPathsAreEqual = PathData == PathMisc; // => false
bPathsAreEqual = PathData == PathDataCopy; // => true

bPathsAreEqual = PathData != TEXT("x/game"); // => true
bPathsAreEqual = PathData != PathMisc; // => true
bPathsAreEqual = PathData != PathDataCopy; // => false
```
## Advanced Usage
The following sections detail advanced path manipulation techniques.
### Path Leaf Manipulation
#### Leaf Extraction
The leaf of the path is its rightmost component. Given the path `x/game/data`, the leaf is `data`.
We can extract the leaf from an **FCakePath** via `CloneLeaf` and `CloneLeafAsString`.
```cpp
FCakePath SourcePath{ TEXT("x/game/data") };

FCakePath LeafPath = SourcePath.CloneLeaf();
FString LeafString = SourcePath.CloneLeafAsString();
```
{: .note }
The FString/FCakePath returned will be empty if there is no leaf to extract.

#### Changing the Leaf
We can change the leaf of a path via `SetLeaf`; there are overloads for both **FString** and **FCakePath**:

```cpp
FCakePath SourcePath{ TEXT("x/game/data") };

SourcePath.SetLeaf( TEXT("cakemix_standard") ); // path is now "x/game/cakemix_standard"
SourcePath.SetLeaf( FCakePath(TEXT("cakemix_extra")) ); // path is now "x/game/cakemix_extra"
```

We can get a copy of an **FCakePath** with a new leaf via `CloneWithNewLeaf`:
```cpp
FCakePath SourcePath{ TEXT("x/game/data") };

FString NewLeafString { TEXT("cakemix") };
FCakePath NewLeaf{ NewLeafString };

FCakePath NewLeaf = SourcePath.CloneWithNewLeaf(NewLeaf);// NewLeaf path is "x/game/new_leaf"
NewLeaf = SourcePath.CloneWithNewLeaf(NewLeafString);// NewLeaf path is "x/game/new_leaf"
```
### Parent Path Manipulation
The parent path of a given path is all path components contained in the given path except for its leaf; the parent path of `x/game/data` is `x/game/`.

#### Parent Path Extraction
We can extract the parent of an **FCakePath** via `CloneParentPath` and `CloneParentPathAsString`. 
```cpp
FCakePath SourcePath{ TEXT("x/game/data") };

FCakePath ParentPath{ SourcePath.CloneParentPath() };
FString ParentString{ SourcePath.CloneParentPathAsString() };
```
{: .note }
The FString/FCakePath returned will be empty if there is no parent path to extract.

#### Changing the Parent
We can change the parent of a path via `SetParentPath`, which is overloaded to accept either an **FCakePath** or an **FString**.

```cpp
FCakePath ParentSourcePath{ TEXT("x/game/data") };

FCakePath NewParent{ TEXT("z/network/remote") };
FString NewParentString{ TEXT("y/cake/sugar") };

ParentSourcePath.SetParentPath(NewParent);
// Path is now "z/network/remote/data"
UE_LOG(LogTemp, Warning, TEXT("    Path After SetParentPath (FCakePath): [%s]"), **ParentSourcePath)

ParentSourcePath.SetParentPath(NewParentString);
// Path is now "y/cake/sugar/data"
UE_LOG(LogTemp, Warning, TEXT("    Path After SetParentPath (FString): [%s]"), **ParentSourcePath)
```

We can get a copy of an **FCakePath** with a new parent via `CloneWithNewParent`:

```cpp
FCakePath SourcePath{ TEXT("x/game/data") };

FString CloneParentString{ TEXT("a/nother/parent") };
FCakePath CloneParentPath{ CloneParentString };

// We can use FString or FCakePath overloads
FCakePath ClonedNewParent = SourcePath.CloneWithNewParent(CloneParentString);
ClonedNewParent = SourcePath.CloneWithNewParent(CloneParentPath);

// The resultant path is "a/nother/parent/data"
```

### Absolute Paths
**FCakePath** provides ways to convert relative paths into absolute paths. When converting relative paths into absolute paths, the location of the executable will be used as the anchor point for expansion. Thus, if we have a relative path `game/data` and our executable resides on `/x/other/game.exe`, converting `game/data` into absolute form will result in the path `/x/other/game/data/`.
However, if a path is already in absolute form then any absolute conversion will have no effect -- this means that __absolute paths not relative to the executable's location will not be changed if an absolute conversion is attempted on them__.

{: .hint }
The executable location used for absolute path conversion will be different when you are running the editor versus running a packaged project. Make sure you know the context in which your absolute conversions will be executed to avoid any surprises.

We can build an absolute path explicitly with `BuildAbsolute`:

```cpp
FCakePath AbsolutePath{ FCakePath::BuildAbsolute("game/data") };
UE_LOG(LogTemp, Warning, TEXT("BuildAbsolute path: [%s]"), **AbsolutePath);
```

To set a path and ensure the final form is absolute, we can use `SetPathAbsolute`:
```cpp
AbsolutePath.SetPathAbsolute( TEXT("misc/models") );
UE_LOG(LogTemp, Warning, TEXT("SetPathAbsolute: [%s]"), **AbsolutePath);

// Absolute operations will apply no transformation if the source path is already an absolute path
AbsolutePath.SetPathAbsolute( TEXT("A:\\windows\\path\\game\\data") );
UE_LOG(LogTemp, Warning, TEXT("Windows Abs path: [%s]"), **AbsolutePath); // => "A:\windows\path\game\data"
AbsolutePath.SetPathAbsolute( TEXT("/a/unix/path/game/data") );
UE_LOG(LogTemp, Warning, TEXT("Unix Abs path: [%s]"), **AbsolutePath); // => "/a/unix/path/game/data"
```
To clone an **FCakePath** and ensure the cloned path is in absolute form, use `CloneToAbsolute` or `CloneToAbsoluteAsString`:

```cpp
FCakePath SourcePath( TEXT("other/misc") );

FCakePath ClonedAbsolutePath{ SourcePath.CloneToAbsolute() }; 
FString ClonedAbsPathString{ SourcePath.CloneToAbsoluteAsString() };
UE_LOG(LogTemp, Warning, TEXT("CloneToAbsolute: [%s]"), **ClonedAbsolutePath);
```

To convert an existing **FCakePath** to absolute form, use `ToAbsoluteInline`:

```cpp
FCakePath SourcePath( TEXT("other/misc") );

SourcePath.ToAbsoluteInline();
UE_LOG(LogTemp, Warning, TEXT("ToAbsoluteInline: [%s]"), **SourcePath);
```

To build combined absolute paths, use the static function `BuildCombinedPathAbsolute`:
```cpp
// We can build combined paths and ensure they are in absolute form via BuildCombinedPathAbsolute
FCakePath CombinedAbsPath{ FCakePath::BuildCombinedPathAbsolute( 
    TEXT("misc/data"), 
    TEXT("animations/hero") ) 
};

UE_LOG(LogTemp, Warning, TEXT("BuildCombinedPathAbsolute: [%s]"), **CombinedAbsPath);
```

To build combined absolute paths from a pre-existing source **FCakePath**, use the member function `BuildCombinedAbsolute`:
```cpp
FCakePath SourceRelative{ TEXT("src/systems") };

FCakePath NetworkingPath{ SourceRelative.BuildCombinedAbsolute(TEXT("network")) };
UE_LOG(LogTemp, Warning, TEXT("BuildCombinedAbsolute: [%s]"), **NetworkingPath);
```
### Replacing Subpaths
**FCakePath** has an interface to support replacing a subpath via the member function `ReplaceSubpath`. A subpath here is defined as a subsection of path components contained in a larger path: e.g., `game/data` is a subpath of `/x/misc/game/data/other`.

As an example, let's say that we are attempting to move a directory tree into another directory, maintaining the relative tree.

```cpp
FCakePath    SourcePath{ TEXT("x/game/data/misc/saves") };
FCakePath TargetSubpath{ TEXT("x/game/data")            };
FCakePath DestDirectory{ TEXT("y/archive/data")         };

FCakePath FinalPath = SourcePath.ReplaceSubpath(DestDirectory, TargetSubpath); 
// FinalPath:  "y/archive/data/misc/saves"
UE_LOG(LogTemp, Warning, TEXT("ReplaceSubpath path: [%s]"), **FinalPath);
```

In the example above, by using `ReplaceSubpath` we were able to replace the subpath `x/game/data` with `y/archive/data` while maintaining the rest of the relative tree `misc/saves`.

If we want to change a subpath of an existing FCakePath instead of generating a copy, we can use `ReplaceSubpathInline`:

```cpp
FCakePath    SourcePath{ TEXT("x/game/data/misc/saves") };
FCakePath TargetSubpath{ TEXT("x/game/data")            };
FCakePath DestDirectory{ TEXT("y/archive/data")         };

SourcePath.ReplaceSubpathInline(DestDirectory, TargetSubpath);
// SourcePath is now:  "y/archive/data/misc/saves"
UE_LOG(LogTemp, Warning, TEXT("ReplaceSubpathInline path: [%s]"), **SourcePath); 
```