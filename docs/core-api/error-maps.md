## CakeFile

### CreateFile (Text / Binary)
|Outcome|Context|
| :-- | :-- |
|AlreadyExists|The file already exists and overwriting is not allowed.|
|FailedCreatingMissingParents|Missing parents were allowed to be created but the creation operation failed.|
|DestDirDoesNotExist|The destination directory does not exist and could not be created.|
|FailedOpenWrite|A write file handle could not be obtained.|
|FailedWrite|The data could not be written to the file.|


### CreateOrWrite (Text / Binary)
|Outcome|Context|
| :-- | :-- |
|FailedOpenWrite|A write file handle could not be obtained.|
|FailedCreatingMissingParents|Missing parents were allowed to be created but the creation operation failed.|
|DestDirDoesNotExist|The destination directory does not exist and could not be created.|
|FailedWrite|The data could not be written to the file.|


### DeleteFile
|Outcome|Context|
| :-- | :-- |
|NoOp|The file does not exist on the filesystem|
|IsReadOnly|The file is readonly and deleting readonly files is disallowed.|
|CouldNotChangePerms|The file is readonly and readonly files are allowed to be deleted, but the file permissions could not be changed in order for it to be deleted.|
|FailedDelete|The file was unable to be deleted.|


### ReadFile (Text / Binary)
|Outcome|Context|
| :-- | :-- |
|DoesNotExist|The file does not exist on the filesystem.|
|FailedOpenRead|A read file handle could not be obtained.|
|FailedWrite|The data could not read from the file.|


### WriteFile (Text / Binary)
|Outcome|Context|
| :-- | :-- |
|DoesNotExist|The file does not exist on the filesystem.|
|FailedOpenWrite|A write file handle could not be obtained.|
|FailedWrite|The data could not be written to the file.|


### AppendFile (Text / Binary)
|Outcome|Context|
| :-- | :-- |
|NoOp|The content to append was empty.|
|DoesNotExist|The file does not exist on the filesystem.|
|FailedOpenWrite|A write file handle could not be obtained.|
|FailedWrite|The data could not be written to the file.|


### CopyFile
|Outcome|Context|
| :-- | :-- |
|DestDirDoesNotExist|The destination directory does not exist and was unable to be created or was not allowed to be created.|
|DoesNotExist|The source file to be copied does not exist on the filesystem.|
|NoOp|The destination path and the source path reference the same location.|
|AlreadyExists|The destination file already exists and overwriting is not allowed.|
|FailedOpenWrite|Failed opening a write handle to the destination file.|
|FailedWrite|Failed writing source file's data to the destination file.|


### CopyFileWithNewName
|Outcome|Context|
| :-- | :-- |
|BadFileName|The file name is empty or consists only of whitespace and/or path separators.|
|DestDirDoesNotExist|The destination directory does not exist and was unable to be created or was not allowed to be created.|
|DoesNotExist|The source file to be copied does not exist on the filesystem.|
|NoOp|The destination path and the source path reference the same location.|
|AlreadyExists|The destination file already exists and overwriting is not allowed.|
|FailedOpenWrite|Failed opening a write handle to the destination file.|
|FailedWrite|Failed writing source file's data to the destination file.|


### MoveFile
|Outcome|Context|
| :-- | :-- |
|DestDirDoesNotExist|The destination directory does not exist and was unable to be created or was not allowed to be created.|
|DoesNotExist|The source file to be copied does not exist on the filesystem.|
|NoOp|The destination path and the source path reference the same location.|
|AlreadyExists|The destination file already exists and overwriting is not allowed.|
|FailedOpenWrite|Failed opening a write handle to the destination file.|
|FailedWrite|Failed writing source file's data to the destination file.|
|FailedDelete|Failed deleting the original file after it was successfully copied to the destination.|


### MoveFileWithNewName
|Outcome|Context|
| :-- | :-- |
|BadFileName|The file name is empty or consists only of whitespace and/or path separators.|
|DestDirDoesNotExist|The destination directory does not exist and was unable to be created or was not allowed to be created.|
|DoesNotExist|The source file to be copied does not exist on the filesystem.|
|NoOp|The destination path and the source path reference the same location.|
|AlreadyExists|The destination file already exists and overwriting is not allowed.|
|FailedOpenWrite|Failed opening a write handle to the destination file.|
|FailedWrite|Failed writing source file's data to the destination file.|
|FailedDelete|Failed deleting the original file after it was successfully copied to the destination.|


