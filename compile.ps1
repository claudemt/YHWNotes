$ROOT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ROOT_DIR
function Pause-And-Exit { param([int]$Code = 0) exit $Code }
function Read-Default {
    param([string]$Prompt, [string]$Default)
    $v = Read-Host $Prompt
    if ([string]::IsNullOrWhiteSpace($v)) { return $Default }
    return $v.Trim()
}
function Get-RelPath {
    param([string]$BasePath, [string]$TargetPath)
    $baseUri = [Uri]((Resolve-Path $BasePath).Path.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar)
    $targetUri = [Uri]((Resolve-Path $TargetPath).Path)
    return [Uri]::UnescapeDataString($baseUri.MakeRelativeUri($targetUri).ToString())
}
function Remove-OuterSpaces {
    param([string]$Text)
    return ($Text -replace '^[\s　]+', '' -replace '[\s　]+$', '')
}
function Remove-CompileArtifacts {
    for ($attempt = 1; $attempt -le 5; $attempt++) {
        $rootTempNames = @(
            "__compile_temp.tex",
            "__compile_temp.aux",
            "__compile_temp.log",
            "__compile_temp.out",
            "__compile_temp.toc",
            "main.aux",
            "main.log",
            "main.out",
            "main.toc",
            "main.synctex.gz",
            "texput.log",
            "missfont.log"
        )
        foreach ($name in $rootTempNames) {
            Remove-Item -LiteralPath (Join-Path $ROOT_DIR $name) -Force -ErrorAction SilentlyContinue
        }
        Get-ChildItem -LiteralPath $buildDir -File -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.Extension -ne ".pdf" } |
            Remove-Item -Force -ErrorAction SilentlyContinue
        Get-ChildItem -LiteralPath $buildDir -Directory -Recurse -ErrorAction SilentlyContinue |
            Sort-Object FullName -Descending |
            Where-Object { -not (Get-ChildItem -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue) } |
            Remove-Item -Force -ErrorAction SilentlyContinue
        $remaining = @(Get-ChildItem -LiteralPath $buildDir -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Extension -ne ".pdf" })
        if ($remaining.Count -eq 0) { break }
        Start-Sleep -Milliseconds 400
    }
}
function Get-LatexHeading {
    param([string]$Line)
    $trim = $Line.TrimStart()
    if ($trim.StartsWith("%")) { return $null }
    if ($Line -notmatch '^\s*\\(section|subsection)\*?\s*(\[[^\]]*\])?\s*\{') { return $null }
    $level = $matches[1]
    $braceStart = $Line.IndexOf('{')
    if ($braceStart -lt 0) { return $null }
    $depth = 0
    $titleChars = New-Object System.Collections.Generic.List[char]
    for ($i = $braceStart; $i -lt $Line.Length; $i++) {
        $ch = $Line[$i]; $escaped = ($i -gt 0 -and $Line[$i - 1] -eq '\')
        if ($ch -eq '{' -and -not $escaped) { if ($depth -gt 0) { $titleChars.Add($ch) }; $depth++; continue }
        if ($ch -eq '}' -and -not $escaped) { $depth--; if ($depth -eq 0) { break }; $titleChars.Add($ch); continue }
        if ($depth -gt 0) { $titleChars.Add($ch) }
    }
    return [PSCustomObject]@{ Level = $level; Title = (Remove-OuterSpaces (-join $titleChars)) }
}
function Parse-TexFile {
    param([string]$FullName, [string]$RelPath)
    $lines = [IO.File]::ReadAllLines($FullName)
    $sections = @(); $currentSec = $null; $currentSub = $null
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $h = Get-LatexHeading $lines[$i]; if ($null -eq $h) { continue }
        if ($h.Level -eq "section") {
            if ($null -ne $currentSub) { $currentSub.EndLine = $i - 1; $currentSub = $null }
            if ($null -ne $currentSec) { $currentSec.EndLine = $i - 1; $sections += $currentSec }
            $currentSec = [PSCustomObject]@{ Title = $h.Title; FullName = $FullName; RelPath = $RelPath; Lines = $lines; StartLine = $i; EndLine = $lines.Count - 1; Subsections = @() }
        }
        if ($h.Level -eq "subsection" -and $null -ne $currentSec) {
            if ($null -ne $currentSub) { $currentSub.EndLine = $i - 1 }
            $currentSub = [PSCustomObject]@{ Title = $h.Title; StartLine = $i; EndLine = $lines.Count - 1; Index = $currentSec.Subsections.Count + 1 }
            $currentSec.Subsections += $currentSub
        }
    }
    if ($null -ne $currentSub) { $currentSub.EndLine = $lines.Count - 1 }
    if ($null -ne $currentSec) { $currentSec.EndLine = $lines.Count - 1; $sections += $currentSec }
    return $sections
}
$texCmd = (Get-Command "xelatex").Source
$buildDir = Join-Path $ROOT_DIR "build"
New-Item -ItemType Directory -Force -Path $buildDir | Out-Null
$preambleText = [IO.File]::ReadAllText((Join-Path $ROOT_DIR "preamble.tex"))
$tocDepth = 2
if ($preambleText -match '\\setcounter\{tocdepth\}\{(\d+)\}') { $tocDepth = [int]$matches[1] }
$chapterSpecs = @(
    [PSCustomObject]@{ Path = "Mechanics";       Title = "力学" },
    [PSCustomObject]@{ Path = "Electrodynamics"; Title = "电学" },
    [PSCustomObject]@{ Path = "Statistics";      Title = "热学" },
    [PSCustomObject]@{ Path = "Optics";          Title = "光学" },
    [PSCustomObject]@{ Path = "MathTool";        Title = "数学工具" }
)
$chapters = @(); $sectionMap = @{}; $globalSectionNo = 0; $chapterNo = 0
foreach ($spec in $chapterSpecs) {
    $chapterDir = Join-Path (Join-Path $ROOT_DIR "chapters") $spec.Path
    if (-not (Test-Path $chapterDir)) { continue }
    $chapterNo++; $ch = [PSCustomObject]@{ No = $chapterNo; Path = $spec.Path; Title = $spec.Title; Sections = @(); Files = @() }
    foreach ($td in (Get-ChildItem -Path $chapterDir -Directory | Sort-Object Name)) {
        foreach ($f in (Get-ChildItem -Path $td.FullName -File -Filter "*.tex" | Where-Object { -not $_.Name.StartsWith("_") -and -not $_.Name.StartsWith(".") -and $_.Name -ne "preamble.tex" } | Sort-Object Name)) {
            $rel = (Get-RelPath $ROOT_DIR $f.FullName) -replace '\\', '/'
            $sections = Parse-TexFile $f.FullName $rel; if ($sections.Count -eq 0) { continue }
            $fileObj = [PSCustomObject]@{ FullName = $f.FullName; RelPath = $rel; Sections = @() }
            foreach ($sec in $sections) {
                $globalSectionNo++
                Add-Member -InputObject $sec -NotePropertyName No -NotePropertyValue $globalSectionNo
                Add-Member -InputObject $sec -NotePropertyName Chapter -NotePropertyValue $ch
                for ($si = 0; $si -lt $sec.Subsections.Count; $si++) {
                    $sub = $sec.Subsections[$si]
                    Add-Member -InputObject $sub -NotePropertyName No -NotePropertyValue ("$globalSectionNo.$($si + 1)")
                }
                $sectionMap[[string]$globalSectionNo] = $sec
                $ch.Sections += $sec; $fileObj.Sections += $sec
            }
            $ch.Files += $fileObj
        }
    }
    if ($ch.Sections.Count -gt 0) { $chapters += $ch }
}
if ($chapters.Count -eq 0) { Write-Host "Error: no sections found." -ForegroundColor Red; exit 1 }
Write-Host ""; Write-Host "Contents"; Write-Host ""
foreach ($ch in $chapters) {
    Write-Host ("  {0,-6} {1}" -f ("c" + $ch.No), ("Chapter " + $ch.No + " " + $ch.Title)) -ForegroundColor White
    if ($tocDepth -ge 1) {
        foreach ($sec in $ch.Sections) {
            Write-Host ("      {0,-7} {1}" -f $sec.No, $sec.Title)
            if ($tocDepth -ge 2) { foreach ($sub in $sec.Subsections) { Write-Host ("          {0,-7} {1}" -f $sub.No, $sub.Title) } }
        }
    }
}
$selChapters = @{}; $selSections = @{}; $defaultFullCompile = $false
while ($true) {
    $selection = Read-Host "`nContent IDs (e.g. c1,c2,12; Enter=all)"
    if ([string]::IsNullOrWhiteSpace($selection)) {
        foreach ($ch in $chapters) { $selChapters[[string]$ch.No] = $true }
        $defaultFullCompile = $true
        break
    }
    $selChapters = @{}; $selSections = @{}; $errors = @()
    $norm = $selection -replace '[，；;\s]+', ','
    foreach ($raw in ($norm.Split(',') | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })) {
        $token = $raw.Trim().ToLower()
        if ($token -eq "all" -or $token -eq "a") { foreach ($ch in $chapters) { $selChapters[[string]$ch.No] = $true }; continue }
        if ($token -match '^c(\d+)$') { $n = [int]$matches[1]; if ($chapters | Where-Object { $_.No -eq $n }) { $selChapters[[string]$n] = $true } else { $errors += $raw }; continue }
        if ($token -match '^c(\d+)-c?(\d+)$') { $a = [int]$matches[1]; $b = [int]$matches[2]; if ($a -gt $b) { $t = $a; $a = $b; $b = $t }; for ($n = $a; $n -le $b; $n++) { if ($chapters | Where-Object { $_.No -eq $n }) { $selChapters[[string]$n] = $true } else { $errors += "c$n" } }; continue }
        if ($token -match '^(\d+)$') { $n = $matches[1]; if ($sectionMap.ContainsKey($n)) { $selSections[$n] = $true } else { $errors += $raw }; continue }
        if ($token -match '^(\d+)-(\d+)$') { $a = [int]$matches[1]; $b = [int]$matches[2]; if ($a -gt $b) { $t = $a; $a = $b; $b = $t }; for ($n = $a; $n -le $b; $n++) { $k = [string]$n; if ($sectionMap.ContainsKey($k)) { $selSections[$k] = $true } else { $errors += $k } }; continue }
        $errors += $raw
    }
    foreach ($k in @($selSections.Keys)) { $sec = $sectionMap[$k]; if ($selChapters.ContainsKey([string]$sec.Chapter.No)) { $selSections.Remove($k) } }
    if ($errors.Count -gt 0) { Write-Host "Unrecognized IDs: $($errors -join ', ')" -ForegroundColor Yellow; Write-Host "Note: chapters use c prefix (e.g. c1); numbers alone refer to sections (e.g. 12)." -ForegroundColor Yellow; continue }
    if ($selChapters.Count -eq 0 -and $selSections.Count -eq 0) { Write-Host "No valid selection, try again." -ForegroundColor Yellow; continue }
    $defaultFullCompile = $false
    break
}
if ($defaultFullCompile) {
    $genTitle = "y"
    $genToc = "y"
} else {
    $genTitle = Read-Default "Generate cover [y/n, Enter=n]" "n"
    $genToc = Read-Default "Generate TOC [y/n, Enter=n]" "n"
}
$mainLines = [System.Collections.Generic.List[string]]::new()
$mainLines.Add("\documentclass[UTF8,openany]{ctexbook}")
$mainLines.Add("\input{preamble.tex}")
$mainLines.Add(""); $mainLines.Add("\begin{document}"); $mainLines.Add("")
if ($genTitle -eq "y" -or $genTitle -eq "Y") {
    $mainLines.Add("\begin{titlepage}"); $mainLines.Add("\centering"); $mainLines.Add("\vspace*{4cm}")
    $mainLines.Add("{\Huge\bfseries 忆灰的物理笔记\par}"); $mainLines.Add("\vspace*{3.5cm}")
    $mainLines.Add("{\Large 忆灰芜\par}"); $mainLines.Add("\vspace*{1.8cm}")
    $mainLines.Add("{\large \today\par}"); $mainLines.Add("\vfill"); $mainLines.Add("\end{titlepage}"); $mainLines.Add("")
}
if ($genToc -eq "y" -or $genToc -eq "Y") { $mainLines.Add("\tableofcontents"); $mainLines.Add("\clearpage"); $mainLines.Add("") }
$isFullCompile = ($selChapters.Count -eq $chapters.Count)
foreach ($ch in $chapters) {
    $chapterSelected = $selChapters.ContainsKey([string]$ch.No)
    if (-not $chapterSelected) {
        $hasSelected = $false
        foreach ($sec in $ch.Sections) { if ($selSections.ContainsKey([string]$sec.No)) { $hasSelected = $true; break } }
        if (-not $hasSelected) { continue }
    }
    if ($isFullCompile) { $mainLines.Add("\setcounter{chapter}{$($ch.No - 1)}"); $mainLines.Add("\chapter{$($ch.Title)}"); $mainLines.Add("") }
    foreach ($file in $ch.Files) {
        if ($file.Sections.Count -eq 0) { continue }
        if (-not $chapterSelected) {
            $hasSec = $false
            foreach ($sec in $file.Sections) { if ($selSections.ContainsKey([string]$sec.No)) { $hasSec = $true; break } }
            if (-not $hasSec) { continue }
        }
        $relDir = ([IO.Path]::GetDirectoryName($file.RelPath) -replace '\\', '/')
        if ($isFullCompile) { $firstSecNo = ($file.Sections | Sort-Object No | Select-Object -First 1).No; $mainLines.Add("\setcounter{section}{$($firstSecNo - 1)}") }
        $mainLines.Add("\subimport{$relDir/}{$([IO.Path]::GetFileName($file.RelPath))}"); $mainLines.Add("\clearpage"); $mainLines.Add("")
    }
}
$mainLines.Add("\end{document}")
$mainTex = Join-Path $ROOT_DIR "main.tex"
[IO.File]::WriteAllLines($mainTex, $mainLines, [Text.UTF8Encoding]::new($false))
Write-Host "Compiling..."
Write-Host "Updated main.tex"
Remove-CompileArtifacts
& $texCmd -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$buildDir" $mainTex *>$null 2>&1
& $texCmd -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$buildDir" $mainTex *>$null 2>&1
$tempPdf = Join-Path $buildDir "main.pdf"
if (Test-Path $tempPdf) {
    Write-Host "Compilation successful" -ForegroundColor Green
    if ($defaultFullCompile) {
        $outName = "compile.pdf"
    } else {
        $outName = Read-Default "Output name [Enter=compile.pdf]" "compile.pdf"
    }
    if (-not $outName.EndsWith(".pdf")) { $outName += ".pdf" }
    $outPath = Join-Path $buildDir $outName
    if (([IO.Path]::GetFullPath($tempPdf)) -ne ([IO.Path]::GetFullPath($outPath))) {
        $moved = $false
        for ($attempt = 1; $attempt -le 5; $attempt++) {
            try {
                Move-Item $tempPdf $outPath -Force -ErrorAction Stop
                $moved = $true
                break
            } catch {
                if ($attempt -lt 5) { Start-Sleep -Milliseconds 500 }
            }
        }
        if (-not $moved) {
            Copy-Item $tempPdf $outPath -Force
            Remove-Item $tempPdf -Force
            Write-Host "Note: PDF was copied (previous output may still be locked by PDF viewer)." -ForegroundColor Yellow
        }
    }
    Remove-CompileArtifacts
    if (Test-Path $outPath) {
        Start-Process $outPath
    } else {
        Write-Host "Output path not found: $outPath" -ForegroundColor Red
    }
} else {
    Write-Host "Failed" -ForegroundColor Red
    $logPath = Join-Path $buildDir "main.log"
    Get-Content $logPath -ErrorAction SilentlyContinue | Select-String "^!" | Select-Object -First 10
    Remove-CompileArtifacts
    exit 1
}