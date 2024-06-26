# yolo_utils.py
import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

class YOLOSegmentation:
    def __init__(self, model_path, threshold=0.6):
        self.model = YOLO(model_path)
        self.names = self.model.model.names
        self.threshold = threshold

    def process_frame(self, frame):
        results = self.model.predict(frame)
        annotator = Annotator(frame, line_width=2)

        if results[0].masks is not None:
            clss = results[0].boxes.cls.cpu().tolist()
            confidences = results[0].boxes.conf.cpu().tolist()
            masks = results[0].masks.xy

            for mask, cls, confidence in zip(masks, clss, confidences):
                if confidence > self.threshold:
                    mask_fill_color = colors(int(cls), True)
                    filled_mask = frame.copy()
                    cv2.fillPoly(filled_mask, [mask.astype(int)], mask_fill_color)

                    alpha = 0.4
                    cv2.addWeighted(filled_mask, alpha, frame, 1 - alpha, 0, frame)

                    annotator.seg_bbox(mask=mask,
                                       mask_color=colors(int(cls), True),
                                       det_label=f"{self.names[int(cls)]} {confidence:.2f}")

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        return frame_bytes
