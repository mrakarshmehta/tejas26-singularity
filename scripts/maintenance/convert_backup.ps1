$content = Get-Content 'D:\HiddenYatra\mysql_data_BACKUP_20260809_team_setup.sql' -Raw -Encoding Unicode
[System.IO.File]::WriteAllText('D:\HiddenYatra\scratch\hiddenyatra_prod_backup.sql', $content, [System.Text.UTF8Encoding]::new($false))
Write-Output 'Done. UTF-8 NoBOM backup written to scratch/hiddenyatra_prod_backup.sql'
