## Introduction
{{ src_loc_group('Settings', 'CakeSettings')}}

CakeIO uses lightweight structs called Settings to group associated function parameters that are used across multiple functions. These structs help enforce regular argument ordering, reduce the length of function signatures, and provide a single location in source code where defaults can be set. Furthermore, because CakeIO takes advantage of C++20, we can use designated initializer syntax in order to allow for a much more ergonomic handling of optional parameters. 


## FCakeSettingsCreateItem
This parameter pack is utilized by various Create / Write IO functions across CakeIO. It contains two Cake Policies: [OverwriteItems](policies.md#overwriteitems) and [MissingParents](policies.md#missingparents). 

```c++
struct FCakeCreateItemSettings
{
	/** Determines if the new item can overwrite a prexisting item. */
	ECakePolicyOverwriteItems OverwritePolicy{ CakePolicies::OverwriteItemsDefault };

	/** Determines if any parent directories that don't exist in the destination path can be created. */
	ECakePolicyMissingParents MissingParentPolicy{ CakePolicies::MissingParentsDefault };
};
```

An example of explicitly setting policy values for an **FCakeCreateItemPolicies**:
```c++
const bool bCreateOK = FileText.CreateTextFile(SourceDataText,
    { 
        .OverwritePolicy     = ECakePolicyOverwriteItems::DoNotOverwriteExistingItems,
        .MissingParentPolicy = ECakePolicyMissingParents::CreateMissing
    }
);

if (!bCreateOK)
{
    UE_LOG(LogTemp, Error, TEXT("Failed creating example text file."));
}
```

## FCakeSettingsFileHandle
This settings struct contains two fields, one describing the read/write permissions for a file handle, and the other specifying how data should be written to the file. 

```c++
CAKEIO_API struct FCakeSettingsFileHandle
{
	ECakeFileOpenMode  OpenMode { ECakeFileOpenMode::Read           };
	ECakeFileWriteMode WriteMode{ ECakeFileWriteMode::OverwriteData };
};
```

### ECakeFileOpenMode
This enum determines how the file should be opened via the file handle.

{{ read_csv(open_csv_by_typename('ECakeFileOpenMode')) }}

### ECakeFileWriteMode
This enum determines how data should be written by the file handle.

{{ read_csv(open_csv_by_typename('ECakeFileWriteMode')) }}

When opening a file handle in read-only mode, the write mode is completely ignored. The easiest way to open a file handle this way is via designated initializer syntax:
```c++
	TUniquePtr<IFileHandle> ReadOnlyHandle{ 
		SrcOrc.OpenFileHandleUnique({ .OpenMode = ECakeFileOpenMode::Read })
	};
```

--8<-- "ad-designated-init.md"


## FCakeSettingsExtFilter
This settings struct is utilized by [filtered directory traversals](../directories.md#filtered-traversals). It contains two Cake Policies: [ExtFilterMode](../policies.md#extfiltermode) and [ExtMatchMode](../policies.md#extmatchmode). 

```c++
struct FCakeSettingsExtFilter
{
	ECakePolicyExtFilterMode FilterMode{ CakePolicies::ExtFilterModeDefault };
	ECakePolicyExtMatchMode  MatchMode { CakePolicies::ExtMatchModeDefault  };
};

```

## FCakeSettingsCopyItems
This settings struct is utilized by in various [CakeMixLibrary functions](../../advanced/cake-mix-library.md#copyingmoving-files-from-a-directory). It holds three Cake policies:

1. [OverwriteItems](policies.md#overwriteitems)
1. [ErrorHandling](policies.md#errorhandling)
1. [FileRelativeParents](policies.md#filerelativeparents)

For the ErrorHandling policy, if AbortOnError is selected, then the entire operation will be aborted immediately if any individual copy operation fails. 

Be sure to read the specifics about `FileRelativeParents`, which in essence determines whether or not the copied files will placed directly in the source directory or if their parent subdirectories should also be copied into the source directory (e.g., if copying "x:/game/data/save.dat" to "y:/archive" should copy to "y:/archive/save.dat" or "y:/archive/data/save.dat").

```c++
CAKEIO_API struct FCakeSettingsCopyItems
{
	ECakePolicyOverwriteItems      OverwritePolicy      { CakePolicies::OverwriteItemsDefault      };
	ECakePolicyErrorHandling       ErrorPolicy          { CakePolicies::ErrorHandlingDefault       };
	ECakePolicyFileRelativeParents RelativeParentPolicy { CakePolicies::FileRelativeParentsDefault };
};
```

## FCakeSettingsGatherSubdir
This settings struct is only used on CakeMixLibrary's [GatherCustomSubirs] function. It merely bundles an [ErrorHandling](policies.md#errorhandling) policy with an [ExtFilterClone](policies.md#extfilterclone) policy. The ErrorHandling policy is used to determine how the overall GatherCustom operation will react to errors, and the ExtFilterClone policy is forwarded to the internal traversal. This means that if the caller requests that the extension filter is cloned, each CakeDirectory object passed to the GatherCustom predicate will also have an extension filter identical to the source directory.

```c++
struct FCakeSettingsGatherSubdir
{
	ECakePolicyErrorHandling  ErrorPolicy         { CakePolicies::ErrorHandlingDefault  };
	ECakePolicyExtFilterClone ExtFilterClonePolicy{ CakePolicies::ExtFilterCloneDefault };
};
```

## FCakeSettingsDeleteItems
This is used by various directory deletion operations in [CakeMixLibrary](../../advanced/cake-mix-library.md#deleting-elements-from-a-directory). It combines a [DeleteFile](policies.md#deletefile) policy, which determines whether read-only files are allowed to be deleted and a [ErrorHandling](policies.md#errorhandling) policy, which determines whether the operation will halt if any delete operations fail.

```c++
struct FCakeSettingsDeleteItems
{
	ECakePolicyDeleteFile    DeleteFilePolicy{ CakePolicies::DeleteFileDefault    };
	ECakePolicyErrorHandling ErrorPolicy     { CakePolicies::ErrorHandlingDefault };
};
```

## FCakeSettingsAsyncTask
This struct is used whenever we launch an [async IO](../../advanced/async-io.md) task. It lets us customize the task priority, task flags, and which thread the completion callback should be called from.

```c++
struct FCakeSettingsAsyncTask 
{
	UE::Tasks::ETaskPriority Priority    { UE::Tasks::ETaskPriority::Normal              };
	UE::Tasks::ETaskFlags    TaskFlags   { UE::Tasks::ETaskFlags::DoNotRunInsideBusyWait };

	//...
};
```

!!! note
	The priority and task flags are types defined by Unreal Engine. ETaskPriority is defined in `Tasks.h`, and `ETaskFlags` is defined in `TaskPrivate.h`.

By default, the task priority will be normal and the flags indicate that the task should not be run in a busy-wait context. Considering these are all IO operations, it is difficult to imagine a scenario where a busy-wait context could be appropriate, but the option remains for callers to set their own flags. General advice here is to use the default settings and only consider changing them if profiling shows a benefit. 

The final member is of type `ECallbackThread`, which is a custom enum defined directly in the FCakeSettingsAsyncTask struct:

```c++
	enum struct ECallbackThread : uint8 
	{
		/** The completion callback should be called in the game thread. */
		CallbackInGameThread,

		/** The completion callback should be called in the thread used by the Async Task. */
		CallbackInAsyncThread
	};
```

Every Cake Async IO operation will require the caller to provide a callback that is invoked when the async IO operation has completed. We can choose to have the completion callback occur in the game thread or in the thread that the async IO operation was run in. 

```c++
struct FCakeSettingsAsyncTask 
{
	ECallbackThread CallbackThread{ ECallbackThread::CallbackInGameThread };
};
```

The default value is to call the completion callback in the game thread, as this can eliminate many complications that arise from callbacks being invoked on a different thread. We can freely update any Slate / Widget GUI without first waiting to return to the game thread, for instance. Use whichever callback style works best for your current context.

There are a variety of convenience static functions that create FCakeSettingsAsyncTask objects with various settings. It is not an exhaustive set of functions, but it covers some common settings you might desire:

```c++
static constexpr FCakeSettingsAsyncTask PriorityNormal_CallbackGameThread() 
{
	return FCakeSettingsAsyncTask(UE::Tasks::ETaskPriority::Normal, ECallbackThread::CallbackInGameThread);
}

static constexpr FCakeSettingsAsyncTask PriorityHigh_CallbackGameThread() 
{
	return FCakeSettingsAsyncTask(UE::Tasks::ETaskPriority::High, ECallbackThread::CallbackInGameThread);
}

static constexpr FCakeSettingsAsyncTask PriorityNormal_CallbackAsyncThread()
{
	return FCakeSettingsAsyncTask(UE::Tasks::ETaskPriority::Normal, ECallbackThread::CallbackInAsyncThread);
}

static constexpr FCakeSettingsAsyncTask PriorityHigh_CallbackAsyncThread() 
{
	return FCakeSettingsAsyncTask(UE::Tasks::ETaskPriority::High, ECallbackThread::CallbackInAsyncThread);
}
```
