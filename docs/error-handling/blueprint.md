---
title: Blueprint
parent: Error Handling
nav_order: 2
---

{% assign bp_path="error-handling" %}

{% assign header_parent="Result" %}
## Error Handling
{% include components/default_toc.md %}

## Introduction
**CakeIO** introduces a variety of custom types that indicate the outcome of IO operations or directory iteration. Though each type has some unique properties, they all follow a common design pattern. The error handling in CakeIO was designed to be an opt-in experience for the callers -- they are in control of how complicated they wish their error handling to be. Results from an operation can be entirely ignored, viewed as a success/fail binary outcome via a boolean, or viewed through an outcome/error code that gives detailed context surrounding failing operations.

To that end, we will see a familiar pattern no matter what operation we are trying to achieve -- the function will return back both a boolean that indicates generic success or failure, and it will also send us back an enum type whose value will map to specific outcome/error contexts. 

We'll start by examining how we can handle and understand IO operations involving files and directories, and then we will look at error handling with directory iteration.

## File and Directory Error Handling
{% assign in_source="CakeFileError|CakeDirError" %}
{% include components/source_info_ex.html %}
File and directory error handling is very similar, and so we'll look at them together. Any file IO operation will return a boolean that indicates generically whether the operation succeeded, and an `ECakeFileError` enum value that gives specific context about how the operation succeeded or failed:
{% assign bp_file_id="file-result-example" %}
{% include components/blueprint_image.md %}

Likewise, any directory IO operation will return a boolean indicating general success or failure and an `ECakeDirError` enum value that gives greater context:
{% assign bp_file_id="dir-result-example" %}
{% include components/blueprint_image.md %}


So we can see the only difference between an IO operation for a file or directory is the error code type that is returned.


### OK and NOP
While file and directory operations each have their own dedicated error code type, they share two values that have the exact same meaning: `OK` and `NOP`. It is important to understand the difference between these two errors.

> **OK**: The IO operation was executed and encountered no errors.

> **NOP**: The IO operation was not necessary and was not executed.

An example of a situation that might generate a **NOP** is when we attempt to delete a file or directory that doesn't exist. The benefit of distinguishing between **OK** and **NOP** is that we can know whether or not an IO operation actually occurred and work was done. 

In many scenarios, callers likely won't care to distinguish between **OK** and **NOP**, since either error value means that the file system is in the desired state after the operation resolved. That is why the boolean returned by an IO operation will be true if the value is **OK** _or_ **NOP**. 
{% assign bp_file_id="ok-bool" %}
{% include components/blueprint_image.md %}

In situations where we only want to do something if an IO operation actually occurred, we will need to switch on the error code and only proceed if it is `OK`:
{% assign bp_file_id="ok-strict" %}
{% include components/blueprint_image.md %}

For a pragmatic example of when we might care about distinguishing between OK and NOP, we can look to the `MoveFile` implementation. A `UCakeFile` needs to update its path information when it is moved, but it should only update that path information when a move actually succeeds. It is possible (though likely rare) that the destination directory was the same as the file's current directory, which would result in a NOP. In this situation, we need to be sure that the IO operation occurred, and so this is a scenario where we only need to perform logic on an `OK` return value. 

### Error Handling Idioms
{: .note }
The following examples uses a directory operation; however, the exact same approach will work for file operations. The only difference is that there will be different values possible for the returned `ErrorCode`.

By far the simplest way to handle errors is to ignore them altogether. However, as you might imagine, this isn't recommended! But it's still an option, and might make sense when you are just trying to get something to work very quickly:
{% assign bp_file_id="idiom-io-ignore" %}
{% include components/blueprint_image.md %}

There are many situations where we might not care exactly how an IO operation, but just want to know whether or not it succeeded in doing its job. For this, we can easily branch on the boolean returned by our IO operation. Remember, this will be true if the operation returns `OK` or `NOP`, so it doesn't guarantee that the operation occurred, it just guarantees the filesystem is in the state you expect after the call.
{% assign bp_file_id="idiom-io-bool" %}
{% include components/blueprint_image.md %}

{: .note }
This generic error handling approach is much more ergonomic for things like editor tools and scripts where the nuances of IO errors are less important.

Finally, we can use the error code itself to handle any potential outcomes that we deem necessary:
{% assign bp_file_id="idiom-io-error-code" %}
{% include components/blueprint_image.md %}

And that's all there is to handling IO operations. As you can see, error handling can be as comprehensive as you desire. CakeIO strives to give developers the freedom to balance their error handling complexity around their own particular needs. 

{% include common_ad_error_map.md %}

### Human-Readable Strings
{% assign link_desc="CakeMixLibrary" %}
Sometimes we might want to display error codes as a human-readable string. 
{% include rlinks/cakemix_blueprint.md %} offers utility functions that allow us to do this easily. Depending on the error code type, we simply need to use either `GetCakeDirErrorAsString` or `GetCakeFileErrorAsString`:
{% assign bp_file_id="ec-string-dir" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="ec-string-file" %}
{% include components/blueprint_image.md %}

## Iteration Error Handling
{% assign bp_path="dir" %}
Just like IO operations, error handling for iterations is meant to be simple and opt-in. While there are slight differences in how we should handle errors based upon the iteration style being used, there is a common error reporting idiom that all iteration functions follow.

