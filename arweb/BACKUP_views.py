from pathlib import Path
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators import gzip
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
from .yolo_segmentation import YOLOSegmentation
import numpy as np
import time

def detect():
    relative_path = "speaker.pt"
    path = Path(__file__).resolve().parent.parent / "arweb/static" / relative_path

    model = YOLO(path)
    threshold = 0.4
    class_name_dict = {0: 'AC', 1: 'Mouse', 2: 'Fan'}

    cap = cv2.VideoCapture(0)
    # fps = 24  # Set your desired fps
    # frame_delay = 1 / fps

    while True:
        start_time = time.time()
        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)[0]

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            if score > threshold:
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
        elapsed_time = time.time() - start_time

        # if elapsed_time < frame_delay:
        #     time.sleep(frame_delay - elapsed_time)

    cap.release()

@gzip.gzip_page
def live_object_detection(request):
        return render(request, 'server/index.html')

def segment():
    model = YOLO("/Users/nichdylan/Documents/AR_Assembly/Remote model/yolov8n.pt")

    model_path = '/Users/nichdylan/Documents/AR_Assembly/arproject/arweb/static/speaker_segment.pt'
    model = YOLO(model_path)

    names = model.model.names #to find the name of the classes

    cap = cv2.VideoCapture(0)

    threshold = 0.7

    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

    out = cv2.VideoWriter('instance-segmentation.avi', cv2.VideoWriter_fourcc(*'MJPG'), fps, (w, h))

    while True:
        ret, im0 = cap.read()
        if not ret:
            print("Video frame is empty or video processing has been successfully completed.")
            break

        results = model.predict(im0)
        annotator = Annotator(im0, line_width=2)

        if results[0].masks is not None:
            clss = results[0].boxes.cls.cpu().tolist()
            confidences = results[0].boxes.conf.cpu().tolist()
            masks = results[0].masks.xy
            for mask, cls, confidence in zip(masks, clss, confidences):
                if confidence > threshold: 
                    mask_fill_color = colors(int(cls), True)
                    filled_mask = im0.copy()
                    cv2.fillPoly(filled_mask, [mask.astype(int)], mask_fill_color)

                    alpha = 0.4
                    cv2.addWeighted(filled_mask, alpha, im0, 1 - alpha, 0, im0)

                    annotator.seg_bbox(mask=mask,
                                    mask_color=colors(int(cls), True),
                                    det_label=f"{names[int(cls)]} {confidence:.2f}")

        ret, buffer = cv2.imencode('.jpg', im0)
        im0 = buffer.tobytes()
        yield (b'--im0\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + im0 + b'\r\n\r\n')
    cap.release()

def yolo_view(request):
    return render(request, 'arweb/detect.html')



# class ARView(View):
#     def get(self, request):
#         return render(request, 'arweb/ar.html')

# class YOLOv8Inference:
#     relative_path = "best.pt"
#     path = Path(__file__).resolve().parent.parent / "arweb/static" / relative_path

#     def __init__(self, model_path=path):
#         # Load the model and access its state dict
#         loaded_dict = torch.load(model_path)
#         self.model = loaded_dict['model'].fuse().eval()

#     def predict(self, frame):
#         # Process the frame and perform object detection
#         # ...

#         # For simplicity, returning the original frame for now
#         return frame
    
    
# def real_time_object_detection(request):
#     cap = cv2.VideoCapture(0)  # Use 0 for default camera, you may need to change it based on your setup
#     yolo = YOLOv8Inference()

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Perform YOLOv8 object detection on the frame
#         processed_frame = yolo.predict(frame)

#         # Display the frame in the Django template
#         _, buffer = cv2.imencode('.jpg', processed_frame)
#         img_str = buffer.tobytes()
#         img_data = 'data:image/jpg;base64,' + img_str.decode('utf-8')

#         return render(request, 'arweb/real_time_detection.html', {'img_data': img_data})

