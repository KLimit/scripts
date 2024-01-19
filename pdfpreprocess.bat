@echo off
set file=%~1
set ext=%file:~-3%
echo %ext%
if "%ext%" == "pdf" (
	pdftotext "%file%" -
)
