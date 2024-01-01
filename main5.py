import asyncio
import sys
import asyncio.subprocess

async def run_uvicorn():
    # Replace 'your_fastapi_module:app' with the actual module and app instance you want to run
    # command = 'uvicorn pytorch_solver:app --host 192.168.0.130 --port 8001'
    command = [
        sys.executable,  # Path to the Python interpreter
        '-m', 'uvicorn',
        'pytorch_solver:app',
        '--host', '192.168.0.130',  # Adjust the host and port as needed
        '--port', '8001',
        # '--reload',  # Enable auto-reload for development
    ]

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    async def read_stream(stream, name):
        while True:
            line = await stream.readline()
            if not line:
                break
            print(f"{name}: {line.strip()}")
    
    # Start tasks to read stdout and stderr concurrently
    stdout_task = asyncio.create_task(read_stream(process.stdout, 'stdout'))
    stderr_task = asyncio.create_task(read_stream(process.stderr, 'stderr'))


    # # Read output asynchronously
    # while True:
    #     try:
    #         stdout_data = await asyncio.wait_for(process.stdout.readline(), timeout=1.0)
    #         stderr_data = await asyncio.wait_for(process.stderr.readline(), timeout=1.0)

    #         if not stdout_data and not stderr_data:
    #             break

    #         if stdout_data:
    #             print(f"stdout: {stdout_data.decode().strip()}")
    #         if stderr_data:
    #             print(f"stderr: {stderr_data.decode().strip()}")
    #     except asyncio.TimeoutError:
    #         print(f'timeout error. ')
    #         pass


    # Wait for the process to complete
    print(f'does this loop forever?')
    await process.wait()
    print(f'does this loop forever2?')
    

    # Wait for the reading tasks to complete
    await asyncio.gather(stdout_task, stderr_task)

async def main():
    # Run uvicorn in the background
    uvicorn_task = asyncio.create_task(run_uvicorn())

    # Continue with other asynchronous tasks if needed

    # Wait for uvicorn to complete (you can set a timeout if desired)
    await uvicorn_task
    print(f'uvicorn task finished. ')

if __name__ == "__main__":
    asyncio.run(main())
