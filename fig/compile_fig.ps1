$FIG_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$ROOT_DIR = Split-Path $FIG_DIR
Set-Location $FIG_DIR
$texCmd = (Get-Command "xelatex").Source
$ppmCmd = (Get-Command "pdftoppm").Source
$pythonCmd = (Get-Command "python" -ErrorAction SilentlyContinue).Source
if (-not $pythonCmd) { $pythonCmd = (Get-Command "python3" -ErrorAction SilentlyContinue).Source }
$buildDir = Join-Path $FIG_DIR "build"
New-Item -ItemType Directory -Force -Path $buildDir | Out-Null
function Remove-PythonCache {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return }
    Get-ChildItem -Path $Path -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
        Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path $Path -Recurse -File -Include "*.pyc", "*.pyo" -ErrorAction SilentlyContinue |
        Remove-Item -Force -ErrorAction SilentlyContinue
}
function Remove-LatexPdfIntermediates {
    Get-ChildItem -Path $buildDir -File -Filter "*.pdf" -ErrorAction SilentlyContinue |
        Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path $FIG_DIR -File -Filter "tmp-pdfcrop-*" -ErrorAction SilentlyContinue |
        Remove-Item -Force -ErrorAction SilentlyContinue
}
$chapterTitle = @{
    "Mechanics"       = "力学"
    "Electrodynamics" = "电学"
    "Statistics"      = "热学"
    "Optics"          = "光学"
    "MathTool"        = "数学工具"
}
$chapterOrder = @("Mechanics", "Electrodynamics", "Statistics", "Optics", "MathTool")
function Get-SectionDisplay {
    param([string]$Name)
    $d = $Name -creplace '(?<=[a-z])(?=[A-Z])', ' '
    $d = $d -creplace '(?<=[A-Z])(?=[A-Z][a-z])', ' '
    $d = $d -creplace '([a-zA-Z])(\d+)', '$1 $2'
    return $d.Trim()
}
$allFigs = @()
$figMap = @{}
$texFiles = Get-ChildItem $ROOT_DIR\chapters -Recurse -Filter "*_code.tex" -File |
    Where-Object { $_.FullName -notmatch "\\build\\" }
foreach ($f in $texFiles) {
    $baseName = [IO.Path]::GetFileNameWithoutExtension($f.Name)
    if ($baseName.EndsWith("_code")) { $baseName = $baseName.Substring(0, $baseName.Length - 5) }
    $relDir = $f.Directory.FullName.Substring((Join-Path $ROOT_DIR "chapters").Length + 1)
    $parts = $relDir -split '\\'
    $chapter = $parts[0]
    $section = $parts[1]
    if (-not $figMap.ContainsKey($baseName)) {
        $entry = [PSCustomObject]@{ Name = $baseName; Type = "tex"; Source = $f.FullName; Chapter = $chapter; Section = $section }
        $allFigs += $entry
        $figMap[$baseName] = $entry
    }
}
$pyFiles = Get-ChildItem $ROOT_DIR\chapters -Recurse -Filter "*_code.py" -File |
    Where-Object { $_.FullName -notmatch "\\build\\" } | Sort-Object FullName
