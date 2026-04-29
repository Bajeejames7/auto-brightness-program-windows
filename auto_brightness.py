import cv2
import numpy as np
import time
import wmi

class StealthBrightness:
    def __init__(self, camera_index=0):
        self.index = camera_index
        # Direct connection to Windows Monitor Brightness methods
        self.conn = wmi.WMI(namespace='root/WMI')
        self.monitor = self.conn.WmiMonitorBrightnessMethods()[0]

    def set_brightness(self, level):
        """Kernel-level brightness set."""
        self.monitor.WmiSetBrightness(int(level), 1)

    def get_ambient_flux(self):
        """
        The 'Flash' method: 
        Fastest possible capture to minimize 'Green Light' time.
        """
        # CAP_DSHOW bypasses the heavy Windows Media Foundation overhead
        cap = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
        if not cap.isOpened():
            return None

        # Optimization: Don't just resize—request the smallest raw buffer
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 16)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 16)

        # Grab only 1 frame to minimize 'on' time. 
        # (If too dark, change range to 2)
        ret, frame = cap.read()
        cap.release() # LED turns off immediately here

        if ret:
            # CPU Optimization: Simple mean of a tiny array
            return (np.mean(frame) / 255) * 100
        return None

def main():
    # 60 seconds is the sweet spot for battery life vs responsiveness
    INTERVAL = 60 
    
    agent = StealthBrightness(camera_index=0)
    last_b = None

    print("=== Stealth Auto-Brightness Active ===")
    print(f"Polling every {INTERVAL}s. Run as Admin for best results.")

    try:
        while True:
            light = agent.get_ambient_flux()
            
            if light is not None:
                # Quadratic curve: better for human eye perception
                target = 10 + (np.sqrt(light / 100) * 90)
                
                # Only wake the CPU for a change > 10%
                if last_b is None or abs(target - last_b) > 10:
                    agent.set_brightness(target)
                    last_b = target
                    print(f"Adjusted: {int(target)}% (Light: {int(light)}%)")
            
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nShutting down.")

if __name__ == "__main__":
    main()