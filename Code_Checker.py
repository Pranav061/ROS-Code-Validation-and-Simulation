import os, zipfile, subprocess, json, re


SAFE_JOINT_LIMIT = 3.14 # rad




def unzip(zip_path, out_dir):
with zipfile.ZipFile(zip_path, 'r') as z:
z.extractall(out_dir)




def check_ros_structure(path):
errors = []
if not any(f in os.listdir(path) for f in ['package.xml', 'setup.py']):
errors.append("Missing package.xml or setup.py")
return errors




def check_python_syntax(path):
errors = []
for root, _, files in os.walk(path):
for f in files:
if f.endswith('.py'):
res = subprocess.run(['python3', '-m', 'py_compile', os.path.join(root, f)],
capture_output=True, text=True)
if res.returncode != 0:
errors.append(res.stderr)
return errors




def detect_ros_usage(path):
info = {"publishers": 0, "subscribers": 0, "init_node": False}
for root, _, files in os.walk(path):
for f in files:
if f.endswith('.py'):
txt = open(os.path.join(root, f)).read()
info["publishers"] += len(re.findall(r'Publisher\(', txt))
info["subscribers"] += len(re.findall(r'Subscriber\(', txt))
if 'init_node' in txt:
info["init_node"] = True
return info




def safety_heuristics(path):
warnings = []
for root, _, files in os.walk(path):
for f in files:
if f.endswith('.py'):
txt = open(os.path.join(root, f)).read()
if 'while True' in txt and 'sleep' not in txt:
warnings.append("Infinite loop without sleep detected")
if re.search(r'joint.*=\s*([0-9\.]+)', txt):
val = float(re.search(r'joint.*=\s*([0-9\.]+)', txt).group(1))
if abs(val) > SAFE_JOINT_LIMIT:
warnings.append("Joint command exceeds safe limit")
return warnings




def run_all(zip_file):
workdir = 'uploads/code'
unzip(zip_file, workdir)


report = {
"structure": check_ros_structure(workdir),
"syntax": check_python_syntax(workdir),
"ros_usage": detect_ros_usage(workdir),
"warnings": safety_heuristics(workdir)
}


with open('results/report.json', 'w') as f:
json.dump(report, f, indent=2)


with open('results/report.txt', 'w') as f:
for k, v in report.items():
f.write(f"{k}: {v}\n")


return report
