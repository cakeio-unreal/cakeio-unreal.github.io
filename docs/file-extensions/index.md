---
title: File Extensions
nav_order: 6
---

## File Extensions Overview
{: .no_toc .text-delta }
1. TOC
{:toc}
## File Extensions
CakeIO uses a dedicated type for representing file extensions. This type ensures that all file extensions are represented in a common format, and it also supplies a variety of interfaces to support file extension querying and manipulation. 

### Standardized Representation
The CakeIO file extension objects ensure that their associated file extensions are represented in a common format. Users do not have to worry about whether to include the leading period in a file extension, they can input an extension in either format and the file extension object will ensure it is transformed into the same form. 

Furthermore, the file extension objects will also handle malformed file extension inputs, such as ".txt..dat.". The file extension will still be parsed correctly and any extraneous separating characters will be removed.

### File Extension Types
The CakeIO file extension objects have a concept of file extension types. Currently, there are two types of file extensions recognized: single and multi file extensions. A single file extension is a file extension that consists of only one component, such as the extension ".txt" or ".json." A multi file extension is a file extension that consists of more than one component, such as ".cdr.txt" or ".bin.dat". 

This classification system allows for more advanced processing of file extensions based on their extension type; for an example, see WithFilter directory iteration, which has different forms of matching logic based on file extension types.

### File Extension Documentation
The following documentation sections will provide an overview of many of the interfaces you will commonly use with CakeIO file objects. However, if you want to see the entire interface, please examine the source code which is fully documented. Each article will include the location of the header files for the associated types.

{% include native_bp_divide.md %}