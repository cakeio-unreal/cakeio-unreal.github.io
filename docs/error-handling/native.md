---
title: Native
parent: Error Handling
nav_order: 1
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

{% include common_ad_error_map.md %}

### FCakeDirBatchResult
{% assign in_source="CakeDirBatchResult" %}
{% include components/source_info_ex.html %}

**FCakeDirBatchResult** is a special result type used for compound directory operations, or directory operations that involve multiple IO operations. An example of a compound directory operation would be one that copies multiple files from one directory to another. **FCakeDirBatchResult** has two member fields: an **FCakeDirOpResult** that records the final result of the entire compound operation, and an integer member field that records the number of individual IO operations that successfully completed:
```cpp
FCakeDirBatchResult BatchResult{};

FCakeDirOpResult FinalResult = BatchResult.OpResult;
int32 NumOperationsCompleted = BatchResult.ItemsProcessed;
```
The generic `ItemsProcessed` field needs to be interpreted based on the context of the compound operation; e.g., if the compound operation involves deleting files, then items processed represents the number of files successfully deleted; if it involves moving files, then the number of files successfully moved, and so on.

There are some convenience functions that mirror the API of `FCakeDirOpResult`:
```cpp
if (BatchResult)
{
    // Same as if (BatchResult.OpResult)
}

if (BatchResult.IsOk())
{
    // Same as if (BatchResult.OpResult.IsOk())
}

if (BatchResult.IsOkStrict())
{
    // Same as if (BatchResult.OpResult.IsOkStrict())
}
```
These are the equivalent of calling the same functions on BatchResult.OpResult.

Finally, there is one extra function unique to **FCakeDirBatchResult**. We can use `DidAnyWOrk` to find out if `ItemsProcessed` has a value greater than 0:
```cpp
if (BatchResult.DidAnyWork())
{
    // We reach this branch when BatchResult.ItemsProcessed > 0
}
```



As of now, **CakeMixLibrary** is the only official source location that uses them, so let's take a look at an example using `DeleteFilesWithFilter`:

```cpp
FCakeDir DirGame{ TEXT("/x/game/data/"), TEXT("json|bin")};

BatchResult = CakeMixLibrary::Dir::DeleteFilesWithFilter(DirGame, ECakePolicyOpDepth::Shallow);

if (BatchResult.DidAnyWork())
{
    UE_LOG(LogTemp, Warning, 
        TEXT("Deleted [%d] file(s) from [%s]."), BatchResult.ItemsProcessed, *DirGame.GetDirName()
    );
}
else
{
    if (!BatchResult)
    {
        UE_LOG(LogTemp, Error, TEXT("Failed deleting files: [%s]"), *BatchResult.ToString());
    }
    else
    {
        UE_LOG(LogTemp, Warning, TEXT("No matching files to delete!"));
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

```cpp
// --- FCakeFileOpResult Human-Readable Strings
FCakeFileOpResult FileOpResult{ FCakeFileOpResult::FailedOpenRW() };

ErrorCodeString = CakeMixLibrary::Results::FileErrorToString(FileOpResult.ErrorCode);
UE_LOG(LogTemp, Warning, TEXT("Error Code String (File): [%s]"), *ErrorCodeString);

ResultString = CakeMixLibrary::Results::FileOpResultToString(FileOpResult);
UE_LOG(LogTemp, Warning, TEXT("Result String (File): [%s]"), *ResultString);

UE_LOG(LogTemp, Warning, TEXT("To String (File): [%s]"), *FileOpResult.ToString());

// --- FCakeDirBatchResult Human-Readable Strings
FCakeDirBatchResult BatchOpResult{ FCakeDirOpResult::CouldNotReplace() };
ErrorCodeString = CakeMixLibrary::Results::DirErrorToString(BatchOpResult.OpResult.ErrorCode);
UE_LOG(LogTemp, Warning, TEXT("Error Code String (Batch): [%s]"), *ErrorCodeString);

ResultString = CakeMixLibrary::Results::DirOpResultToString(BatchOpResult.OpResult);
UE_LOG(LogTemp, Warning, TEXT("Result String (Batch): [%s]"), *ResultString);

UE_LOG(LogTemp, Warning, TEXT("To String (Batch): [%s]"), *BatchOpResult.ToString());
```

{: .note }
If these generic solutions do not have the formatting you desire, it is simple to write your own version of them! See the CakeMixLibrary's source code for the implementation details.


## Iteration Error Handling
Just like file and directory IO operations, directory iterations return result types that wrap a code value. These code values are called outcomes because the represent the final outcome of a particular iteration. There are two result types: `FCakeDirIterationResult` and `FCakeDirSearchResult`. 

{% assign subsec_link="directory-iteration" %}
{% assign link_desc="this section first" %}
{: .note }
This section is only dedicated to discussing error handling with directory iteration. If you are unfamiliar with directory iteration via **FCakeDir**, please read {% include rlinks/cakedir_native.md %}.

### Failure to Launch
{% include common_failure_to_launch.md %}
### FCakeDirIterationResult
{% assign in_source="CakeDirIterationOutcome|CakeDirIterationResult" %}
{% include components/source_info_ex.html %}
This result type is returned from two iteration styles: Sequential and Guarded. This result type wraps an `ECakeDirIterationOutcome` which only has three values: **DidNotLaunch**, **Completed**, or **Aborted**.

```cpp
FCakeDirIterationResult ExampleItrResult{ FCakeDirIterationResult::Completed() };
ECakeDirIterationOutcome ExampleItrOutcome = ExampleItrResult.Outcome;
```

**FCakeDirIterationResult** has a few utility functions to help us quickly assess the outcome of an iteration:

```cpp
FCakeDir IntDir{ FPaths::ProjectIntermediateDir() };