### Query Functions
|Outcome|Context|
| :-- | :-- |
|DoesNotExist|The file does not exist on the filesystem.|
|FailedStatQuery|The query operation failed.|


### ChangeTimestampLastModified
|Outcome|Context|
| :-- | :-- |
|DoesNotExist|The file does not exist on the filesystem.|


### ChangeFilePermissions
|Outcome|Context|
| :-- | :-- |
|DoesNotExist|The file does not exist on the filesystem.|
|CouldNotChangePerms|The file's permissions could not be changed.|


### ChangeFileName / ChangeFileExt / ChangeFileExtSingle
|Outcome|Context|
| :-- | :-- |
|BadFileName|The file name is empty or consists only of whitespace and/or path separators.|
|DestDirDoesNotExist|The destination directory does not exist and was unable to be created or was not allowed to be created.|
|DoesNotExist|The source file to be copied does not exist on the filesystem.|
|NoOp|The destination path and the source path reference the same location.|
|AlreadyExists|The destination file already exists and overwriting is not allowed.|
|FailedOpenWrite|Failed opening a write handle to the destination file.|
|FailedWrite|Failed writing source file's data to the destination file.|
|FailedDelete|Failed deleting the original file after it was successfully copied to the destination.|


## CakeDir

### CreateDir
|Outcome|Context|
| :-- | :-- |
|NoOp|The directory already exists on the filesystem.|
|FailedCreate|The directory failed to be created.|


### DeleteDir
|Outcome|Context|
| :-- | :-- |
|NoOp|The directory does not exist on the filesystem.|
|FailedDelete|The directory failed to be deleted.|


### CopyDir
|Outcome|Context|
| :-- | :-- |
|DoesNotExist|The directory does not exist on the filesystem.|
|NoOp|The destination directory is the same as the source directory path.|
|DestDirDoesNotExist|The destination directory does not exist and could not be created.|
|FailedCopy|The copy operation encountered an error and was aborted.|


### CopyDirWithNewName
|Outcome|Context|
| :-- | :-- |
|BadDirName|The directory name is empty or consists only of whitespace and/or path separators.|
|DoesNotExist|The directory does not exist on the filesystem.|
|NoOp|The destination directory is the same as the source directory path.|
|DestDirDoesNotExist|The destination directory does not exist and could not be created.|
|FailedCopy|The copy operation encountered an error and was aborted.|


### MoveDir
|Outcome|Context|
| :-- | :-- |
|DoesNotExist|The directory does not exist on the filesystem.|
|NoOp|The destination directory is the same as the source directory path.|
|DestDirDoesNotExist|The destination directory does not exist and could not be created.|
|FailedCopy|The copy operation encountered an error and was aborted.|
|FailedDelete|The original directory could not be deleted.|


### MoveDirWithNewName
|Outcome|Context|
| :-- | :-- |
|BadDirName|The directory name is empty or consists only of whitespace and/or path separators.|
|DoesNotExist|The directory does not exist on the filesystem.|
|NoOp|The destination directory is the same as the source directory path.|
|DestDirDoesNotExist|The destination directory does not exist and could not be created.|
|FailedCopy|The copy operation encountered an error and was aborted.|
|FailedDelete|The original directory could not be deleted.|


### ChangeDirName
|Outcome|Context|
| :-- | :-- |
|BadDirName|The directory name is empty or consists only of whitespace and/or path separators.|
|DoesNotExist|The directory does not exist on the filesystem.|
|NoOp|The destination directory is the same as the source directory path.|
|DestDirDoesNotExist|The destination directory does not exist and could not be created.|
|FailedCopy|The copy operation encountered an error and was aborted.|
|FailedDelete|The original directory could not be deleted.|


### QueryStatData
|Outcome|Context|
| :-- | :-- |
|DoesNotExist|The directory does not exist on the filesystem.|
|FailedStatQuery|The info could not be retrieved from the OS.|


