#!/usr/bin/env python3
"""
Simple A2A System Runner with real-time output for debugging
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path

# Add the strands-a2a-inter-agent directory to Python path
SCRIPT_DIR = Path(__file__).parent
A2A_DIR = SCRIPT_DIR / "strands-a2a-inter-agent"

def cleanup_ports():
    """Clean up any processes using the required ports"""
    ports = [8000, 8001, 8002]
    for port in ports:
        try:
            result = subprocess.run(['lsof', '-ti', f':{port}'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        subprocess.run(['kill', '-9', pid], check=False)
                        print(f"🧹 Killed process {pid} using port {port}")
                    except:
                        pass
        except:
            pass

def stream_output(process, name):
    """Stream process output in real-time"""
    for line in iter(process.stdout.readline, ''):
        if line:
            print(f"[{name}] {line.rstrip()}")

def main():
    print("🚀 Simple A2A System Runner")
    print("=" * 40)
    
    # The agents use Amazon Bedrock (Claude Haiku 5.5 via the global inference profile),
    # so AWS credentials must be available in the environment or the AWS CLI config.
    print(f"☁  Bedrock region: {os.getenv('AWS_REGION', 'us-east-1')} | model: {os.getenv('BEDROCK_MODEL_ID', 'global.anthropic.claude-haiku-5-5')}")
    
    # Clean up ports
    print("🧹 Cleaning up ports...")
    cleanup_ports()
    time.sleep(1)
    
    processes = []
    
    try:
        # Start MCP Server
        print("\n🚀 Starting MCP Server...")
        mcp_process = subprocess.Popen(
            [sys.executable, "server.py"],
            cwd=str(A2A_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(mcp_process)
        
        # Start output streaming thread
        mcp_thread = threading.Thread(target=stream_output, args=(mcp_process, "MCP"))
        mcp_thread.daemon = True
        mcp_thread.start()
        
        print("⏳ Waiting for MCP Server to start...")
        time.sleep(5)
        
        # Start Employee Agent
        print("\n🤖 Starting Employee Agent...")
        employee_process = subprocess.Popen(
            [sys.executable, "employee-agent.py"],
            cwd=str(A2A_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(employee_process)
        
        # Start output streaming thread
        employee_thread = threading.Thread(target=stream_output, args=(employee_process, "EMPLOYEE"))
        employee_thread.daemon = True
        employee_thread.start()
        
        print("⏳ Waiting for Employee Agent to start...")
        time.sleep(5)
        
        # Start HR Agent
        print("\n👥 Starting HR Agent...")
        hr_process = subprocess.Popen(
            [sys.executable, "hr-agent.py"],
            cwd=str(A2A_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(hr_process)
        
        # Start output streaming thread
        hr_thread = threading.Thread(target=stream_output, args=(hr_process, "HR"))
        hr_thread.daemon = True
        hr_thread.start()
        
        print("⏳ Waiting for HR Agent to start...")
        time.sleep(5)
        
        print("\n🎉 All services started!")
        print("=" * 40)
        print("Press Ctrl+C to stop all services")
        print("=" * 40)
        
        # Keep running and monitor processes
        while True:
            # Check if any process has died
            for i, process in enumerate(processes):
                if process.poll() is not None:
                    service_names = ["MCP Server", "Employee Agent", "HR Agent"]
                    print(f"\n❌ {service_names[i]} has stopped!")
                    return
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Received interrupt signal, shutting down...")
    
    finally:
        print("🧹 Cleaning up processes...")
        for process in processes:
            if process.poll() is None:
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()

if __name__ == "__main__":
    main()
