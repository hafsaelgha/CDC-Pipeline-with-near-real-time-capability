import sys
import logging
import time
import json
from amazon_kclpy import kcl

#Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class RecordProcessor(kcl.RecordProcessorBase):
    def __init__(self):
        super(RecordProcessor, self).__init__()

    def process_record(self, data, partition_key, sequence_number):
    
        # Convert the data from bytes to string
        data_str = data.decode('utf-8')

        # Parse the data as a JSON object
        try:
            record_data = json.loads(data_str)
            operation = record_data['operation']
        
            print(f"Received record: SequenceNumber: {sequence_number}, Operation: {operation}, Data: {data_str}")
        except : 
            return kcl.RecordProcessorBase.RecordProcessingStatus.ERROR

        return kcl.RecordProcessorBase.RecordProcessingStatus.SUCCESS

if __name__ == "__main__":
    #Create a Kinesis application
    kcl_process = kcl.KCLProcess(RecordProcessor())

    #Start the Kinesis application
    kcl_process.run()
