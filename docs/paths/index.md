---
title: Paths
nav_order: 4
---
## Paths Overview
{: .no_toc .text-delta }
1. TOC
{:toc}

## Paths
CakeIO uses a dedicated type for storing filesystem paths. It ensures that every path is in a standardized form, regardless of the input path. Paths also offer a variety of utility functions for path querying and manipulation. 

### Standardized Path Representation
One of the primary purposes of the path object is to ensure that all paths are represented in a common, standardized form. This standardized form relieves the caller of concerning themselves with path representation. It doesn't matter if we input Windows style paths or UNIX style paths to the path object, or whether we include the trailing path separator -- the path object will take any input path and transform it into a common form for us.

### Advanced Path Manipulation
Storing a path as merely an FString is error-prone and obviates type-safety. With a dedicated path object, we can define more precise interfaces that expect system paths, and also the path object itself can provide a rich interface of path specific operations. The path object supports a wide variety of path operations, from path manipulation to querying various informational details about a path. 

### Path Documentation
The following documentation will provide guidance and usage instructions for the majority of use-cases with the path object. However, if you want to see the entire interface in an exhaustive format, please examine the source code which is fully documented. Each article will include the location of the header files for the associated types.

{% include native_bp_divide.md %}