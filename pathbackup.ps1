$userpath = [environment]::getenvironmentvariable('path', [system.environmentvariabletarget]::user)
$machinepath = [environment]::getenvironmentvariable('path', [system.environmentvariabletarget]::machine)
$backuppath = "$($env:USERPROFILE)/.envpaths"
function make-folder {
	param ($foldername)
	if (!(test-path $foldername)) {
		mkdir $foldername
	}
}
function dump-backup {
	param (
		$todump,
		$dumproot,
		$dumpdest,
		$oldfolder,
		$maxold = 10,
		$oldword = 'old'
	)
	$oldfolder = "$dumproot/$oldfolder"
	$dumpdest = "$dumproot/$dumpdest"
	make-folder "$dumproot"
	make-folder "$oldfolder"
	$tmpfile = new-item (new-guid)
	write-output "$todump" > $tmpfile
	$newhash = get-filehash $tmpfile
	$currenthash = get-filehash $dumpdest
	if ($newhash.hash -ne $currenthash.hash) {
		gci $oldfolder | sort-object -descending {$_.name.length} |foreach {
			# increment the backups by one
			move-item "$oldfolder/$($_.name)" "$oldfolder/$($_.name)$oldword"
		}
		# remove any items older than the max
		remove-item "$oldfolder/$($oldword*$maxold)*"
		if (test-path $dumpdest) {
			copy-item "$dumpdest" "$oldfolder/$oldword"
		}
		move-item $tmpfile $dumpdest -force
		#write-output "$todump" > "$dumpdest"
	} else {
		remove-item $tmpfile
		(get-item $dumpdest).lastwritetime = get-date
	}
}
make-folder "$backuppath"
dump-backup -todump $userpath -dumproot "$backuppath" -dumpdest "userpath" -oldfolder "userold"
dump-backup -todump $machinepath -dumproot "$backuppath" -dumpdest "machinepath" -oldfolder "machineold"
