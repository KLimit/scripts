@echo off

rem just run mysqlsh.exe with motiv params

set uri=motivpsc_script@factory.motivps.com:3306
set schema=motivpsc_production

mysqlsh --uri="%uri%" -D %schema% --sql
