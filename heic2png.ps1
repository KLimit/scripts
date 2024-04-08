get-childitem *.heic | foreach-object -parallel {
	$orig = $_.name
	$base = $_.basename
	write-host "converting $orig"
	& magick convert "$orig" "$base.png" && remove-item $_
}
