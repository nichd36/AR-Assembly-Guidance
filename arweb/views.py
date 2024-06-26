
from django.shortcuts import redirect, render
from functools import wraps
import json
import cv2
import numpy as np
import base64
import asyncio

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

from arweb.models import Product

import torch

def login_required_redirect_home(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Assuming 'home' is the name of your home URL pattern
        return view_func(request, *args, **kwargs)
    return wrapper

def segment(frame, currentComponents, connection_closed):
    if connection_closed:  # Check if connection is closed
        return None, []
    
    # Checking if CUDA-enabled GPU is available
    if torch.cuda.is_available():
        print("GPU detected")
    else:
        print("No GPU, expect slower inference")
    # Initiating the model first
    model = YOLO("/Users/nichdylan/Documents/AR_Assembly/Remote model/yolov8n.pt")
    # Replacing it with the trained model
    model_path = '/Users/nichdylan/Documents/AR_Assembly/arproject/arweb/static/test80.pt'
    model = YOLO(model_path)
    # Overwrite the names from the model, giving it more user-friendly names
    names = ["filter gear", "filter tube", "filter disc", "gear combined with tube", 
             "gear, tubed, and disc combined", "filter body", "filter body screwed", 
             "tube", "spring", "final"]
    # Set a threshold or confidence rate of the classification
    threshold = 0.05

    H, W, _ = frame.shape
    results = model.predict(frame)
    annotator = Annotator(frame, line_width=4)

    detected_object_names = []

    if results[0].masks is not None:
        clss = results[0].boxes.cls.cpu().tolist()
        confidences = results[0].boxes.conf.cpu().tolist()
        masks = results[0].masks.xy
        for mask, cls, confidence in zip(masks, clss, confidences):
            object_name = names[int(cls)]
            if confidence > threshold and object_name in currentComponents: 
                mask_fill_color = colors(int(cls), True)
                filled_mask = frame.copy()
                cv2.fillPoly(filled_mask, [mask.astype(int)], mask_fill_color)
                object_name = names[int(cls)]
                detected_object_names.append(object_name)
                # Transparency level
                alpha = 0.7 
                cv2.addWeighted(filled_mask, alpha, frame, 1 - alpha, 0, frame)
                #Give annotation on top of the image
                annotator.seg_bbox(mask=mask,
                                mask_color=colors(int(cls), True),
                                det_label=f"{names[int(cls)]} {confidence:.2f}")
                                # det_label=f"{names[int(cls)]}")
        ret, buffer = cv2.imencode('.jpg', frame)
        segmented_frame = buffer.tobytes()
        return segmented_frame, detected_object_names
    else:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        return frame, detected_object_names

@login_required_redirect_home
def yolo_view(request, product_id):
    context = {}
    product = Product.objects.get(product_id=product_id)
    steps = product.get_steps()
    steps = sorted(steps, key=lambda x: x.order)
    # components = product.components.all()

    context['product'] = product
    context['steps'] = steps
    # context['components'] = components

    return render(request, 'arweb/detect.html', context)

class ClassConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.stop = False
        self.loop = asyncio.get_running_loop()
        await self.accept()

    async def disconnect(self, close_code):
        self.stop = True
        print("WebSocket Disconnected")
        raise StopConsumer()

    async def receive(self, text_data):
        if not text_data:
            print('Closed connection')
            await self.close()
        else:
            data = json.loads(text_data)
            blob = data.get('image')
            currentComponents = data.get('currentComponents')

            # Decode the frames/images from client
            blob = blob.split(",")[1]

            decoded_image = base64.b64decode(blob)
            image_array = np.frombuffer(decoded_image, dtype=np.uint8)
            self.frame = await self.loop.run_in_executor(None, cv2.imdecode, image_array, cv2.IMREAD_COLOR)
            cv2.imwrite('output_frame.jpg', self.frame)

            # Run inference on it
            self.segmented_frame, detected_object_names = segment(self.frame, currentComponents, self.stop)

            if self.segmented_frame is not None:
                # Turn it into base64 encoding
                self.b64_img = base64.b64encode(self.segmented_frame).decode('utf-8')
                
                # If there's any detection, send the object's name to client
                message = {}
                if detected_object_names:
                    message['detected_object_names'] = detected_object_names
                # Send the base64 encoded segmented image back to the client
                message['image'] = self.b64_img
                await self.send(json.dumps(message))