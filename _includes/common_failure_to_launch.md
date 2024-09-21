
All iteration outcomes share a common value to indicate that an iteration failed to start. As of now, this is `DidNotLaunch`. It is important to understand the contexts that can cause an iteration to fail to start:

1. **The source directory does not exist.**
When an iteration is called on a directory object, that iteration process will ensure that the directory it represents actually exists on the filesystem. If it does not, the iteration will not proceed.

2. **A {% glossary filtered_iteration, display: filtered iteration %} is called on a directory object when its extension filter is empty.** 
This will visit files in a way that the caller does not expect, and so the iteration will not proceed.

3. **A policy argument with an out of range value was submitted.**
All CakeIO policies are enums, so out of range issues should be quite rare. The only way these are able to occur is if one is casting integer values to the policy type; if you are doing this, be extremely careful! 

{: .hint }
If CakeIO logging is enabled, it will describe the error that prevented the iteration from launching.