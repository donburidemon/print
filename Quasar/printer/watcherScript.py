import subprocess
import time
import logging
from datetime import datetime
import platform  # Required for OS detection

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('print_queue_monitor.log'),
        logging.StreamHandler()
    ]
)

PRINTER_NAME = "right-printer"
INTERVAL_SECONDS = 5  # Check every 5 seconds

class PrinterMock:
    def __init__(self):
        self.job_counter = 1
        
    def generate_mock_jobs(self):
        """Creates realistic mock print jobs"""
        self.job_counter += 1
        current_time = datetime.now().strftime('%a %b %d %H:%M:%S %Y')
        
        # Simulate 1-3 random jobs
        num_jobs = self.job_counter % 3 + 1  
        jobs = []
        for i in range(num_jobs):
            jobs.append(
                f"{PRINTER_NAME}-{self.job_counter+i} user{i+1} {1024*(i+1)} {current_time}"
            )
        return "\n".join(jobs) if jobs else "no entries"

printer_mock = PrinterMock()

def get_print_queue():
    try:
        if platform.system() == "Windows":
            # Windows mock mode
            return printer_mock.generate_mock_jobs()
        else:
            # Real Linux mode
            result = subprocess.run(
                ["lpstat", "-o", PRINTER_NAME],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return result.stdout.strip()
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return None

def main():
    #logging.info(f"Starting print queue monitor for printer: {PRINTER_NAME}")
    #logging.info(f"Checking every {INTERVAL_SECONDS} seconds (Ctrl+C to stop)")
    
    try:
        while True:
            queue_info = get_print_queue()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if queue_info:
                logging.info(f"{timestamp} - Print queue status:\n{queue_info}")
            else:
                logging.info(f"{timestamp} - No queue information available")
            
            time.sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user")

if __name__ == "__main__":
    main()