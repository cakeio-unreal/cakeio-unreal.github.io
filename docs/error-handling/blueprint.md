---
title: Blueprint
parent: Error Handling
nav_order: 2
---

{% assign header_parent="Result" %}
## Error Handling
{% include components/default_toc.md %}

## Introduction
**CakeIO** introduces a variety of custom types that indicate the outcome of IO operations. Though each type will have some unique properties, there are some common design patterns and programming idioms that can be applied to all of the error types. 

The error handling in CakeIO was designed to be an opt-in experience for the callers -- all result types have `operator bool` defined so that IO operation functions outcomes can be expressed as successes or failures. However, should the caller wish to know more details surrounding the outcome, these error types will help give greater context. For instance, if a file move operation fails, that failure can occur in many different ways. The error code returned will grant the caller greater context -- perhaps the file itself did not exist, the copy operation failed, or the delete operation failed. 

## Result Types
{% assign link_desc="CakeMixLibrary" %}
All IO operations return result types, and these are convenience types that wrap either an underlying error code (for file and directory IO operations) or an outcome code (for directory iterations). The actual codes are simple enums, and the result types are very simple types that add some extra utility and convenience functions. {% include rlinks/cakemix_native.md %} also offers functions that will take result types and generate human-readable strings for them. 

In the following sections, we'll examine these result types and the wrapped error / outcome codes in detail.

### Opt-In Error Handling
The error handling in CakeIO was designed to be an opt-in experience for the callers -- all result types have `operator bool` defined so that IO operation functions outcomes can be expressed as successes or failures. Thus, a caller is never forced to create elaborate error handling when using CakeIO interfaces.

However, should the caller wish to know more details surrounding the outcome, these error types will help give greater context. For instance, if a file move operation fails, that failure can occur in many different ways. The error code returned will grant the caller greater context -- perhaps the file itself did not exist, the copy operation failed, or the delete operation failed. 

## File and Directory Error Handling
{% assign in_source="CakeFileError|CakeFileOpResult|CakeDirError|CakeDirOpResult" %}
{% include components/source_info_ex.html %}
File and directory error handling is very similar, and so we'll look at them together. Any file IO operation will return an `FCakeFileOpResult`, which in turn wraps an `FCakeFileError` error code.
```cpp
FCakeFileOpResult FileOpResult{ FCakeFileOpResult::OK() };
ECakeFileError ErrorCode = FileOpResult.ErrorCode;
```

Likewise, any directory IO operation will return an `FCakeDirOpResult`, which wraps an `FCakeDirError` error code.
```cpp
FCakeDirOpResult DirOpResult{ FCakeDirOpResult::OK() };
ECakeDirError ErrorCode = DirOpResult.ErrorCode;
```

### OK and NOP
Both file and directory error codes have two values that do not indicate an actual error: `OK` and `NOP`. It is important to understand the difference between these two errors.

> **OK**: The IO operation was executed and encountered no errors.

> **NOP**: The IO operation was not necessary and was not executed.

An example of a situation that might generate a **NOP** is when we attempt to delete a file or directory that doesn't exist. The benefit of distinguishing between **OK** and **NOP** is that we can know whether or not an IO operation actually occurred and work was done. 

In many scenarios, callers likely won't care to distinguish between **OK** and **NOP**, since either error value means that the file system is in the desired state after the operation resolved. That is why `operator bool` and the result type's convenience function `IsOk` will return true if the value is **OK** _or_ **NOP**.

```cpp
if (FileOpResult) // OK or NOP
{ 
    // ... 
}
if (FileOpResult.IsOk())  // OK or NOP
{ 
    // ... 
}
```

However, when we want to only do something when an IO operation actually occurs, we can use `IsOkStrict`, which only returns true if the error code is **OK**:

```cpp
if (FileOpResult.IsOkStrict()) // OK
{
    //...
}
```

For a pragmatic example of `IsOkStrict`'s value, we can look to the `MoveFile` implementation. `FCakeFile` needs to update its path information when it is moved, but it should only update that path information when a move actually occurs. We can easily setup a branch for updating the path via `IsOkStrict`:

```cpp
const FCakeFileOpResult MoveResult{ 
    CakeFileServices::MoveFileTo(*DestDir, FileName_, *FilePath_, OverwritePolicy, MissingParentPolicy) 
};

if (MoveResult.IsOkStrict())
{
    SetPath(FilePath_.CloneWithNewParent(DestDir));
}
return MoveResult;
```
### Error Handling Idioms

