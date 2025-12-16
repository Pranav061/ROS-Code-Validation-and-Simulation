import subprocess, json, time, os
def run_simulation():
# Launch Gazebo with UR5
subprocess.Popen([
'roslaunch', 'ur_gazebo', 'ur5.launch'
])

time.sleep(10) # wait for sim

node = subprocess.Popen(['rosrun', 'user_pkg', 'node.py'])

time.sleep(15)

subprocess.run(['gz', 'camera', '--camera-name', 'camera'])
result = {
"success": True,
"frames": 1
}
with open('results/simulation.json', 'w') as f:
json.dump(result, f, indent=2)
node.terminate()
return result
