#!/bin/sh
tocheck=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')
errorcount=0
IFS=$'\n' read -ra tocheck <<< "$tocheck"
for toch in "${tocheck[@]}"
do
	echo "$toch:"
	# maybe there's a shebang saying it should be python3 syntax
	if (head -n1 "$toch" | grep -q python3)
	then
		# shady mix of windows' py.exe and shell
		py='py -3'
	else
		py='py -2'
	fi
	if eval "git show ':$toch' | $py -m pyflakes"
	then
		echo "No flakes found in $toch"
	else
		echo "Fix your errors in $toch!"
		errorcount=$(( $errorcount + 1 ))
	fi
	echo "---"
done
exit $errorcount
