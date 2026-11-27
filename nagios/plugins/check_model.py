#!/usr/bin/env python3


import subprocess
#excecute external cmds
import sys
#read cli args

container = sys.argv[1]
#read container name from args

#excecute inside container
#load the model
#check if the model gives an output on the sample data
# if the prediction is provided : model is up

command = [
    "docker", "exec", container,
    "python", "-c",
    """
import pickle
import numpy as np

with open('/app/diabetes_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('/app/diabetes_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

features = np.array([[
    100, 5.5, 30, 24, 2, 80,
    120, 10, 12, 0, 0, 1
]])

scaled = scaler.transform(features)
model.predict(scaled)
model.predict_proba(scaled)
"""
]


try:
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)

    if result.returncode == 0:
        print("OK - Model is working in " + container)
        sys.exit(0)

    print("CRITICAL - Model failed in " + container)
    sys.exit(2)

except Exception:
    print("CRITICAL - Could not check model in " + container)
    sys.exit(2)
