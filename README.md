# YHWNotes

用 LaTeX 编写的物理讲义。一个仓库容纳多本书，覆盖力学、电动力学、统计物理、光学与数学工具。

## 技术栈

- **XeLaTeX** (`ctexbook`) 排版，中英混排
- **biblatex + biber** 参考文献
- **TikZ / tikz-3dplot / circuitikz** 矢量图，**Python (matplotlib)** 定量图
- **Python** 构建驱动 (`main.py`)，一键编译成书

## 目录结构

```text
YHWNotes/
├── main.tex                 # 通用入口（多书共用）
├── preamble.tex             # 公共宏包、页面样式、编号、盒子、数学命令
├── main.py                  # 构建驱动
├── SKILL.md                 # 讲义编写与工程规范
└── content/
    ├── AdvancedPhysics/
    ├── FreeElectronQuantumOptics/
    ├── GroupTheory/
    ├── MathSkills/
    └── YHWNotes/            # 一本讲义的唯一入口
        ├── YHWNotes.tex
        ├── ch01.tex ...     # 章文件
        ├── sections/        # 章内需要继续拆分的稳定模块
        ├── frontmatter/     # 前置材料
        ├── backmatter/      # 附录、索引
        ├── figures/         # 图
        ├── settings.tex     # 本书专用记号与宏包
        └── references.bib
```

## 构建

```bash
python main.py list                              # 列出所有书
python main.py build YHWNotes                    # 编译一本
python main.py build YHWNotes --figures          # 先跑图脚本再编译
python main.py build --all                       # 编译全部
```

产物在 `build/<书名>/main.pdf`，同时复制一份到 `example/<书名>.pdf`。两者都不进版本库。

## 依赖

XeLaTeX、biber、xdvipdfmx（TeX Live 2024 已验证），Python 3.11+。

## 编写规范

讲义的组织方式、数学要求、图形约定与 LaTeX 工程规范见 [SKILL.md](SKILL.md)。

## License

CC BY-NC-ND 4.0
