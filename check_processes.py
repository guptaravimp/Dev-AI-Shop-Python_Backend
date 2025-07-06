#!/usr/bin/env python3
import os
import subprocess
import sys

def check_python_processes():
    """Check what Python processes are running"""
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                                  capture_output=True, text=True)
            print("Python processes running:")
            print(result.stdout)
        else:  # Mac/Linux
            result = subprocess.run(['ps', 'aux', '|', 'grep', 'python'], 
                                  capture_output=True, text=True, shell=True)
            print("Python processes running:")
            print(result.stdout)
    except Exception as e:
        print(f"Error checking processes: {e}")

def kill_python_processes():
    """Kill all Python processes"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                         capture_output=True, check=False)
            print("✅ Killed all Python processes")
        else:  # Mac/Linux
            subprocess.run(['pkill', '-f', 'python'], 
                         capture_output=True, check=False)
            print("✅ Killed all Python processes")
    except Exception as e:
        print(f"Error killing processes: {e}")

if __name__ == '__main__':
    print("🔍 Checking Python processes...")
    check_python_processes()
    
    print("\n🔄 Do you want to kill all Python processes? (y/n)")
    response = input().lower()
    
    if response == 'y':
        kill_python_processes()
        print("\n✅ Now restart your server with: python app.py")
    else:
        print("\n❌ Please manually kill Python processes and restart") 