@echo off
rem make sure in master branch, then start ipython session with PCU_IO
git rev-parse --abbrev-ref HEAD | find /v "" | findstr /r /c:"^master$" > NUL & IF ERRORLEVEL 1 (
	echo Switch to master branch and try again
	break
) ELSE (
	ECHO I am on the main branch
	ipython -i -c "import sys; import PCU_IO as pcuio; sys.argv = ['']; self = pcuio.TestControl(); self.helper.run_DUT_cmd('chassis output off'); self.helper.run_DUT_cmd('acc output off')"
)
exit
