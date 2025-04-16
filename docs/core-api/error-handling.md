## Introduction
One of the primary design goals of Cake IO is to provide enhanced error reporting from IO operations. Cake IO accomplishes this by using {{ link_outcomes('outcome types') }} which are defined for various types of IO operations. The following sections will showcase common usage patterns and idioms for error handling in Cake IO.

### Opt-In Error Handling
Exhaustive error handling is often complex and tedious, and there are many contexts in which exhaustive error handling is not actually necessary. Because Cake IO is intended for use in a variety of circumstances, from in-house editor tools to end-user interfaces, error handling has been designed so that callers are allowed to opt-in to the level of complexity that best suits their current context. There are three main levels of error complexity, ranging from simplest to most complex: **minimal**, **targeted**, and **exhaustive** error handling.

#### Minimal Error Handling
Minimal error handling views a particular IO operation outcome as a simple binary success or failure. This mirrors the original experience when using Unreal's built-in IO operations. In this strategy, we merely branch on a success flag and have two paths: one for the success state, and one for the error state.

#### Targeted Error Handling
While a particular IO operation might generate a large number of outcomes, there can be situations where a particular function is only equipped to handle a subset of those outcomes. In this strategy, we selectively target the possible outcome values that we want to handle.

#### Exhaustive Error Handling
As long as you know the complete list of outcomes a particular IO operation can generate, you can always implement exhaustive error handling whenever necessary. In this strategy, we provide a path for every possible outcome value a particular function can generate.

--8<-- "ad-error-map.md"

## File/Directory IO Error Handling Idioms
For our examples, we are going to use a [CakeFile](files.md) object. However, all of the idioms presented will work with [CakeDir](directories.md) objects. Only the possible outcome values will be different, since directory IO operations are distinct from file IO operations in Cake IO.

