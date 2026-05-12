$root = $PSScriptRoot
$out  = "$root\main.tex"

$chapters = @(
    @{ path = "Mechanics";       title = "力学" },
    @{ path = "Electrodynamics"; title = "电学" },
    @{ path = "Statistics";      title = "热学" },
    @{ path = "Optics";          title = "光学" },
    @{ path = "MathTool";        title = "数学工具" }
)

$lines = @(
"\documentclass[UTF8,openany]{ctexbook}"
"\input{preamble.tex}"
""
"\begin{document}"
""
"%\begin{titlepage}"
"%	\centering"
"%	\vspace*{4cm}"
"%	{\Huge\bfseries 忆灰的物理笔记\par}"
"%	\vspace*{3.5cm}"
"%	{\Large 忆灰芜\par}"
"%	\vspace*{1.8cm}"
"%	{\large \today\par}"
"%	\vfill"
"%\end{titlepage}"
"%\tableofcontents"
"%\clearpage"
""
)

foreach ($ch in $chapters) {
    $chapterDir = "$root\chapters\$($ch.path)"
    if (-not (Test-Path $chapterDir)) { continue }

    $lines += "%\chapter{$($ch.title)}"

    Get-ChildItem $chapterDir -Directory |
        Sort-Object Name |
        ForEach-Object {
            $tex = Get-ChildItem $_.FullName -File -Filter "*.tex" |
                Where-Object { $_.Name -ne "preamble.tex" } |
                Select-Object -First 1

            if ($tex) {
                $dir = [IO.Path]::GetRelativePath($root, $_.FullName) -replace "\\", "/"
                $lines += "%\subimport{$dir/}{$($tex.Name)}"
                $lines += "%\clearpage"
            }
        }

    $lines += ""
}

$lines += "\end{document}"

[IO.File]::WriteAllLines($out, $lines, [Text.UTF8Encoding]::new($false))
Write-Host "updated: $out"