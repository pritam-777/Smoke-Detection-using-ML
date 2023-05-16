from smoke.pipeline.training_pipeline import start_training_pipeline
from smoke.pipeline.batch_prediction import start_batch_prediction

#file_path="D:/Project/Smoke Detection Dataset/smoke_detection_iot.csv"
file_path="D:/Project2/smoke_detection_iot.csv"
#print(__name__)
if __name__=="__main__":
     try:
          #start_training_pipeline()
          output_file = start_batch_prediction(input_file_path=file_path)
          #output = start_training_pipeline()
          #print(output_file)
          print(output_file)
     except Exception as e:
          print(e)