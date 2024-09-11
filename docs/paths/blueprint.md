---
title: Blueprint
parent: Paths
nav_order: 2
---
{% assign in_source="CakePath_BP" %}
{% include components/source_info_blueprint.html %}

{% assign bp_path="path" %}

## UCakePath
{% include components/default_toc.md %}

## Introduction
The Blueprint path object in CakeIO is **UCakePath**. **UCakePath** is designed to provide an ergonomic and standardized way to work with filesystem paths. The following documentation will provide usage and guidance instructions for most situations.

{% include components/src_advert_blueprint.md %}


## Basic Usage
This section covers only fundamental **UCakePath** operations. Once you are comfortable using **UCakePath**s, consider looking at the advanced usage section for examples of more complex (and less common) scenarios.

### Creating Paths
We use the function `BuildCakePath` path to create **UCakePath** objects, submitting a string for the path the **UCakePath** should represent:

{% assign bp_file_id="build-cake-path" %}
{% include components/blueprint_image.md %}

To create a combined path from multiple strings, we use function `BuildCombinedCakePath`:
{% assign bp_file_id="build-cake-path-combined" %}
{% include components/blueprint_image.md %}

### Reading Paths as Strings
To read a **UCakePath**'s path as a string, we use the function `GetPathString`:
{% assign bp_file_id="get-path-string" %}
{% include components/blueprint_image.md %}

### Modifying Paths
If we want to change the path of a **UCakePath**, we use the `SetPath` member function:
{% assign bp_file_id="set-path-string" %}
{% include components/blueprint_image.md %}

We can also set the path to be the same as another UCakePath via the `SetPathViaOther` member function:
{% assign bp_file_id="set-path-other" %}
{% include components/blueprint_image.md %}

To check if a **UCakePath**'s path is empty, we can use the `IsEmpty` member function:
{% assign bp_file_id="is-empty" %}
{% include components/blueprint_image.md %}

To clear the path contents of an **UCakePath** back to the empty string we use the `Reset` member function:
{% assign bp_file_id="reset" %}
{% include components/blueprint_image.md %}

### Combining Paths
To make a new combined path using a source **UCakePath** and a string, we can use the member function `BuildCombined`.
{% assign bp_file_id="build-combined" %}
{% include components/blueprint_image.md %}

{: .note}
In the example above, the combined path will be `x/game/hero/hero.fbx`.

We can also make a combined path from two source **UCakePaths** via the member function `BuildCombinedViaOther`.
{% assign bp_file_id="build-combined-via-other" %}
{% include components/blueprint_image.md %}

{: .note}
In the example above, the combined path will be `x/game/hero/hero.fbx`.

To append a path directly to a pre-existing path, use `CombineInline` or `CombineInlineViaOther`.
{% assign bp_file_id="combine-inline" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="combine-inline-via-other" %}
{% include components/blueprint_image.md %}

{: .note}
In both examples above, the `PathGame`'s path will be set to `x/game/hero/hero.fbx`.

### Comparing Paths
UCakePath supports functions that check for path equality. It is important to understand that path equality is different from string equality; two paths are equal if they both refer to the same absolute location on the filesystem. 

To check if a UCakePath is equal to another path, we can use `IsEqualTo` or `IsEqualToOther`:
{% assign bp_file_id="is-equal-to" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="is-equal-to-other" %}
{% include components/blueprint_image.md %}

To check if a UCakePath is not equal to another path, we can use `IsNotEqualTo` or `IsNotEqualToOther`:
{% assign bp_file_id="is-not-equal-to" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="is-not-equal-to-other" %}
{% include components/blueprint_image.md %}

## Advanced Usage
The following sections detail advanced path manipulation techniques.

### Path Leaf Manipulation

#### Leaf Extraction
The leaf of the path is its rightmost component. Given the path `x/game/data`, the leaf is `data`.
We can get a copy path containing **UCakePath**'s leaf via ' `CloneLeaf`:
{% assign bp_file_id="clone-leaf" %}
{% include components/blueprint_image.md %}

To get the leaf of a **UCakePath** as a string, we can use `CloneLeafAsString`:
{% assign bp_file_id="clone-leaf-as-string" %}
{% include components/blueprint_image.md %}

{: .note }
In both examples above, the returned leaf is `data`.

#### Changing the Leaf
We can change the leaf of a path via `SetLeaf` or `SetLeafViaOther`.
{% assign bp_file_id="set-leaf" %}
{% include components/blueprint_image.md %}


{% assign bp_file_id="set-leaf-via-other" %}
{% include components/blueprint_image.md %}

