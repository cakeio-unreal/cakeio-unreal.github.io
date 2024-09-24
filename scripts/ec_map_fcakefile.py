from ec_map_types import ErrorCode, ClassErrorMap, FunctionErrorMap

common_error_codes = {
            
    'DoesNotExist': 
        ErrorCode('DoesNotExist', None, 'Occurs when the file does not exist.'),
    'AlreadyExists':
        ErrorCode('AlreadyExists', 'OverwriteItems', 'Occurs when the file already exists and the policy disallows overwriting items.'),
    'FailedCreatingMissingParents': 
        ErrorCode('FailedCreatingMissingParents', 'MissingParents', 'Occurs when the destination directory has missing parents, the policy allows creation of missing parents, but the directory creation IO operations failed.'),
    'DestDirDoesNotExist':
        ErrorCode('DestDirDoesNotExist', 'MissingParents', 'Occurs when the destination directory has missing parents and the policy disallows missing parent creation.'),
    'FileIsReadOnly':
        ErrorCode('FileIsReadOnly', 'FileDelete', 'Occurs when the file is read only and the policy disallows deleting read only files.'),
    'FailedOpenW':
        ErrorCode('FailedOpenW', None, 'Occurs when a write handle could not be obtained from the operating system.'),
    'FailedOpenR':
        ErrorCode('FailedOpenR', None, 'Occurs when a read handle could not be obtained from the operating system.'),
    'FailedCopy':
        ErrorCode('FailedCopy', None, 'Occurs when the operating system failed copying the source file to the destination directory.'),
    'FailedDelete':
        ErrorCode('FailedDelete', None, 'Occurs when the operating system failed deleting the file.'),
}

def from_common_with_ctx(ec: str, ctx: str):
    src_ec = common_error_codes[ec]
    final_ctx = src_ec.extra_context + f' {ctx}'
    return ErrorCode(src_ec.code_value, src_ec.linked_policy, final_ctx)

def use_common(ec: str):
    return common_error_codes[ec]

fcakefile = ClassErrorMap('FCakeFile',
    [
        FunctionErrorMap('CreateTextFile / CreateBinaryFile',
        [
            use_common('AlreadyExists'),
            use_common('FailedCreatingMissingParents'),
            use_common('DestDirDoesNotExist'),
            use_common('FailedOpenW'),
        ]),
        FunctionErrorMap('CreateOrWriteTextFile / CreateOrWriteBinaryFile', 
        [
            use_common('AlreadyExists'),
            use_common('FailedCreatingMissingParents'),
            use_common('DestDirDoesNotExist'),
            use_common('FailedOpenW'),
        ]),
        FunctionErrorMap('WriteTextToFile / WriteBytesToFile', 
        [
            from_common_with_ctx('DoesNotExist', 'Write is only intended for existing files, use Create otherwise.'),
            use_common('FailedOpenW'),
        ]),
        FunctionErrorMap('AppendTextToFile / AppendBytesToFile',
        [
            ErrorCode('NOP', None, 'Occurs when an empty string or empty byte array is submitted to be appended.'),
            from_common_with_ctx('DoesNotExist', 'Append is only intended for existing files, use Create otherwise.'),
            use_common('FailedOpenW'),
        ]),
        FunctionErrorMap('ReadFileAsString / ReadFileAsBytes', 
        [
            use_common('DoesNotExist'),
            use_common('FailedOpenR'),
        ]),
        FunctionErrorMap('DeleteFile', 
        [
            ErrorCode('NOP', None, 'Occurs when the file already does not exist.'),
            use_common('FileIsReadOnly'),
            ErrorCode('CouldNotChangePerms', 'FileDelete', 'Occurs when the file is read only, the policy allows deleting read only files, but the operating system could not remove the read only attribute from the file.'),
            use_common('FailedDelete'),
        ]),
        FunctionErrorMap('CopyFile / CopyFileAliased', 
        [
            ErrorCode('NOP', None, 'Occurs when the destination directory is the source file\'s directory.'),
            use_common('DoesNotExist'),
            use_common('AlreadyExists'),
            ErrorCode('CouldNotReplace', 'OverwriteItems', 'Occurs when a file of the same name already exists in destination directory, the policy allows overwrites, but that file could not be deleted in preparation for the copy operation.'),
        ]),
        FunctionErrorMap('MoveFile / MoveFileAliased', 
        [
            ErrorCode('NOP', None, 'Occurs when the destination directory is the source file\'s directory.'),
            use_common('DoesNotExist'),
            use_common('AlreadyExists'),
            ErrorCode('CouldNotReplace', 'OverwriteItems', 'Occurs when a file of the same name already exists in destination directory, the policy allows overwrites, but that file could not be deleted in preparation for the move operation.'),
            ErrorCode('FailedCopy', None, 'Occurs when the operating system failed copying the source file to the destination directory.'),
            ErrorCode('FailedDelete', None, 'Occurs when the operating system failed deleting the original source file.')
        ]),
        FunctionErrorMap('RenameFile', 
        [
            ErrorCode('BadFileName', None, 'Occurs when the submitted name is completely empty after being sanitized for illegal characters.'),
            ErrorCode('NOP', None, 'Occurs when the destination directory is the source file\'s directory.'),
            use_common('DoesNotExist'),
            use_common('AlreadyExists'),
            ErrorCode('CouldNotReplace', 'OverwriteItems', 'Occurs when a file of the same name already exists in destination directory, the policy allows overwrites, but that file could not be deleted in preparation for the move operation.'),
            ErrorCode('FailedCopy', None, 'Occurs when the operating system failed copying the source file to the destination directory.'),
            ErrorCode('FailedDelete', None, 'Occurs when the operating system failed deleting the original source file.')
        ]),
    ]
)