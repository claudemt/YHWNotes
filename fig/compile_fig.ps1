$FIG_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$ROOT_DIR = Split-Path $FIG_DIR
Set-Location $FIG_DIR

$texCmd = (Get-Command "xelatex").Source
$ppmCmd = (Get-Command "pdftoppm").Source
$buildDir = Join-Path $FIG_DIR "build"
New-Item -ItemType Directory -Force -Path $buildDir | Out-Null

function Read-Default {
    param([string]$Prompt, [string]$Default)
    $v = Read-Host $Prompt
    if ([string]::IsNullOrWhiteSpace($v)) { return $Default }
    return $v.Trim()
}

$chapters = @(
    @{ Name = "Mechanics";       Title = "力学" },
    @{ Name = "Electrodynamics"; Title = "电学" },
    @{ Name = "Statistics";      Title = "热学" },
    @{ Name = "Optics";          Title = "光学" },
    @{ Name = "MathTool";        Title = "数学工具" }
)

Write-Host ""; Write-Host "Figures"; Write-Host ""

$allCodeFiles = Get-ChildItem $ROOT_DIR\chapters -Recurse -Filter "*_code.tex" -File | Where-Object { $_.FullName -notmatch "\\build\\" } | Sort-Object FullName
if ($allCodeFiles.Count -eq 0) { Write-Host "No figure code files found." -ForegroundColor Red; exit 1 }

$courses = @()
foreach ($ch in $chapters) {
    $chDir = Join-Path (Join-Path $ROOT_DIR "chapters") $ch.Name
    if (-not (Test-Path $chDir)) { continue }
    $chFiles = $allCodeFiles | Where-Object { $_.FullName -like "$chDir\*" }
    if ($chFiles.Count -eq 0) { continue }
    $sectionGroups = @{}
    foreach ($f in $chFiles) {
        $rel = $f.Directory.FullName.Substring($chDir.Length + 1)
        $secName = ($rel -split '\\')[0]
        if (-not $sectionGroups.ContainsKey($secName)) { $sectionGroups[$secName] = @() }
        $sectionGroups[$secName] += $f
    }
    $items = @(); $displays = @(); $filesets = @()
    foreach ($secName in ($sectionGroups.Keys | Sort-Object)) {
        $files = $sectionGroups[$secName] | Sort-Object Name
        $items += $secName; $filesets += @(, @($files))
        $disp = $secName -creplace '(?<=[a-z])(?=[A-Z])', ' '
        $disp = $disp -creplace '(?<=[A-Z])(?=[A-Z][a-z])', ' '
        $displays += $disp
    }
    $courses += [PSCustomObject]@{ Name = $ch.Title; NameEn = $ch.Name; Items = $items; Displays = $displays; FileSets = $filesets }
}

for ($i = 0; $i -lt $courses.Count; $i++) {
    Write-Host ("  $($i+1). $($courses[$i].Name)") -ForegroundColor White
    for ($j = 0; $j -lt $courses[$i].Items.Count; $j++) {
        Write-Host ("      $($i+1).$($j+1) $($courses[$i].Displays[$j])")
        for ($k = 0; $k -lt $courses[$i].FileSets[$j].Count; $k++) {
            $figName = [IO.Path]::GetFileNameWithoutExtension($courses[$i].FileSets[$j][$k].Name)
            if ($figName.EndsWith("_code")) { $figName = $figName.Substring(0, $figName.Length - 5) }
            $figName = $figName -replace '_', ' '
            Write-Host ("          $($i+1).$($j+1).$($k+1) $figName")
        }
    }
}