{: .note }
In both examples above, the final path is `x/game/misc/`.

We can get a copy of a **UCakePath** with a new leaf via `CloneWithNewLeaf` or `CloneWithNewLeafViaOther`:

{% assign bp_file_id="clone-with-new-leaf" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="clone-with-new-leaf-via-other" %}
{% include components/blueprint_image.md %}

{: .note }
In both examples above, the returned path is `x/game/misc/`.

### Parent Path Manipulation
The parent path of a given path is all path components contained in the given path except for its leaf; the parent path of `x/game/data` is `x/game/`.

#### Parent Path Extraction
We can get a copy path containing **UCakePath**'s parent path via ' `CloneParentPath`:
{% assign bp_file_id="clone-parent-path" %}
{% include components/blueprint_image.md %}

To get the parent path of a **UCakePath** as a string, we can use `CloneParentPathAsString`:
{% assign bp_file_id="clone-parent-path-as-string" %}
{% include components/blueprint_image.md %}

{: .note }
In the example above, the parent path produced is `x/game/`.

#### Changing the Parent
We can change the parent of a **UCakePath** via `SetParentPath` or `SetParentPathViaOther`.

{% assign bp_file_id="set-parent-path" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="set-parent-path-via-other" %}
{% include components/blueprint_image.md %}

{: .note }
In both examples above, the final path is `z/network/data/`.


We can get a copy of a **UCakePath** with a new parent via `CloneWithNewParent` or `CloneWithNewParentViaOther`:

{% assign bp_file_id="clone-with-new-parent" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="clone-with-new-parent-via-other" %}
{% include components/blueprint_image.md %}

{: .note }
In both examples above, the cloned path is `z/network/data/`.

### Absolute Paths
UCakePath provides ways to convert relative paths into absolute paths. When converting relative paths into absolute paths, the location of the executable will be used as the anchor point for expansion. Thus, if we have a relative path `game/data` and our executable resides on `/x/other/game.exe`, converting `game/data` into absolute form will result in the path `/x/other/game/data/`.
However, if a path is already in absolute form then any absolute conversion will have no effect -- this means that __absolute paths not relative to the executable's location will not be changed if an absolute conversion is attempted on them__.

{: .hint }
The executable location used for absolute path conversion will be different when you are running the editor versus running a packaged project. Make sure you know the context in which your absolute conversions will be executed to avoid any surprises.

We can build an absolute path explicitly with `BuildCakePathAbsolute`:

{% assign bp_file_id="build-cake-path-absolute" %}
{% include components/blueprint_image.md %}

To set a path and ensure the final form is absolute, we can use `SetPathAbsolute` or `SetPathAbsoluteViaOther`:
{% assign bp_file_id="set-path-absolute" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="set-path-absolute-via-other" %}
{% include components/blueprint_image.md %}

To clone an FCakePath and ensure it is in absolute form, use `CloneToAbsolute` or `CloneToAbsoluteAsString`:
{% assign bp_file_id="clone-to-absolute" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="clone-to-absolute-as-string" %}
{% include components/blueprint_image.md %}

To convert an existing FCakePath to absolute form, use `ToAbsoluteInline`:
{% assign bp_file_id="to-absolute-inline" %}
{% include components/blueprint_image.md %}

To build combined absolute paths, use the function `BuildCakePathCombinedAbsolute`:
{% assign bp_file_id="build-cake-path-combined-absolute" %}
{% include components/blueprint_image.md %}

To build combined absolute paths from a pre-existing **UCakePath**, use the member function `BuildCombinedAbsolute` or `BuildCombinedAbsoluteViaOther`:
{% assign bp_file_id="build-combined-absolute" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="build-combined-absolute-via-other" %}
{% include components/blueprint_image.md %}

### Replacing Subpaths
**UCakePath** has an interface to support replacing a subpath via the member function `ReplaceSubpath`. A subpath here is defined as a subsection of path components contained in a larger path: e.g., `game/data` is a subpath of `/x/misc/game/data/other`.

As an example, let's say that we are attempting to move a directory tree into another directory, maintaining the relative tree.

{% assign bp_file_id="replace-subpath" %}
{% include components/blueprint_image.md %}

In the example above, by using `ReplaceSubpath` we were able to replace the subpath `x/game/data` to `y/archive/data` while maintaining the rest of the relative tree `misc/saves`.

If we want to change a subpath of an existing **UCakePath** instead of generating a copy, we can use `ReplaceSubpathInline`:

{% assign bp_file_id="replace-subpath-inline" %}
{% include components/blueprint_image.md %}