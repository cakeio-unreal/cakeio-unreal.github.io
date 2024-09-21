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
To create a **UCakeFileExt** we can use `BuildCakeFileExt`:
{% assign bp_file_id="build-cake-file-ext" %}
{% include components/blueprint_image.md %}

{: .note }
**UCakeFileExt** is very lenient when it comes to file extension input strings; it doesn't matter if you include a leading '.' or not, the final result will be converted into the standard form.

To create a **UCakeFileExt** by extracting the file extension from a file name, we can use `BuildCakeFileExtFromFileName`.
{% assign bp_file_id="build-cake-file-ext-from-file-name" %}
{% include components/blueprint_image.md %}

{: .warning }
Make sure you are sending input strings that are only file names into `BuildCakeFileExtFromFileName`. While the function can technically extract file extensions from paths, there is a danger of an erroneous extraction since the file extension separator '.' is valid to use in directory names in most major operating systems. 

If we want to create a **UCakeFileExt** whose file extension is initially empty, we can use `BuildCakeFileExtEmpty`:
{% assign bp_file_id="build-cake-file-ext-empty" %}
{% include components/blueprint_image.md %}

We can create a **UCakeFileExt** copy of a **UCakeFileExt** via `Clone`:
{% assign bp_file_id="clone" %}
{% include components/blueprint_image.md %}

We can create a string copy of a **UCakeFileExt** via `CloneAsString`:
{% assign bp_file_id="clone-as-string" %}
{% include components/blueprint_image.md %}

### Reading the file extension
To read the file extension as a string, we use `GetExtString`:
{% assign bp_file_id="get-ext-string" %}
{% include components/blueprint_image.md %}

### Changing the file extension
We can change a **UCakeFileExt**'s file extension to a different extension via `SetFileExt` or `SetFileExtViaOther`:

{% assign bp_file_id="set-file-ext" %}
{% include components/blueprint_image.md %}

{: .note }
After the `SetFileExt` call, the **UCakeFileExt**'s new file extension is `.bin`.

{% assign bp_file_id="set-file-ext-via-other" %}
{% include components/blueprint_image.md %}

{: .note }
After the `SetFileExtViaOther` call, the **UCakeFileExt**'s new file extension is `.bin.dat`.


We can also extract the extension from a file name and set our extension to the extracted result via `SetFileExtFromFileName`:
{% assign bp_file_id="set-file-ext-from-file-name" %}
{% include components/blueprint_image.md %}

{: .warning }
Only send file names without other path components to `SetFileExtFromFileName` in order to ensure the extraction is correct.

We can check if a **UCakeFileExt** currently has a non-empty file extension via `IsEmpty`:

{% assign bp_file_id="is-empty" %}
{% include components/blueprint_image.md %}

We can clear a **UCakeFileExt**'s file extension via `Reset`:
{% assign bp_file_id="reset" %}
{% include components/blueprint_image.md %}

### Combining file extensions
We can build a **UCakeFileExt** that is a combination of two extensions with `BuildCombined` or `BuildCombinedViaOther`:

{% assign bp_file_id="build-combined" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="build-combined-via-other" %}
{% include components/blueprint_image.md %}

{: .note }
In both examples above, the **UCakeFileExt** returned has the file extension `.cdr.txt`.

We can append a file extension onto a UCakeFileExt with `CombineInline` or `CombineInlineViaOther`:
{% assign bp_file_id="combine-inline" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="combine-inline-via-other" %}
{% include components/blueprint_image.md %}

{: .note }
In both examples above, the **UCakeFileExt** has the file extension `.cdr.txt`.

### Comparing file extensions
To check if a **UCakeFileExt** is equal to another file extension, we can use `IsEqualTo` or `IsEqualToOther`. 

{% assign bp_file_id="is-equal-to" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="is-equal-to-other" %}
{% include components/blueprint_image.md %}

To check if a **UCakeFileExt** is not equal to another file extension, we can use `IsNotEqualTo` or `IsNotEqualToOther`. 

{% assign bp_file_id="is-not-equal-to" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="is-not-equal-to-other" %}
{% include components/blueprint_image.md %}

## Advanced Usage
### File Extension Types
CakeIO defines two major categories of file extensions: **multi** file extensions and **single** file extensions.

> **Single File Extension**: A file extension that contains only one file extension component: e.g., `.txt` or `.bin`

> **Multi File Extension**: A file extension that contains more than one file extension component: e.g., `.cdr.txt` or `.bin.dat.zip`

A **UCakeFileExt** stores its file extension type via the enum `ECakeFileExtType`:
{% assign bp_file_id="enum-ext-type" %}
{% include components/blueprint_image.md %}

We can get the type of a particular **UCakeFileExt** via `GetExtType`:
{% assign bp_file_id="get-ext-type" %}
{% include components/blueprint_image.md %}

When working with multi file extensions, there may be times when we want to consider just its trailing extension. We can use the member function `CloneAsSingle` to get a **UCakeFileExt** copy that only contains the trailing file extension component of the original:

{% assign bp_file_id="clone-as-single" %}
{% include components/blueprint_image.md %}

{: .note }
Calling `CloneAsSingle` on a **UCakeFileExt** that is not a multi file extension is effectively the same as calling `Clone`. 
