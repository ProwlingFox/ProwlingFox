import pprint
from importlib import reload
import traceback
import JobsiteSniffers.workableJobsniffer as w

while True:
    try:
        reload(w)
        workableJobsniffer = w.workableJobsniffer({
            "enabled": True,
            "fakeApply": True
        })
        for job in workableJobsniffer:
            pprint.pprint(job)
            
            break
    except Exception as e:
        print("Error", e)
        print(traceback.format_exc())

    input("?????????????getNext???????????????")