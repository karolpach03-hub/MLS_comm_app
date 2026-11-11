import re
from pathlib import Path

def generate(header_path="com_protocol.h",output_path="com_protocol.py"):
	content=Path(header_path).read_text()

	constexprs=re.findall(r"constexpr\s+\w+\s+([A-Za-z0-9_]+)\s*=([^;]+);",content)
	enums=re.findall(r"enum\s+([A-Za-z0-9_]+)\s*:\s*\w+\s*\{([^}]+)\};",content)

	lines=["from dataclasses import dataclass",""]

	if constexprs:
		max_len=max(len(name) for name,_ in constexprs)
		max_prefix_len=max_len+4
		target_col=(max_prefix_len//4)+1
		for name,val in constexprs:
			prefix=f"{name}:int"
			tabs="\t"*(target_col-(len(prefix)//4))
			lines.append(f"{prefix}{tabs}={val.strip()}")
		lines.append("")

	for enum_name,body in enums:
		lines.append("@dataclass(frozen=True)")
		lines.append(f"class {enum_name}:")
		
		items=[]
		for line in body.splitlines():
			line=re.sub(r"//.*","",line)
			if not line.strip():
				continue
			for raw_item in line.split(","):
				raw_item=raw_item.strip()
				if "=" in raw_item:
					k,v=raw_item.split("=",1)
					items.append((k.strip(),v.strip()))

		if items:
			max_len=max(len(k) for k,_ in items)
			max_prefix_len=max_len+4
			target_col=(max_prefix_len//4)+1
			for k,v in items:
				prefix=f"{k}:int"
				tabs="\t"*(target_col-(len(prefix)//4))
				lines.append(f"\t{prefix}{tabs}={v.strip()}")
		lines.append("")

	Path(output_path).write_text("\n".join(lines)+"\n")

if __name__=="__main__":
	generate()