=== "C++"
    File/Directory IO operations will return either an {{ link_results('FCakeResultFileIO', 'fcakeresultfileio') }} or an {{ link_results('FCakeResultDirIO', 'fcakeresultdirio') }} result type, respectively. If you are unfamiliar with result types, please glance over those sections and refer to them as necessary when viewing the following idioms.

    The following examples will assume we have previously declared the following {{ link_cakefile() }} object:

    ```c++
	FCakeFile FileReadme{ FCakePath{ TEXTVIEW("X:/Game/readme.md")} };
    ```

    The simplest error handling method is to simply use a result type as an implicit boolean via `operator bool`:

    ```c++
	if (!FileReadme.CreateTextFile(TEXTVIEW("## Cake Battle Arena"))
	{
		UE_LOG(LogTemp, Error, TEXT("Failed creating the readme file."));
	}
    ```
    This style is highly ergonomic when we don't need to worry about specific details of failure and just want to know whether an IO operation has succeeded.

    When we do want to examine the error more closely, we can save it to a variable:

    ```c++
	FCakeResultFileIO ResultAppend{
		FileReadme.AppendTextFile(TEXTVIEW("Welcome to Cake Battle Arena."))
	};

	if (ResultAppend.IsOk())
	{
		UE_LOG(LogTemp, Warning, TEXT("Successfully appended text to the readme file!"))
	}
	else
	{
		UE_LOG(LogTemp, Error, TEXT("Failed appending text to file: [%s]"), *ResultAppend.ToString())
	}
    ```

    A few things to note here. First of all, the call to `IsOk` is equivalent to using `operator bool` on the result type. So we could also have used:

    ```c++
	if (ResultAppend)
	{
		UE_LOG(LogTemp, Warning, TEXT("Successfully appended text to the readme file!"))
	}
    ```
    Second, since we have stored the result type, we can use its `ToString` function to get better error reporting context, even though we aren't doing any specific error handling in our code. Storing the result can be valuable even when we aren't planning on directly examining the outcome value.

    Finally, since we're using `IsOk`, which is equivalent to `operator bool`, we can use scoped variable declaration for a more compact style:

    ```c++
	if (FCakeResultFileIO ResultAppend =
		FileReadme.AppendTextFile(TEXTVIEW("Welcome to Cake Battle Arena.")))
	{

		UE_LOG(LogTemp, Warning, TEXT("Successfully appended text to the readme file!"))
	}
	else 
	{
		UE_LOG(LogTemp, Error, TEXT("Failed appending text to file: [%s]"), *ResultAppend.ToString())
	}
    ```

    However, we need to keep in mind that this approach will only work if we plan to use `IsOk`. Let's consider our current IO operation: `AppendTextFile`. This function can return a `NoOp` in the situation where the string-like object we send to be appended is empty. In our particular scenario, this can't occur, and so we have no interest in checking for it. However, let's assume for a minute that we're accepting the append text data from an outside source. In this situation, we might be interested in checking for `NoOp`. 

	```c++
	FCakeResultFileIO ResultAppend{
		FileReadme.AppendTextFile(ExternalSourceTextData)
	};

	if (ResultAppend.IsOkStrict())
	{
		UE_LOG(LogTemp, Warning, TEXT("Successfully appended text to the readme file!"))
	}
	else
	{
		switch (ResultAppend.Outcome)
		{
		case ECakeOutcomeFileIO::NoOp:
			UE_LOG(LogTemp, Error, TEXT("The append text payload was empty! Please be sure to submit some text."))
			break;
		default:
			UE_LOG(LogTemp, Error, TEXT("Failed appending text to file: [%s]"), *ResultAppend.ToString())
			break;
		}
	}
	``` 
	!!! note
		If you need a refresher regarding the differences between `Ok` and `NoOp`, please see {{ link_outcomes('this section', 'ok-and-no-op') }}.

	Now we're leveraging the power of distinguishing between `Ok` and `NoOp`, as well as using targeted error handling. We recognize when the text that was submitted was empty, and so we can provide a specialized error message to better help the caller. However, if some other IO operation failed, we'll just use the same generic string report strategy as before. 

    !!! tip
        This is an example of how the {{ link_errormap() }} can help us achieve better error handling, even when we don't care about exhaustive error handling. 

    Finally, let's see what exhaustive error handling might look like:

    ```c++
	FCakeResultFileIO ResultAppend{
		FileReadme.AppendTextFile(ExternalSourceTextData)
	};

	if (ResultAppend.IsOkStrict())
	{
		UE_LOG(LogTemp, Warning, TEXT("Successfully appended text to the readme file!"))
	}
	else
	{
		switch (ResultAppend.Outcome)
		{
		case ECakeOutcomeFileIO::NoOp:
			UE_LOG(LogTemp, Error, 
				TEXT("The append text payload was empty! Please be sure to submit some text."))
			break;
		case ECakeOutcomeFileIO::DoesNotExist:
			UE_LOG(LogTemp, Error, 
				TEXT("The file we're attempting to append to doesn't exist, should we make it?"))
			break;
		case ECakeOutcomeFileIO::FailedOpenWrite:
			UE_LOG(LogTemp, Error, 
				TEXT("We couldn't open a write handle to this file, should we retry?"))
			break;
		case ECakeOutcomeFileIO::FailedWrite:
			UE_LOG(LogTemp, Error, 
				TEXT("We opened a valid write handle but the write operation failed, should we retry?"))
			break;
		default:
			UE_LOG(LogTemp, Error, 
				TEXT("Unexpected append error occurred: "), *ResultAppend.ToString())
			break;
		}
	}
    ```

    Exhaustive error handling will usually require referencing the appropriate [error map](../core-api/error-maps/#appendfile-text-binary) unless you have a great memory or choose to delve into the implementation source code.
    For the sake of example we are just logging out the error, but we can easily imagine putting more robust error handling logic in each switch case.

=== "Blueprint"
	Any IO operation will always return at least two variables related to the IO operation: a boolean to indicate whether the operation succeeded or failed as a whole, and an outcome value that identifies the exact outcome that the operation generated. For CakeFile IO operations, the outcome value we get back is of type {{ link_outcomes('ECakeOutcomeFileIO', 'ecakeoutcomefileio') }}. For CakeDir IO operations, the outcome value we get back is of type {{ link_outcomes('ECakeOutcomeDirIO', 'ecakeoutcomedirio') }}.

	It is important to understand that the bool will return true if the outcome is either `Ok` OR `NoOp`. If you are unfamiliar with the differences, please see {{ link_outcomes('this section', 'ok-and-no-op') }}. 

    The following examples will assume we have previously declared the following [CakeFile](files.md) object:

	{{ bp_img_error_handling('Example Readme File') }}

	Let's start with an example of minimal error handling. In this approach, we branch on the bool value that indicates whether or not the operation succeeded / failed: 

	{{ bp_img_error_handling('Minimal Error Handling IO') }}

	This style is ergonomic and ideal for situations where we don't actually care about the specific details regarding failure, but still want to know whether the operation succeeded or failed.

	Using the outcome value returned by an IO operation will give us greater context and the ability to implement more refined error handling. Even when using the simple branch technique described above, we can use a [CakeMixLibrary](/core-api/cake-mix/#error-handling) utility function to get a human-readable string of the outcome when it fails, giving any readers a better understanding of the actual point of failure:

	{{ bp_img_error_handling('Minimal Error Handling IO To String') }}

	The bool `Op Ok` is true if the outcome is `Ok` or `NoOp`, false otherwise. In some situations, we might want to distinguish between those `Ok` and `NoOp`. for instance, since we are using the AppendTextFile interface, a `NoOp` can be generated whenever it is submitted an empty string to append to a file. Since there is nothing to append, the IO operation will be skipped entirely. Since this is not technically an error from the API's standpoint, it is up to the caller to decide what to do. 
	
	Let's imagine that we are accepting input from an outside source, like a GUI. At this point, we can't be certain that the string being sent to AppendTextFile is non-empty, and it would be good to know when it is empty. Since now we are interested in distinguishing between `Ok` and `NoOp`, but we still don't care about handling all potential outcome values, we will be using the targeted error handling approach. 

	To do this, we'll still branch on the bool value, knowing that it will be true if the result is `Ok` or `NoOp`, and false otherwise. When it's false, we'll still just print the generic error message to the user. When it's true, however, we'll switch on the outcome and provide two new paths: one for `Ok` and one for `NoOp`.

	Now we can more accurately report the outcome to our users. Below is the same Blueprint script, zoomed into the error handling part specifically:

	{{ bp_img_error_handling('Targeted Error Handling IO') }}

	Finally, let's take a look at the final strategy: exhaustive error handling. Exhaustive error handling will usually require referencing the appropriate [error map](/core-api/error-maps/#appendfile-text-binary) unless you have a great memory or choose to delve into the implementation source code. This time we'll ignore the bool value entirely and just switch on the outcome value, handling every potential outcome value that AppendTextFile can send us. To keep the example simple, we'll just print a string for each outcome, but we can imagine that each of these print string nodes could instead be replaced with more complex, appropriate error handling:

	{{ bp_img_error_handling('Exhaustive Error Handling IO') }}

	As we can see, exhaustive error handling greatly increases the complexity of our code. Strive to choose the minimum complexity required by a given context. 


And that concludes our tour through error handling with file and directory IO operations. Remember, the level of complexity for error handling depends entirely upon your use case. 

## Traversal Error Handling Idioms
--8<-- "ad-traversal.md"

For this section we'll use a search traversal since it is the most complex kind of traversal. Any idioms shown here will work with the other kinds of traversal, but they will just be simpler and have less options.

For our search, our goal is to collect three text files from a given directory. 

=== "C++"
    For our example, we are going to assume the following directory is declared: 

    ```c++
	FCakeDir DesignDocsDir{ FCakePath{TEXTVIEW("X:/cake-arena/design-docs")}, TEXTVIEW("txt") };
    ```

    Furthermore, we are also going to assume the following variables and our search callback are declared as:

    ```c++
	constexpr int32 DesiredFileCount{ 3 };

	TArray<FCakeFile> Files{};
	Files.Reserve(DesiredFileCount);

	auto FindThreeTextFiles =
		[&Files, CurrentCount = int32{ 0 }](FCakeFile NextFile) mutable -> ECakeSignalSearch 
	{
		Files.Emplace(MoveTemp(NextFile));
		++CurrentCount;
		if (CurrentCount >= DesiredFileCount) { return ECakeSignalSearch::Success; }
		return ECakeSignalSearch::Continue;
	};
    ```

	First we'll let the result implicitly convert to `bool` via its `operator bool`. [FCakeResultSearch](special-types/results.md#fcakeresultsearch) only is true if the search was successful, so we can branch on it and then safely use our expected files:

	```c++
	if (DesignDocsDir.TraverseSearchFilesWithFilter(ECakePolicyOpDepth::Deep, FindThreeTextFiles))
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't get three files. Found [%d] file(s)."), Files.Num())
	}
	```

	Since we didn't store the result type, we can't be sure of what exactly happened with the traversal -- it could have failed to launch or the search itself could have failed. We know it wouldn't have aborted due to an error since we don't have an abort branch in our search callback.

	Let's try storing the result type returned by our traverse operation.

	```c++
	FCakeResultSearch ResultSearch{
		DesignDocsDir.TraverseSearchFilesWithFilter(ECakePolicyOpDepth::Deep, FindThreeTextFiles)
	};

	if (ResultSearch.WasSuccessful())
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't find necessary files: [%s]."), *ResultSearch.ToString())
	}
	```

	Now that we have stored the result type, we can use its `ToString` function to help give the caller better insight into how the search traversal failed.

	Calling `WasSuccessful` is equivalent to using `operator bool`, so we could also use this equivalent form when checking for search success: 

	```c++
	if (ResultSearch)
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	```

    Since `WasSuccessful` and `operator bool` are equivalent, we can always use scoped variable declaration for a more compact style if we prefer:

	```c++
	if (FCakeResultSearch ResultSearch = 
		DesignDocsDir.TraverseSearchFilesWithFilter(ECakePolicyOpDepth::Deep, FindThreeTextFiles))
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	else
	{
		UE_LOG(LogTemp, Warning, TEXT("Couldn't find necessary files: [%s]."), *ResultSearch.ToString())
	}
	```


	It can be beneficial to distinguish between a search failure and the search traversal error states. Let's change our error handling so we know when the search fails, and thus can also identify when the traversal operation itself fails to launch.

	```c++
	if (FCakeResultSearch ResultSearch = 
		DesignDocsDir.TraverseSearchFilesWithFilter(ECakePolicyOpDepth::Deep, FindThreeTextFiles))
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	else
	{
		switch (ResultSearch.Outcome)
		{
		case ECakeOutcomeSearch::Failed:
			UE_LOG(LogTemp, Warning, 
				TEXT("The target directory does not have at least [%d] text file(s)!"), DesiredFileCount)
			break;
		default:
			UE_LOG(LogTemp, Warning, TEXT("Traversal error: [%s]"), *ResultSearch.ToString())
			break;
		}
	}
	```
	And, for completeness, we can always exhaustively handle every possible outcome:

	```c++
	if (FCakeResultSearch ResultSearch = 
		DesignDocsDir.TraverseSearchFilesWithFilter(ECakePolicyOpDepth::Deep, FindThreeTextFiles))
	{
		// We have the three files.
		check(Files.Num() == 3);
	}
	else
	{
		switch (ResultSearch.Outcome)
		{
		case ECakeOutcomeSearch::Failed:
			UE_LOG(LogTemp, Warning, 
				TEXT("The target directory does not have at least [%d] text file(s)!"), DesiredFileCount)
			break;
		case ECakeOutcomeSearch::DidNotLaunch:
			UE_LOG(LogTemp, Warning, TEXT("The traversal failed to launch."))
			break;
		case ECakeOutcomeSearch::Aborted:
			UE_LOG(LogTemp, Warning, TEXT("The traversal was aborted due to an error."))
			break;
		}
	}
	```

	The case statement for `Aborted` is useless in our scenario since we don't actually return it, but we have included it for completeness. 

=== "Blueprint"
    For our example, we are going to assume the following directory is declared: 

	{{ bp_img_error_handling('Design Doc Dir') }}

	This is the callback we will be using to gather the first three text files found in the target directory:

	{{ bp_img_error_handling('Search Callback Definition') }}

	First, let's look at a minimal error handling example. The bool returned by a search traversal is only true if the search was successful. Since we're trying to gather three text files, we can be certain that a true value for this outcome means we did indeed gather three text files from the target directory.

	{{ bp_img_error_handling('Minimal Error Handling Search') }}

	Just like with CakeFile / CakeDir IO operations, we can use a utility function from [CakeMixLibrary]/core-api/cake-mix/#error-handling) to get a human-readable string of the outcome:

	{{ bp_img_error_handling('Minimal Error Handling Search To String') }}

	By using the minimal error handling approach, we have lost some information. Namely, when a search does not succeed, we can't distinguish between a search failure (the directory doesn't meet the search requirements, i.e., it doesn't have at least three text files in our case) and a traversal error. Search traversal can abort due to IO errors, and furthermore all traversal operations can [fail to launch](special-types/outcomes.md#did-not-launch). 
	
	We'll start by using targeted error handling to allow us to easily distinguish between search failure and error results. First, we will switch on the search outcome value, providing special paths for success and failure. Then we will route the remaining paths back to the generic string error report we used in the prior example:

	{{ bp_img_error_handling('Targeted Error Handling Search') }}


	Finally, we can always use exhaustive error handling and provide an exclusive path for every possible outcome value. In our situation, our callback never returns an Abort signal, so this error path technically doesn't need to be handled. However, we will show a full handling of the outcomes for completeness, and as a reference for those callbacks that do return Abort signals:

	{{ bp_img_error_handling('Exhaustive Error Handling Search') }}

And that concludes a tour of error handling with a search traversal. Remember, the same strategies work for Unguarded and Guarded traversals, but you just have fewer outcome values to deal with since the traversal operations themselves are simpler.