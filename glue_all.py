import re
from pathlib import Path
from pprint import pprint
from textwrap import dedent, indent


indentation = 4 * " "

re_imports = re.compile(r"^import\s+(.+)\s*$", re.M)
re_from = re.compile(r"^from\s+(\S+)\s+import\s+(.+)$", re.M)
re_example = re.compile(r"^\s*EXAMPLE\s+=\s+(True|False)\s*$", re.M)
re_print_day = re.compile(r'^\s*print\("Day\s+\d+', re.M)
re_print_result = re.compile(r'print\(f?"Part ')

days, modules = {}, set()
partials = {"argparse": {"ArgumentParser"}, "time": {"perf_counter"}}
for file_path in Path().glob("day_*.py"):
    if "v1" in (name := file_path.name):
        continue
    
    day = int(name[4:6])
    content = file_path.read_text()

    # Extract the import information
    modules.update(m[1] for m in re_imports.finditer(content))
    for match in re_from.finditer(content):
        module, objects =  match[1], match[2].replace(",", " ").split()
        partials.setdefault(module, set()).update(objects)

    # Prepare the function definition
    content = re_example.sub("", content, count=1)
    content = re_print_day.sub("\g<0>:", content, count=1)
    content = re_print_result.sub('print(f"  - part ', content, count=2)
    start = 0
    if match := re_print_day.search(content):
        start = match.start()
    body = indent(content[start:].strip(), indentation)
    func = f"def day_{day}():\n{body}"
    days[day] = func    

# Consolidate the imports
partials = {module: sorted(partials[module]) for module in sorted(partials)}
days = {day: days[day] for day in sorted(days)}
strings = [f"import {module}" for module in sorted(modules)]
strings.extend(
    f"from {module} import {', '.join(objects)}"
    for module, objects in partials.items()
)
strings = ["\n".join(strings)]

# Add 2 options: (1) setting EXAMPLE = True globally, (2) select specific days
strings.append(
    dedent("""\
        parser = ArgumentParser()
        parser.add_argument("-e", "--example", action="store_true")
        parser.add_argument("-d", "--days", default="1-25")
        args = parser.parse_args()
        
        EXAMPLE = args.example
        
        interval = r"(\d{1,2}|\d{1,2}-\d{1,2})"
        if re.match(rf"{interval}(,{interval})*", args.days):
            days = set()
            for part in args.days.split(","):
                interval = tuple(map(int, part.split("-")))
                for n in interval:
                    if n == 0 or 25 < n:
                        parser.error(f"-d: wrong argument(s): {n}")
                start, stop = interval[0], interval[-1]
                if start != stop and stop < start:
                    parser.error(f"-d: wrong argument(s): {start} > {stop}")
                days.update(range(start, stop + 1))
        else:
            parser.error("-d: wrong format!")
        selected_days = tuple(sorted(days))\
        """
    )
)

# Add the functions
strings.extend(days[day] for day in days)
day_dict = ",\n".join(f"{day}: day_{day}" for day in days)
strings.append(f"days = {{\n{indent(day_dict, indentation)}\n}}")

# Add the part that actually runs the functions, including some time
# measurements
strings.append('if __name__ == "__main__":')
run_loop = dedent("""\
        total_ms = 0
        for day in selected_days:
            if day not in days: continue
            func = days[day]
            start = perf_counter()
            func()
            end = perf_counter()
            ms = (end - start) * 1_000
            print(f"  => run time: {ms:.0f} ms\\n")
            total_ms += ms
        print(f"\\n=> total run time: {total_ms:.0f} ms\\n")
        """
    )
strings.append(indent(run_loop, indentation))
file_str = "\n\n\n".join(strings)

# Finally write the run_all.py file
Path("run_all.py").write_text(file_str)
