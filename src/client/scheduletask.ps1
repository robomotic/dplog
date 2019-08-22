$binarypath= Get-ChildItem "dist\service.exe" | select -ExpandProperty FullName
$action = New-ScheduledTaskAction -Execute $binarypath
$trigger = New-ScheduledTaskTrigger -Daily -At 8am
$task = Register-ScheduledTask -TaskName "DpLog client" -Trigger $trigger -Action $action
$task.Triggers.Repetition.Duration = "P1D" //Repeat for a duration of one day
$task.Triggers.Repetition.Interval = "PT30M" //Repeat every 30 minutes, use PT1H for every hour
$task | Set-ScheduledTask