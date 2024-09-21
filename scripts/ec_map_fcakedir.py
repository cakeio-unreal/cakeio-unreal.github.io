from ec_map_types import ErrorCode, ClassErrorMap, FunctionErrorMap

common_error_codes = {
            
    'DoesNotExist': 
        ErrorCode('DoesNotExist', None, 'Occurs when the directory does not exist.'),
    'AlreadyExists':
        ErrorCode('AlreadyExists', 'OverwriteItems', 'Occurs when the directory already exists and the policy disallows overwriting items.'),
    'FailedCreatingMissingParents': 
        ErrorCode('FailedCreatingMissingParents', 'MissingParents', 'Occurs when the destination directory has missing parents, the policy allows creation of missing parents, but the directory creation IO operations failed.'),
    'DestDirDoesNotExist':
        ErrorCode('DestDirDoesNotExist', 'MissingParents', 'Occurs when the destination directory has missing parents and the policy disallows missing parent creation.'),
    'FileIsReadOnly':
        ErrorCode('FileIsReadOnly', 'FileDelete', 'Occurs when the file is read only and the policy disallows deleting read only files.'),
    'FailedOpenW':
        ErrorCode('FailedOpenW', None, 'Occurs when a write handle could not be obtained from the operating system.'),
    'FailedOpenR':
        ErrorCode('FailedOpenW', None, 'Occurs when a read handle could not be obtained from the operating system.'),
    'FailedCreate':
        ErrorCode('FailedCopy', None, 'Occurs when the operating system failed creating the directory.'),
    'FailedCopy':
        ErrorCode('FailedCopy', None, 'Occurs when the operating system failed copying the source directory and its contents to the destination directory.'),
    'FailedDelete':
        ErrorCode('FailedDelete', None, 'Occurs when the operating system failed deleting the directory and its contents.'),
}

def from_common_with_ctx(ec: str, ctx: str):
    src_ec = common_error_codes[ec]
    final_ctx = src_ec.extra_context + f' {ctx}'
    return ErrorCode(src_ec.code_value, src_ec.linked_policy, final_ctx)

def use_common(ec: str):
    return common_error_codes[ec]

fcakedir = ClassErrorMap('FCakeDir',
    [
        FunctionErrorMap('CreateDir',
        [
            ErrorCode('NOP', None, 'Occurs when the directory already exists.'),
            use_common('FailedCreatingMissingParents'),
            use_common('DestDirDoesNotExist'),
            use_common('FailedCreate'),
        ]),
        FunctionErrorMap('ExistsOrCreate',
        [
            use_common('FailedCreatingMissingParents'),
            use_common('DestDirDoesNotExist'),
            use_common('FailedCreate'),
        ]),
        FunctionErrorMap('CopyDir / CopyDirAliased',
        [
            ErrorCode('DoesNotExist', None, 'Occurs when the source directory does not exist.'),
            ErrorCode('NOP', None, 'Occurs when the source directory and the destination directory are the same.'),
            use_common('FailedCreatingMissingParents'),
            use_common('DestDirDoesNotExist'),
            use_common('FailedCopy'),
        ]),
        FunctionErrorMap('MoveDir / MoveDirAliased',
        [
            ErrorCode('DoesNotExist', None, 'Occurs when the source directory does not exist.'),
            ErrorCode('NOP', None, 'Occurs when the source directory and the destination directory are the same.'),
            use_common('FailedCreatingMissingParents'),
            use_common('DestDirDoesNotExist'),
            ErrorCode('FailedCopy', None, 'Occurs when the operating system fails copying the source directory during the move operation.'),
            ErrorCode('FailedDelete', None, 'Occurs when the operating system fails deleting the source directory after the copy operation has completed.'),
        ]),
        FunctionErrorMap('RenameDir',
        [
            ErrorCode('BadDirectoryName', None, 'Occurs when the new directory name is empty after sanitizing it for illegal characters.'),
            ErrorCode('DoesNotExist', None, 'Occurs when the source directory does not exist.'),
            ErrorCode('NOP', None, 'Occurs when the source directory and the destination directory are the same.'),
            use_common('DestDirDoesNotExist'),
            use_common('FailedCreatingMissingParents'),
            ErrorCode('FailedCopy', None, 'Occurs when the operating system fails copying the source directory during the move operation.'),
            ErrorCode('FailedDelete', None, 'Occurs when the operating system fails deleting the source directory after the copy operation has completed.'),
        ]),
        FunctionErrorMap('DeleteDir',
        [
            ErrorCode('NOP', None, 'Occurs when the directory does not exist.'),
            use_common('FailedDelete')
        ]),
    ]
)