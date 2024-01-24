# windows defender 提示病毒 bug

删除 C:\ProgramData\Microsoft\Windows Defender\Scans\History\Service\DetectionHistory 下的所有子文件夹。

该文件夹储存了安全中心保护记录, 我们手动删除病毒文件后, windows defender 已经检测出该文件但没有办法对它执行删除、隔离等操作, 保护记录里记录该文件没有被执行任何操作就会一直记录在需要执行操作的记录里, 清除历史记录后就没有对该病毒文件的记录了, 也就不会提示需要执行操作。