foreach ($f in $pyFiles) {
    $baseName = [IO.Path]::GetFileNameWithoutExtension($f.Name)
    if ($baseName.EndsWith("_code")) { $baseName = $baseName.Substring(0, $baseName.Length - 5) }
    $relDir = $f.Directory.FullName.Substring((Join-Path $ROOT_DIR "chapters").Length + 1)
    $parts = $relDir -split '\\'
    $chapter = $parts[0]
    $section = $parts[1]
    $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
    $imgMatches = [regex]::Matches($content, '(?i)save_figure\s*\(\s*fig\s*,\s*"([^"]+)"')
    $images = @()
    foreach ($match in $imgMatches) { $images += $match.Groups[1].Value }
    if ($images.Count -eq 0) { continue }
    if (-not $figMap.ContainsKey($baseName)) {
        $entry = [PSCustomObject]@{ Name = $baseName; Type = "python"; Source = $f.FullName; Chapter = $chapter; Section = $section; Images = $images }
        $allFigs += $entry
        $figMap[$baseName] = $entry
    }
}
$sectionList = @()
$chIdx = 0
Write-Host ""; Write-Host "Figures"; Write-Host ""
foreach ($ch in $chapterOrder) {
    $chFigs = $allFigs | Where-Object { $_.Chapter -eq $ch } | Sort-Object Section, Name
    if ($chFigs.Count -eq 0) { continue }
    $secGroups = @{}
    foreach ($f in $chFigs) {
        if (-not $secGroups.ContainsKey($f.Section)) { $secGroups[$f.Section] = @() }
        $secGroups[$f.Section] += $f
    }
    Write-Host ("  $($chIdx+1). $($chapterTitle[$ch])") -ForegroundColor White
    $secIdx = 0
    foreach ($sec in ($secGroups.Keys | Sort-Object)) {
        $figs = @($secGroups[$sec] | Sort-Object Name)
        $disp = Get-SectionDisplay $sec
        Write-Host ("      $($chIdx+1).$($secIdx+1) $disp")
        for ($k = 0; $k -lt $figs.Count; $k++) {
            $displayName = $figs[$k].Name -replace '_', ' '
            Write-Host ("          $($chIdx+1).$($secIdx+1).$($k+1) $displayName")
        }
        $sectionList += [PSCustomObject]@{ ChIdx = $chIdx; SecIdx = $secIdx; Chapter = $ch; Section = $sec; Disp = $disp; Figs = $figs }
        $secIdx++
    }
    $chIdx++
}
$figLookup = @{}
$secLookup = @{}
$chLookup = @{}
foreach ($sl in $sectionList) {
    $chId = "$($sl.ChIdx + 1)"
    $secId = "$($sl.SecIdx + 1)"
    $secLookup["$chId.$secId"] = $sl
    if (-not $chLookup.ContainsKey($chId)) { $chLookup[$chId] = @() }
    $chLookup[$chId] += $sl
    for ($k = 0; $k -lt $sl.Figs.Count; $k++) {
        $figLookup["$chId.$secId.$($k+1)"] = $sl.Figs[$k]
    }
}
while ($true) {
    $selection = Read-Host "`nFigure IDs (e.g. 1, 2.1.2, 2.1,3.2.1; Enter=all)"
    $selectedFigs = @()
    if ([string]::IsNullOrWhiteSpace($selection)) {
        foreach ($sl in $sectionList) { foreach ($f in $sl.Figs) { $selectedFigs += $f } }
        break
    }
    $seen = @{}
    foreach ($part in $selection.Split(',')) {
        $part = $part.Trim()
        if ($figLookup.ContainsKey($part)) {
            $fig = $figLookup[$part]
            if (-not $seen.ContainsKey($fig.Name)) { $selectedFigs += $fig; $seen[$fig.Name] = $true }
        } elseif ($secLookup.ContainsKey($part)) {
            foreach ($f in $secLookup[$part].Figs) { if (-not $seen.ContainsKey($f.Name)) { $selectedFigs += $f; $seen[$f.Name] = $true } }
        } elseif ($chLookup.ContainsKey($part)) {
            foreach ($sl in $chLookup[$part]) {
                foreach ($f in $sl.Figs) { if (-not $seen.ContainsKey($f.Name)) { $selectedFigs += $f; $seen[$f.Name] = $true } }
            }
        }
    }
    if ($selectedFigs.Count -gt 0) { break }
    Write-Host "Invalid input, try again." -ForegroundColor Yellow
}
$overrideInput = Read-Host "`nSync project images? [y/n, Enter=y]"
if ([string]::IsNullOrWhiteSpace($overrideInput)) { $overrideInput = "y" }
$overrideInput = $overrideInput.ToLower()
if ($overrideInput -eq "y" -or $overrideInput -eq "yes") { $override = $true }
else { $override = $false }
Write-Host ""
function Invoke-Override {
    param([string]$BaseName, [string]$PngSource)
    if (-not $override) { return }
    if (-not (Test-Path $PngSource)) { return }
    $targets = Get-ChildItem $ROOT_DIR\chapters -Recurse -Filter "${BaseName}.png" -File
    foreach ($t in $targets) {
        Copy-Item $PngSource $t.FullName -Force
        $rel = $t.FullName.Substring($ROOT_DIR.Length)
        Write-Host "  -> Overrode ...$rel"
    }
}
$figDraw = Join-Path $FIG_DIR "fig_draw.tex"
Set-Content -Path $figDraw -Value "\documentclass[tikz,border=5pt]{standalone}" -Encoding UTF8
Add-Content -Path $figDraw -Value "\input{fig_config.tex}" -Encoding UTF8
Add-Content -Path $figDraw -Value "\begin{document}" -Encoding UTF8
Add-Content -Path $figDraw -Value "" -Encoding UTF8
$successCount = 0; $failCount = 0
foreach ($fig in $selectedFigs) {
    $baseName = $fig.Name
    if ($fig.Type -eq "python") {
        Write-Host "[$($fig.Chapter)] $baseName ... " -NoNewline
        $env:PYTHONPATH = "$FIG_DIR;$env:PYTHONPATH"
        $oldDontWriteBytecode = $env:PYTHONDONTWRITEBYTECODE
        $oldPycachePrefix = $env:PYTHONPYCACHEPREFIX
        $env:PYTHONDONTWRITEBYTECODE = "1"
        Remove-Item Env:\PYTHONPYCACHEPREFIX -ErrorAction SilentlyContinue
        $logOut = Join-Path $buildDir "py_${baseName}.log"
        $logErr = Join-Path $buildDir "py_${baseName}.err"
        $process = Start-Process -FilePath $pythonCmd -ArgumentList "-B `"$($fig.Source)`"" -Wait -NoNewWindow -PassThru -RedirectStandardOutput $logOut -RedirectStandardError $logErr
        if ($null -eq $oldDontWriteBytecode) { Remove-Item Env:\PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue }
        else { $env:PYTHONDONTWRITEBYTECODE = $oldDontWriteBytecode }
        if ($null -ne $oldPycachePrefix) { $env:PYTHONPYCACHEPREFIX = $oldPycachePrefix }
        Remove-PythonCache -Path $buildDir
        Remove-PythonCache -Path $FIG_DIR
        if ($process.ExitCode -ne 0) {
            Write-Host "Failed (exit $($process.ExitCode))" -ForegroundColor Red
            $failCount++
            continue
        }
        $ok = $false
        foreach ($img in $fig.Images) {
            $outPath = Join-Path $buildDir $img
            if (Test-Path $outPath) {
                $ok = $true
                Invoke-Override -BaseName ([IO.Path]::GetFileNameWithoutExtension($img)) -PngSource $outPath
            }
        }
        if ($ok) { Write-Host "OK" -ForegroundColor Green; $successCount++ }
        else { Write-Host "No output" -ForegroundColor Yellow; $failCount++ }
    } else {
        Write-Host "[$($fig.Chapter)] $baseName ... " -NoNewline
        $codeFile = $fig.Source
        $tempTex = Join-Path $FIG_DIR "__fig_temp.tex"
        $baseUri = [Uri](($FIG_DIR.TrimEnd('\')) + '\')
        $targetUri = [Uri]($codeFile)
        $relPath = [Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()) -replace '\\', '/'
        $wrapper = @"
\documentclass[tikz,border=5pt]{standalone}
\input{fig_config.tex}
\begin{document}
\input{$relPath}
\end{document}
"@
        Set-Content -Path $tempTex -Value $wrapper -Encoding UTF8
        & $texCmd -interaction=nonstopmode -output-directory="$buildDir" $tempTex *>$null 2>&1
        & $texCmd -interaction=nonstopmode -output-directory="$buildDir" $tempTex *>$null 2>&1
        Remove-Item $tempTex -Force -ErrorAction SilentlyContinue
        $tempPdf = Join-Path $buildDir "__fig_temp.pdf"
        if (Test-Path $tempPdf) {
            & pdfcrop $tempPdf $tempPdf *>$null 2>&1
            $outPdf = Join-Path $buildDir "$baseName.pdf"
            Move-Item $tempPdf $outPdf -Force
            Get-ChildItem "$buildDir\__fig_temp.*" -ErrorAction SilentlyContinue | Remove-Item -Force
            & $ppmCmd -png -r 300 $outPdf "$buildDir\$baseName" *>$null 2>&1
            if (Test-Path "$buildDir\$baseName-1.png") { Move-Item "$buildDir\$baseName-1.png" "$buildDir\$baseName.png" -Force }
            $outPng = Join-Path $buildDir "$baseName.png"
            Remove-LatexPdfIntermediates
            if (Test-Path $outPng) {
                Write-Host "OK" -ForegroundColor Green
                $successCount++
                Add-Content -Path $figDraw -Value "\input{$relPath}" -Encoding UTF8
                Add-Content -Path $figDraw -Value "" -Encoding UTF8
                Invoke-Override -BaseName $baseName -PngSource $outPng
            } else {
                Write-Host "Failed (PNG not generated)" -ForegroundColor Red
                $failCount++
            }
        } else {
            Write-Host "Failed" -ForegroundColor Red
            Get-Content (Join-Path $buildDir "__fig_temp.log") -ErrorAction SilentlyContinue | Select-String "^!" | Select-Object -First 10
            $failCount++
        }
    }
}
Add-Content -Path $figDraw -Value "\end{document}" -Encoding UTF8
Remove-PythonCache -Path $buildDir
Remove-LatexPdfIntermediates
Get-ChildItem -Path $buildDir -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -ne ".png" } |
    Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host ""
Write-Host "Done: $successCount succeeded, $failCount failed" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Yellow" })
Write-Host "Output: $buildDir"