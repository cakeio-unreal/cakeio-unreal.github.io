## Advanced Result Types
--8<-- "note-native-only.md"
CakeMixLibrary provides powerful, high level functionality that is built on top of the CakeIO [core API](../core-api/api-overview.md). Because of this, it requires some more complex types to supply its callers with important context regarding its operations. 

## Mixed IO
IO operations that involve both directories and files are called **Mixed IO Operations**. These are usually operations that involve collecting or querying elements from a source directory. These **Mixed IO** operations are more difficult to consider from an error handling perspective, because we can have failure on multiple fronts. Because of this, we need new types that can hold more error information.

### FCakeResultMixedIO
This struct is very simple: it contains both an [FCakeResultDirIO](../core-api/special-types/results.md#fcakeresultdirio) result type and an [FCakeResultFileIO](../core-api/special-types/results.md#fcakeresultfileio) result type:

```c++
struct FCakeResultCompoundIO
{
	FCakeResultDirIO  DirResult  { FCakeResultDirIO::NoOp()  };
	FCakeResultFileIO FileResult { FCakeResultFileIO::NoOp() };
    //...
};
```

This result type is used by types that are returned from mixed IO operations. It offers a few convenience functions that should feel familiar to users of the individual result types:

`IsOk` and `IsOkStrict` simply return the conjunction of calling the same function on each individual result:
```c++
[[nodiscard]] FORCEINLINE bool IsOk() const
{
    return DirResult.IsOk() && FileResult.IsOk();
}

[[nodiscard]] FORCEINLINE bool IsOkStrict() const
{
    return DirResult.IsOkStrict() && FileResult.IsOkStrict();
}
```
`operator bool` behaves differently, however, because it is equivalent to `IsOkStrict` instead of `IsOk`. This is because with compound operations we want to see `Ok` instead of `NoOp`, since `NoOp` can imply failure. In many mixed IO operations, we are traversing a directory and performing operations on files. A `NoOp` in the `DirResult` member field often signals that the traversal failed to launch, and thus no IO operation was performed on the directory.

```c++
[[nodiscard]] FORCEINLINE operator bool() const
{
    return IsOkStrict();
}
```

We can check for individual errors with the convenience functions `HasDirError` and `HasFileError`, which are just equivalent to calling `!IsOkStrict()` on each result type:
```c++
[[nodiscard]] FORCEINLINE bool HasDirError() const
{
    return !DirResult.IsOkStrict();
}

[[nodiscard]] FORCEINLINE bool HasFileError() const
{
    return !FileResult.IsOkStrict();
}
```

Finally, two convenience functions exist that let us quickly set both result values to either `Ok` or `NoOp`:
```c++
FORCEINLINE void SetBothOk()
{
    DirResult  = FCakeResultDirIO::Ok();
    FileResult = FCakeResultFileIO::Ok();
}

FORCEINLINE void SetBothNoOp()
{
    DirResult  = FCakeResultDirIO::NoOp();
    FileResult = FCakeResultFileIO::NoOp();
}
```


### TCakeOrderMixedIO
This is a template alias version of [TCakeOrder](../core-api/special-types/orders.md) whose ResultType template argument is [FCakeResultMixedIO](#fcakeresultmixedio):

```c++
template<CakeConcepts::CNotPtrOrRef PayloadType>
using TCakeOrderMixedIO = TCakeOrder<FCakeResultMixedIO, PayloadType>;
```

## Reports
{{ src_loc_group('Reports', 'CakeReports')}}
Reports are a special type of type used to give callers more detailed context surrounding the outcome of an IO operation. 

### FCakeReportBatch
This report type is designed to convey extra context to IO operations involving groups of elements, such as copying multiple files. This is a simple type that has just three fields: one numeric field to indicate how many items were succesfully processed, one numeric field to indicate how many items failed in their IO operations, and a pointer to an array containing the list of all paths that failed their IO operations:


```c++
struct CAKEIO_API FCakeReportBatch
{
private:
	int32 ItemsSucceeded{ 0 };
	int32 ItemsFailed   { 0 };

	TSharedPtr<TArray<FCakePath>> FailedPaths{ nullptr };

public:
	/**@return The number of items that succeded in their IO operation. */
	FORCEINLINE int32 GetNumSucceeded() const { return ItemsSucceeded; }

	/**@return The number of items that failed in their IO operation. */
	FORCEINLINE int32 GetNumFailed()    const { return ItemsSucceeded; }

	/** @return Pointer to the container that holds the paths of items that failed their operation. WARNING: This pointer is INVALID if no errors are encountered. ALWAYS check that this is valid before dereferencing it! */ 
	FORCEINLINE const TSharedPtr<TArray<FCakePath>>& GetFailedPaths() const { return FailedPaths; }
    // ...
};
```
This snippet contains the core interface consumers of BatchReports will need. We can get the number of items that succeeded in their IO operation via `GetNumSucceeded`, and we can get the number of items that failed their IO operation via `GetNumFailed`. 
We can get access to the FailedPaths array shared pointer via `GetFailedPaths`. As the source documentation explains, this pointer is __invalid when no errors are encountered__. _Thus, it is vital that callers __always check the validity of the pointer before use__.

There are also two convenience functions that allow us to quickly check if any items succeeded or any items failed. `DidAnyWork` will return true if at least one item succeeded, and `AnyItemsFailed` will return true if at least one item failed:
```c++
/** @return True if ItemsSucceeded > 0, false otherwise. */
[[nodiscard]] FORCEINLINE bool DidAnyWork() const { return ItemsSucceeded > 0; }

/** @return True if ItemsFailed > 0, false otherwise. */
[[nodiscard]] FORCEINLINE bool AnyItemsFailed() const { return ItemsFailed > 0; }
```
#### Types Using FCakeReportBatch
There are two template aliases that use `FCakeReportBatch`, `FCakeorderBatchDir` and `FCakeOrderBatchMixedIO`:

```c++
template TCakeOrderDir<FCakeReportBatch>;
using FCakeOrderBatchDir = TCakeOrderDir<FCakeReportBatch>;

template TCakeOrderMixedIO<FCakeReportBatch>;
using FCakeOrderBatchMixedIO = TCakeOrderMixedIO<FCakeReportBatch>;
```
