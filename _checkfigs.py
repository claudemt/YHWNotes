import pathlib, re, collections

root = pathlib.Path("content/YHWNotes")
fig_root = root / "figures"

# 收集 figures 目录下所有文件（相对 figures 的路径 + 纯文件名）
fig_files = {}
for p in fig_root.rglob("*"):
    if p.is_file():
        fig_files[p.name] = p  # 文件名 -> 路径（可能有重名，记录最后一个）

# 收集 figures 下所有文件名（用于按名查找）
all_fig_names = set(fig_files.keys())

# 提取 ch*.tex 中的 includegraphics 文件名
img_pat = re.compile(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}')
input_pat = re.compile(r'\\input\{([^}]+)\}')

missing_img = collections.defaultdict(list)
missing_input = collections.defaultdict(list)
found_img = collections.Counter()
found_input = collections.Counter()

tex_files = sorted(root.glob("ch*.tex")) + [root / "YHWNotes.tex"]
for tf in tex_files:
    t = tf.read_text(encoding="utf-8")
    for m in img_pat.finditer(t):
        name = m.group(1).strip()
        # 取纯文件名
        base = pathlib.PurePosixPath(name).name
        if base in all_fig_names:
            found_img[base] += 1
        else:
            line = t.count("\n", 0, m.start()) + 1
            missing_img[base].append((tf.name, line))
    for m in input_pat.finditer(t):
        name = m.group(1).strip()
        # 只关心 figures 相关 / tikz / 相对路径的 input
        base = pathlib.PurePosixPath(name).name
        # 跳过 content/ 完整路径的章文件 input
        if name.startswith("content/"):
            continue
        if base:
            # 是否为已存在的文件（相对 figures 或相对 root）
            if (root / name).exists() or (fig_root / name).exists() or base in all_fig_names:
                found_input[base] += 1
            else:
                line = t.count("\n", 0, m.start()) + 1
                missing_input[name].append((tf.name, line))

print("=== 缺失的图片 (includegraphics) ===")
if not missing_img:
    print("  无缺失")
for name, locs in sorted(missing_img.items()):
    print(f"  {name}: {locs}")

print("\n=== 缺失的 input (相对路径) ===")
if not missing_input:
    print("  无缺失")
for name, locs in sorted(missing_input.items()):
    print(f"  {name}: {locs}")

print("\n=== 引用的图片总数 ===")
print("  唯一图片名:", len(found_img))

# 对比：figures/generated 里的文件有多少被引用
gen_names = set(p.name for p in (fig_root / "generated").glob("*") if p.is_file())
unused_gen = gen_names - set(found_img.keys())
print("\n=== figures/generated 中未被引用的文件（可能冗余，仅供参考）===")
for n in sorted(unused_gen):
    print("  ", n)