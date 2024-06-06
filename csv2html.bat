@echo off
set _2px=style=""border:2px solid black; border-collapse: collapse;""
set _1px=style=""border:1px solid black; border-collapse: collapse;""
csv2html.exe --table "%_2px%" --th "%_2px%" --td "%_1px%" %*