Let's look at an example with a Sequential iteration:

Just like IO operations, all iteration functions will send back at least two variables: a boolean indicating whether or not the iteration was successful (the definition of success will vary across iteration styles), and an enum outcome code that will contain more detailed context. 

When we just need to know whether or not an iteration was successful and we don't care about the context surrounding success / failure, we can simply branch on the boolean.

{% assign bp_file_id="itr-bool-sequential" %}
{% include components/blueprint_image.md %}
If, however, we want to do more robust error handling, we can switch on the outcome value and handle any specific outcomes we care about. 
{% assign bp_file_id="itr-outcome-sequential" %}
{% include components/blueprint_image.md %}

Handling either of these return values is entirely optional -- for quick and dirty scripts we can gleefully ignore all returned results returned and continue on our way.

Before we look at each iteration style and its potential outcomes, we need to first learn about the outcome value that is shared across all iteration styles.

### Failure to Launch
{% include common_failure_to_launch.md %}

With that common value now explained, let's look into the unique differences that each iteration style has in relation to outcomes.

{% assign bp_path="error-handling" %}
### Sequential Iterations
**Sequential** iterations use the `ECakeDirIterationOutcome` type to represent their outcomes:
{% assign bp_file_id="itr-ec-seq" %}
{% include components/blueprint_image.md %}
As we can see, there are three outcome values possible: **DidNotLaunch**, **Completed**, and **Aborted**.
**Sequential** iterations are the simplest iteration type -- once launched, they will visit every target element in the source directory. They cannot be stopped until all elements have been visited; and because of this, the **Aborted** outcome does not apply. A **Sequential** iteration will either launch and be completed, or it will fail to launch. Thus, we can interpret the boolean value roughly as "did or didn't launch":
{% assign bp_file_id="itr-bool-seq" %}
{% include components/blueprint_image.md %}

And that's all there is to handling outcomes from **Sequential** iterations.

### Guarded Iterations
**Guarded** iterations also use the `ECakeDirIterationOutcome` type to represent their outcomes, only this time the **Aborted** value can also be sent back:
{% assign bp_file_id="itr-ec-guard" %}
{% include components/blueprint_image.md %}

Whenever a **Guarded** iteration callback sends the signal **Abort**, the final outcome for that iteration will be **Aborted**. Since the callback determines what is or isn't worth aborting over, it will need to record additional context on its own (e.g., send out a log). From our perspective, we simply know that some error was encountered and the iteration did not fully complete. 

The boolean return value implies more than its **Sequential** counterpart; we can interpret this boolean as either the iteration failed to launch OR the iteration was aborted early. 
{% assign bp_file_id="itr-ec-guard" %}
{% include components/blueprint_image.md %}

Since it can indicate more than one outcome, the boolean represents a loss of information; as long as we only care whether or not the iteration completed, that should be an acceptable loss.
{% assign bp_file_id="itr-bool-guard" %}
{% include components/blueprint_image.md %}

And that concludes our tour of **Guarded** iteration error handling, let's move on to **Search** iterations!

### Search Iterations
**Search** iteration outcomes use the outcome type `ECakeDirSearchOutcome`. Since **Search** iterations are the most complex type of iteration, it is fitting they have a unique outcome type. However, complexity is relative, and the good news is that **Search** iteration outcomes are still quite straightforward and simple.

{% assign bp_file_id="itr-ec-search" %}
{% include components/blueprint_image.md %}

Failure to launch is an expected outcome type, and **Aborted** is just like a **Guarded** iteration: it will be returned whenever an **Abort** signal is sent from a **Search** iteration callback. The new values are **Succeeeded** and **Failed**. Recall that a **Search** iteration expects its associated callback to have a defined goal; **Succeeded** is the outcome that will be returned when the **Complete** signal is sent from a search callback. If, however, all elements are visited (the iteration is exhausted) and the search callback has never sent a **Complete** signal, the entire **Search** iteration is considered a failure and will be assigned the outcome **Failed**.

When we use the boolean returned by a **Search** iteration, we need to understand its implications. Just like a **Guarded** iteration, the boolean represents a loss of information. In the case of a **Search** iteration, the boolean will only be true if the outcome is **Succeeded**. This means that a false value can mean that either the iteration didn't launch OR the iteration was aborted OR the search was a failure. Because using the boolean from a **Search** iteration represents the greatest loss of information, be sure you understand the costs before using it. When the losses are deemed acceptable it can produce more ergonomic code.

{% assign bp_file_id="itr-bool-search" %}
{% include components/blueprint_image.md %}

And that's all there is to handling **Search** iterations. We'll close out this section by seeing how we can get human-readable strings for our iteration outcomes.

### Human-Readable Strings
Just like the error codes for file and directory operations, we can easily get a human-readable string for our iteration outcomes via utility functions from CakeMixLibrary. Depending on the outcome type, we either use `GetDirIterationOutcomeAsString` or `GetDirSearchOutcomeAsString`:
{% assign bp_file_id="ec-string-itr" %}
{% include components/blueprint_image.md %}

{% assign bp_file_id="ec-string-search" %}
{% include components/blueprint_image.md %}