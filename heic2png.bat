@echo off
for %%f in (.\*.heic) do (
	echo converting %%~nf
	magick convert %%~nf.heic %%~nf.png && del %%~nf.heic
)
