import subprocess
import time
import json
from zmqRemoteApi import RemoteAPIClient

COPPELIA_PATH = "./CoppeliaSim_Edu/coppeliaSim.sh"
SCENE_PATH = "simple_arm_scene.ttt"

def run_simulation():

subprocess.Popen([COPPELIA_PATH, SCENE_PATH])
time.sleep(6) # wait for simulator

client = RemoteAPIClient()
sim = client.getObject('sim')

sim.startSimulation()

subprocess.Popen(['rosrun', 'user_pkg', 'node.py'])
time.sleep(10)

cube = sim.getObject('/cube')
target = sim.getObject('/target')
cube_pos = sim.getObjectPosition(cube, -1)
target_pos = sim.getObjectPosition(target, -1)
dist = sum((cube_pos[i] - target_pos[i])**2 for i in range(3)) ** 0.5
success = dist < 0.05

sim.saveImage('results/frame.png', 0)

sim.stopSimulation()
result = {
"success": success,
"distance_to_target": dist
}
with open('results/simulation.json', 'w') as f:
json.dump(result, f, indent=2)
return result