while ($true) {
    $selection = Read-Host "`nFigure IDs (e.g. 3, 2.1.2, 2.1,3.2.1; Enter=all)"
    $selectedFigs = @()
    if ([string]::IsNullOrWhiteSpace($selection)) {
        for ($c = 0; $c -lt $courses.Count; $c++) {
            for ($j = 0; $j -lt $courses[$c].Items.Count; $j++) {
                foreach ($f in $courses[$c].FileSets[$j]) { $selectedFigs += @{ Chapter = $courses[$c].Name; File = $f } }
            }
        }
        break
    }
    $parsed = @()
    foreach ($part in $selection.Split(',')) {
        $part = $part.Trim()
        if ($part -match '^(\d+)\.(\d+)\.(\d+)$') {
            $c = [int]$matches[1]; $j = [int]$matches[2]; $k = [int]$matches[3]
            if ($c -ge 1 -and $c -le $courses.Count -and $j -ge 1 -and $j -le $courses[$c-1].Items.Count -and $k -ge 1 -and $k -le $courses[$c-1].FileSets[$j-1].Count) { $parsed += @{ Type = "fig"; C = $c; J = $j; K = $k } }
        } elseif ($part -match '^(\d+)\.(\d+)$') {
            $c = [int]$matches[1]; $j = [int]$matches[2]
            if ($c -ge 1 -and $c -le $courses.Count -and $j -ge 1 -and $j -le $courses[$c-1].Items.Count) { $parsed += @{ Type = "sec"; C = $c; J = $j } }
        } elseif ($part -match '^(\d+)$') {
            $c = [int]$part
            if ($c -ge 1 -and $c -le $courses.Count) { $parsed += @{ Type = "ch"; C = $c } }
        }
    }
    foreach ($p in $parsed) {
        if ($p.Type -eq "fig") { $f = $courses[$p.C-1].FileSets[$p.J-1][$p.K-1]; $selectedFigs += @{ Chapter = $courses[$p.C-1].Name; File = $f } }
        elseif ($p.Type -eq "sec") { foreach ($f in $courses[$p.C-1].FileSets[$p.J-1]) { $selectedFigs += @{ Chapter = $courses[$p.C-1].Name; File = $f } } }
        elseif ($p.Type -eq "ch") { for ($j = 0; $j -lt $courses[$p.C-1].Items.Count; $j++) { foreach ($f in $courses[$p.C-1].FileSets[$j]) { $selectedFigs += @{ Chapter = $courses[$p.C-1].Name; File = $f } } } }
    }
    $seen = @{}; $selectedFigs = $selectedFigs | Where-Object { $k = $_.File.FullName; if ($seen.ContainsKey($k)) { $false } else { $seen[$k] = $true; $true } }
    if ($selectedFigs.Count -gt 0) { break }
    Write-Host "Invalid input, try again." -ForegroundColor Yellow
}

$figDraw = Join-Path $FIG_DIR "fig_draw.tex"
Set-Content -Path $figDraw -Value "\documentclass[tikz,border=5pt]{standalone}" -Encoding UTF8
Add-Content -Path $figDraw -Value "\input{fig_config.tex}" -Encoding UTF8
Add-Content -Path $figDraw -Value "\begin{document}" -Encoding UTF8
Add-Content -Path $figDraw -Value "" -Encoding UTF8

$successCount = 0; $failCount = 0
foreach ($fig in $selectedFigs) {
    $codeFile = $fig.File
    $tempTex = Join-Path $FIG_DIR "__fig_temp.tex"
    $baseUri = [Uri](($FIG_DIR.TrimEnd('\')) + '\'); $targetUri = [Uri]($codeFile.FullName)
    $relPath = [Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString()) -replace '\\', '/'

    $baseName = $codeFile.BaseName
    if ($baseName.EndsWith("_code")) { $baseName = $baseName.Substring(0, $baseName.Length - 5) }

    Write-Host "[$($fig.Chapter)] $baseName ... " -NoNewline

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
        if (Test-Path "$buildDir\$baseName-1.png") {
            Move-Item "$buildDir\$baseName-1.png" "$buildDir\$baseName.png" -Force
        }
        if (Test-Path "$buildDir\$baseName.png") {
            Write-Host "OK" -ForegroundColor Green
        } else {
            Write-Host "OK (PDF only)" -ForegroundColor Yellow
        }
        $successCount++

        Add-Content -Path $figDraw -Value "\input{$relPath}" -Encoding UTF8
        Add-Content -Path $figDraw -Value "" -Encoding UTF8
    } else {
        Write-Host "Failed" -ForegroundColor Red
        Get-Content (Join-Path $buildDir "__fig_temp.log") -ErrorAction SilentlyContinue | Select-String "^!" | Select-Object -First 10
        $failCount++
    }
}

Add-Content -Path $figDraw -Value "\end{document}" -Encoding UTF8

Write-Host ""
Write-Host "Done: $successCount succeeded, $failCount failed" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Yellow" })
Write-Host "Output: $buildDir"
