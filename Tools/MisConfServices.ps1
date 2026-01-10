$results = Get-CimInstance Win32_Service | ForEach-Object {

    $PathName = $_.PathName

    # Skip services with no path
    if (-not $PathName) { return }

    $PathName = $PathName.Trim()

    # Extract executable exactly
    if ($PathName.StartsWith('"')) {

        # Extract inside the first quotes
        $exe = ($PathName -replace '^"([^"]+)".*$', '$1')
        $Quoted = $true
    }
    else {
        # Extract everything up to .exe (handles spaces)
        if ($PathName -match '^(.+?\.exe)') {
            $exe = $matches[1]
        } else {
            # Rare fallback
            $exe = $PathName -replace '\s+.*$', ''
        }
        $Quoted = $false
    }

    # Detect unquoted vuln
    $Unquoted = (-not $Quoted -and $exe -match '\s')
    # ----- Directory ACL check (for unquoted path exploitation) -----
    # Determine exploitable directory (first space in EXE path)
    # ------------------------------
    # Find exploit directory
    # ------------------------------

    # Remove arguments (truncate at first space)
    $beforeSpace = $PathName -replace '\s+.*$', ''

    # Force the truncated string to behave as a file
    $fakeFile = "$beforeSpace.exe"

    # Extract correct parent directory
    $ExploitDir = Split-Path $fakeFile -Parent

    $WeakDirACL = $false
    $Directory  = $ExploitDir

    if (Test-Path $Directory) {
        $dirAcl = icacls $Directory 2>$null
        if ($dirAcl) {
            $WeakDirACL = (
                $dirAcl -match 'BUILTIN\\Users:.*\((AD|WD|W|M|F|WDC|WO)\)'     -or
                $dirAcl -match 'Everyone:.*\((AD|WD|W|M|F|WDC|WO)\)'           -or
                $dirAcl -match 'Authenticated Users:.*\((AD|WD|W|M|F|WDC|WO)\)' -or
                $dirAcl -match "$env:USERNAME:.*\((AD|WD|W|M|F|WDC|WO)\)"
            )
        }
    }


    # Check file existence
    $Exists = Test-Path $exe

    # Weak ACL check
    $WeakACL = $false
    if ($Exists) {
        $acl = icacls $exe 2>$null
        if ($acl) {
            $WeakACL = (
                $acl -match 'BUILTIN\\Users:.*\(M\)' -or
                $acl -match 'BUILTIN\\Users:.*\(W\)' -or
                $acl -match 'Everyone:.*\(M\)'       -or
                $acl -match 'Everyone:.*\(W\)'       -or
                $acl -match 'Authenticated Users:.*\(M\)'
            )
        }
    }



    $ServiceWeakDACL = $false
    $DangerousRightsFound = @()

    $SDDL = (sc.exe sdshow $_.Name) 2>$null
    $CanWrite = sc.exe config $_.Name  DisplayName= $_.name  | Select-String "SUCCESS"

    if ($CanWrite) {
        $ServiceWeakDACL = $True
    }


    if ( ($Unquoted -and $WeakDirACL) -or $WeakACL -or $ServiceWeakDACL)
 {


        [PSCustomObject]@{
            Service     = $_.Name
            RawPath     = $PathName
            Unquoted    = $Unquoted
            WeakACL     = $WeakACL
            DirWeakACL = $WeakDirACL
            ServiceACL = $ServiceWeakDACL
            Owner       = $_.StartName 

        }
    }
}

# Output
$results | Format-Table -AutoSize
$results | Out-File "C:\Users\$env:USERNAME\svc_vulnerable.txt" -Encoding UTF8
