$fig  = $PSScriptRoot
$root = Split-Path $fig
$out  = "$fig\fig_draw.tex"

$chapters = @("Mechanics", "Electrodynamics", "Optics", "MathTool", "Statistics")

$files = Get-ChildItem "$root\chapters" -Recurse -Filter "*_code.tex" |
    Where-Object FullName -notmatch "\\build\\"

$lines = @(
"\documentclass[tikz,border=5pt]{standalone}"
"\input{fig_config.tex}"
"\begin{document}"
""
)

$i = 1
foreach ($ch in $chapters) {
    $chapterFiles = $files | Where-Object { $_.FullName -like "*\chapters\$ch\*" }
    if (-not $chapterFiles) { continue }

    $lines += "% ==================== Chapter ${i}: $ch ===================="

    $sections = $chapterFiles |
        ForEach-Object {
            ($_.FullName.Substring(("$root\chapters\$ch\").Length) -split "\\")[0]
        } |
        Sort-Object -Unique

    $j = 1
    foreach ($sec in $sections) {
        $lines += "% Section $i.${j}: $sec"

        $chapterFiles |
            Where-Object { $_.FullName -like "*\chapters\$ch\$sec\*" } |
            Sort-Object FullName |
            ForEach-Object {
                $rel = [IO.Path]::GetRelativePath($fig, $_.FullName) -replace "\\", "/"
                $lines += "%\input{$rel}"
            }

        $lines += ""
        $j++
    }

    $i++
}

$lines += "\end{document}"

[IO.File]::WriteAllLines($out, $lines, [Text.UTF8Encoding]::new($false))
Write-Host "updated: $out"