{: .note }
The following examples use `FCakeFileOpResult` as the result type; however, the exact same code will work for an `FCakeDirOpResult`. The only difference is that there will be different values possible for the `ErrorCode` member field.

The simplest error handling method is to simply use a result type as an implicit boolean via `operator bool`:


```cpp
FCakeFile ExampleFile{ FPaths::ProjectIntermediateDir() / TEXT("error_example.txt") };

if (!ExampleFile.CreateTextFile(TEXT("Some example text.")))
{
    UE_LOG(LogTemp, Error, TEXT("Failed creating example text file."));
}
```
This style is highly ergonomic when we don't need to worry about specific details of failure and just want to know whether or not an IO operation has succeeded.

When we do want to examine the error more closely, we can save it to a variable:

```cpp
FCakeFileOpResult CreateResult = ExampleFile.CreateTextFile(TEXT("Some example text."));

if (CreateResult.IsOk())
{
    UE_LOG(LogTemp, Warning, TEXT("Successfully created example text file."));
}
else
{
    UE_LOG(LogTemp, Error, TEXT("Failed creating example text file."))
}
```

We can also use scoped variable declaration to make things more compact:
```cpp
if (FCakeFileOpResult CreateResult = ExampleFile.CreateTextFile(TEXT("Some example text.")))
{
    
    UE_LOG(LogTemp, Warning, TEXT("Successfully created our example text file."));
}
else
{
    switch (CreateResult.ErrorCode)
    {
        case ECakeFileError::CFE_DestDirDoesNotExist:
            UE_LOG(LogTemp, Error, TEXT("The destination directory for our example file doesn't exist!"))
            break;
    }
}
```

### Human-Readable Strings
{% assign link_desc="CakeMixLibrary" %}
{% include rlinks/cakemix_native.md %} offers utility functions that can generate human-readable versions of both error codes and result types. 

Let's first take a look at how to get a human-readable string for an `FCakeDirOpResult`:
```cpp
FCakeDirOpResult DirOpResult{ FCakeDirOpResult::CouldNotReplace() };
```

We can use `DirErrorToString` to get the human-readable version of an `ECakeDirError` error code:
```cpp
FString ErrorCodeString = CakeMixLibrary::Results::DirErrorToString(DirOpResult.ErrorCode);
UE_LOG(LogTemp, Warning, TEXT("Error Code String (Dir): [%s]"), *ErrorCodeString);
```

We can alternatively use `DirOpResultToString` to get the human-readable version of the result type itself:

```cpp
FString ResultString = CakeMixLibrary::Results::DirOpResultToString(DirOpResult);
UE_LOG(LogTemp, Warning, TEXT("Result String (Dir): [%s]"), *ResultString);
```

{: .note }
The difference between an error code string and a result type string is minimal, the result type just includes the integer value of the error code as well to make it more debug friendly!

Finally, each result type has a `ToString` convenience member function that calls the appropriate CakeMixLibrary function:
```cpp
// The following code is equivalent to calling DirOpResultToString
UE_LOG(LogTemp, Warning, TEXT("To String (Dir): [%s]"), *DirOpResult.ToString());
```

For completeness, here are examples using both `FCakeFileOpResult` and `FCakeDirBatchResult`:

{: .note }
If these generic solutions do not have the formatting you desire, it is simple to write your own version of them! See the CakeMixLibrary's source code for the implementation details.


## Iteration Error Handling
{% assign bp_path="dir" %}
Just like IO operations, error handling for iterations is meant to be simple and opt-in. While there are slight differences in how we should handle errors based upon the iteration style being used, there is a common error reporting idiom that all iteration functions follow.

Let's look at an example with a Sequential iteration:

All iteration functions will send back at least two variables: a boolean indicating whether or not the iteration was successful (the definition of success will vary across iteration styles), and an enum outcome code that will contain more detailed context. 

When we just need to know whether or not an iteration was successful and we don't care about the context surrounding success / failure, we can simply branch on the boolean.

{% assign bp_file_id="itr-bool-sequential" %}
{% include components/blueprint_image.md %}
If, however, we want to do more robust error handling, we can switch on the outcome value and handle any specific outcomes we care about. 
{% assign bp_file_id="itr-outcome-sequential" %}
{% include components/blueprint_image.md %}

Handling either of these return values is entirely optional -- for quick and dirty scripts we can gleefully ignore all returned results returned and continue on our way.

The following sections will describe each iteration style and articulate any differences its error handling might require. 

### Sequential Iterations

### Guarded Iterations

### Search Iterations