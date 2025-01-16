## Introduction
{{ src_loc_group('Signals', 'CakeSignals')}}

Signals are a special enum type that are used by various operations that use callbacks. Signals are returned by the callbacks and allow the callbacks to influence the control flow of the associated operation.

## Directory Traversal Signals
These signals are used in [directory traversal](../directories.md#directory-traversal) operations.

### ECakeSignalGuarded
This signal is used to control guarded traversals.

{{ read_csv(open_csv_by_typename('ECakeSignalGuarded')) }}

### ECakeSignalSearch
This signal is used to control search traversals.

{{ read_csv(open_csv_by_typename('ECakeSignalSearch')) }}

## Advanced Signals
These are specialized signals used in higher level, advanced operations.

### ECakeSignalGather
This signal is used in the CakeMix [GatherCustom](../../advanced/cake-mix-library.md#gathercustom) family of functions.

{{ read_csv(open_csv_by_typename('ECakeSignalGather')) }}

### ECakeSignalBatchOp
This signal is used in the [CakeAsyncIO](../../advanced/async-io.md) exclusive [Batch Operation](../../advanced/async-io.md#batch-operations) functions.

{{ read_csv(open_csv_by_typename('ECakeSignalBatchOp')) }}