FCakeDirIterationResult ItrResult = IntDir.IterateFiles(
    ECakePolicyOpDepth::Shallow,
    [](FCakeFile InFile) -> void
    {
        
    }
);
```

We can check to see if the iteration completed successfully via `WasCompleted`:
```cpp
if (ItrResult.WasCompleted())
{
    UE_LOG(LogTemp, Warning, TEXT("Iteration completed successfully."))
}
```

We can use `operator bool` instead which is equivalent to a call of `WasCompleted`:

```cpp
if (ItrResult)
{
    UE_LOG(LogTemp, Warning, TEXT("Iteration completed successfully."))
}
```

We can check to see if the iteration was aborted via `WasAborted`:

```cpp
if (ItrResult.WasAborted())
{
    UE_LOG(LogTemp, Warning, TEXT("Iteration was aborted."))
}
```

And we can check to see if the iteration failed to start via `WasNotLaunched`:
```cpp
if (ItrResult.WasNotLaunched())
{
    UE_LOG(LogTemp, Warning, TEXT("Iteration did not start."))
}
```
Finally, if we want to easily get a human-readable string describing the outcome, we can use the convenience member function `ToString`:

```cpp
UE_LOG(LogTemp, Warning, TEXT("The iteration result is: %s"), *ItrResult.ToString());
```
### FCakeDirSearchResult
{% assign in_source="CakeDirSearchOutcome|CakeDirSearchResult" %}
{% include components/source_info_ex.html %}
This result type is returned only from search iterations. **FCakeDirSearchResult** wraps an `ECakeDirSearchOutcome` which has four values: **DidNotLaunch**, **Succeeded**, **Failed**, or **Aborted**.

```cpp
FCakeDirSearchResult ExampleResult{ FCakeDirSearchResult::Succeeded() };
ECakeDirSearchOutcome ExampleOutcome = ExampleResult.Outcome;
```

**FCakeDirSearchResult** also has utility functions to help us quickly assess the outcome of an search:

```cpp
FCakeDir IntDir{ FPaths::ProjectIntermediateDir() };

FCakeDirSearchResult SearchResult = IntDir.IterateSearchFiles(
    ECakePolicyOpDepth::Shallow,
    [](FCakeFile InFile) -> ECakeDirSearchSignal
    {
        return ECakeDirSearchSignal::DSS_Complete;
    }
);
```

We can check to see if the search was successful via `WasSuccessful`:
```cpp
if (SearchResult.WasSuccessful())
{
    UE_LOG(LogTemp, Warning, TEXT("Search Iteration completed successfully."))
}
```

We can use `operator bool` instead which is equivalent to a call of `WasSuccessful`:

```cpp
if (SearchResult)
{
    UE_LOG(LogTemp, Warning, TEXT("Search Iteration completed successfully."))
}
```

We can check to see if the search failed via `WasFailure`:

```cpp
if (SearchResult.WasFailure())
{
    UE_LOG(LogTemp, Warning, TEXT("Search Iteration failed."))
}
```

We can check to see if the search was aborted via `WasAborted`:
```cpp
if (SearchResult.WasAborted())
{
    UE_LOG(LogTemp, Warning, TEXT("Search Iteration aborted."))
}
```

And we can check to see if the search failed to start via `WasNotLaunched`:
```cpp
if (SearchResult.WasNotLaunched())
{
    UE_LOG(LogTemp, Warning, TEXT("Search Iteration did not start."))
}
```

Finally, if we want to easily get a human-readable string describing the search outcome, we can use the convenience member function `ToString`:

```cpp
UE_LOG(LogTemp, Warning, TEXT("Search Result ToString: %s"), *SearchResult.ToString())
```
### Human-Readable Strings
{% assign link_desc="CakeMixLibrary" %}
{% include rlinks/cakemix_native.md %} offers utility functions that can generate human-readable versions of both outcome codes and result types. The following examples show all ways we can get human-readable strings from the iteration outcome types. 

{: .note }
The result type's `ToString` member function is the equivalent of calling CakeMixLibrary's `Dir<Type>ResultToString`.

```cpp
auto FakeSearchResult{ FCakeDirSearchResult::Succeeded() };

// --- DirSearchOutcomeToString 
FString OutcomeString{ CakeMixLibrary::Results::DirSearchOutcomeToString(FakeSearchResult.Outcome) };
UE_LOG(LogTemp, Warning, TEXT("Outcome string (Search): [%s]"), *OutcomeString);

// --- DirSearchResultToString 
FString ResultString{ CakeMixLibrary::Results::DirSearchResultToString(FakeSearchResult) };
UE_LOG(LogTemp, Warning, TEXT("Result string (Search): [%s]"), *OutcomeString);

// --- ToString (Search)
UE_LOG(LogTemp, Warning, TEXT("ToString (Search): [%s]"), *FakeSearchResult.ToString())


auto FakeIterationResult{ FCakeDirIterationResult::Completed() };

// --- DirIterationOutcomeToString 
OutcomeString = CakeMixLibrary::Results::DirIterationOutcomeToString(FakeIterationResult.Outcome);
UE_LOG(LogTemp, Warning, TEXT("Outcome string (Iteration): [%s]"), *OutcomeString);

// --- DirIterationResultToString 
ResultString = CakeMixLibrary::Results::DirIterationResultToString(FakeIterationResult);
UE_LOG(LogTemp, Warning, TEXT("Result string (Iteration): [%s]"), *OutcomeString);

// --- ToString (Iteration)
UE_LOG(LogTemp, Warning, TEXT("ToString (Iteration): [%s]"), *FakeIterationResult.ToString())
```

{: .note }
If these generic solutions do not have the formatting you desire, it is simple to write your own version of them! See the CakeMixLibrary's source code for the implementation details.
