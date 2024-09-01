---
title: Overview
layout: default
nav_order: 2
---

## Introduction
Welcome to the CakeIO documentation! All major areas of this documentation are split into two parts: Native and Blueprint.
Native provides examples and guidance for the C++ version of CakeIO, and Blueprint provides examples and guidance for the Blueprint version of CakeIO. 

The source code is provided with the plugin-in and the source code is fully documented. For this reason, one of the best ways to learn about CakeIO is to browse the source code directly. Whenever possible, any associated headers are included in this documentation so that you can study the related source code directly. 

(section about feedback)

Without further ado, let's examine the key features that define the CakeIO API.

## Key Features

### Cake Core Objects
CakeIO offers a set of three core objects that simplify and enhance Unreal's base IO interfaces: CakePath, CakeFile, and CakeDir. There are two different versions of these types; one for C++ and one for Blueprint. 

For a quick introduction to using the core objects, see the Flash Tour.
For a more detailed examination, see the Core Objects section.

### Enhanced Error Reporting
Any IO operation in CakeIO will return an error type associated with that particular operation. These error types will provide the caller with the necessary context to understand both when and why an operation fails. There are various utilities built on top of these error types in order to keep error handling as ergonomic as possible.

For more information, please see (Error Handling).

### Policies
There are a variety of policy enums defined by CakeIO that will modify function behavior based upon their values; these policies allow granular control over the various IO operations supported by CakeIO.

For more information, please see (Cake IO Policies).

### Advanced Directory Iteration
CakeIO offers a large set of directory iteration functions in order to give users an ergonomic interface to achieve iteration of any complexity. There are three styles of iteration available, each providing a different level of control to the caller.

For more information, see (Advanced Directory Iteration).

### File Extensions
CakeIO provides a dedicated type for file extensions. This type enforces a standard, normalized representation of file extensions and provides a set of utility functions for dealing with nd classifying file extensions.  

For more information, please see (File Extensions).

### CakeMix Library
CakeIO's CakeMixLibrary provides a suite of utility functions that range from extra directory or file operations to generating human-readable strings for the various CakeIO error/result types. 

It also serves as a valuable example for how users can easily create their own various advanced utility functions for CakeIO core objects.

For more information, see (CakeMixLibrary).
