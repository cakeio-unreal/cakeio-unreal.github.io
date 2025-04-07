
!!! warning
    `SetFileExt` is designed to accept strings that __only__ represent file extensions. (e.g., `".txt"` or `".bin.dat"`). It is not meant for path-like strings that contain file names and file extensions. (e.g., `"data.bin.dat"`, `"items/desc.txt"`) Use `SetFileExtFromFilePath` for that instead.