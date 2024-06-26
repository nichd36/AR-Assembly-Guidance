# # call/consumers.py
# import base64
# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# from ultralytics.utils.plotting import Annotator, colors
# import cv2
# import numpy as np
# # from arproject.arweb.yolo_segmentation import YOLOSegmentation

# class CallConsumer(WebsocketConsumer):

# #     def process_frame(self, frame):
# #         results = self.model.predict(frame)
# #         annotator = Annotator(frame, line_width=2)

# #         if results[0].masks is not None:
# #             clss = results[0].boxes.cls.cpu().tolist()
# #             confidences = results[0].boxes.conf.cpu().tolist()
# #             masks = results[0].masks.xy

# #             for mask, cls, confidence in zip(masks, clss, confidences):
# #                 if confidence > self.threshold:
# #                     mask_fill_color = colors(int(cls), True)
# #                     filled_mask = frame.copy()
# #                     cv2.fillPoly(filled_mask, [mask.astype(int)], mask_fill_color)

# #                     alpha = 0.4
# #                     cv2.addWeighted(filled_mask, alpha, frame, 1 - alpha, 0, frame)

# #                     annotator.seg_bbox(mask=mask,
# #                                        mask_color=colors(int(cls), True),
# #                                        det_label=f"{self.names[int(cls)]} {confidence:.2f}")

# #         ret, buffer = cv2.imencode('.jpg', frame)
# #         frame_bytes = buffer.tobytes()
# #         return frame_bytes

# #     model_path = "/Users/nichdylan/Documents/AR_Assembly/arproject/arweb/static/speaker_segment.pt"
# #     # yolo = YOLOSegmentation(model_path)

# #     def connect(self):
# #         self.accept()

# #         # response to client, that we are connected.
# #         self.send(text_data=json.dumps({
# #             'type': 'connection',
# #             'data': {
# #                 'message': "Connected"
# #             }
# #         }))

# #     def disconnect(self, close_code):
# #         # Leave room group
# #         async_to_sync(self.channel_layer.group_discard)(
# #             self.my_name,
# #             self.channel_name
# #         )

# #     # Receive message from client WebSocket
# #     def receive(self, text_data):
# #         text_data_json = json.loads(text_data)
# #         eventType = text_data_json['type']

# #         if eventType == 'login':
# #             name = text_data_json['data']['name']
# #             self.my_name = name
# #             async_to_sync(self.channel_layer.group_add)(
# #                 self.my_name,
# #                 self.channel_name
# #             )

# #         elif eventType == 'call':
# #             name = text_data_json['data']['name']
# #             async_to_sync(self.channel_layer.group_send)(
# #                 name,
# #                 {
# #                     'type': 'call_received',
# #                     'data': {
# #                         'caller': self.my_name,
# #                         'rtcMessage': text_data_json['data']['rtcMessage']
# #                     }
# #                 }
# #             )

# #         elif eventType == 'answer_call':
# #             caller = text_data_json['data']['caller']
# #             async_to_sync(self.channel_layer.group_send)(
# #                 caller,
# #                 {
# #                     'type': 'call_answered',
# #                     'data': {
# #                         'rtcMessage': text_data_json['data']['rtcMessage']
# #                     }
# #                 }
# #             )

# #         elif eventType == 'ICEcandidate':
# #             user = text_data_json['data']['user']
# #             async_to_sync(self.channel_layer.group_send)(
# #                 user,
# #                 {
# #                     'type': 'ICEcandidate',
# #                     'data': {
# #                         'rtcMessage': text_data_json['data']['rtcMessage']
# #                     }
# #                 }
# #             )

# #         elif eventType == 'video_frame':
# #             image_data = text_data_json['data']['image_data']
# #             frame_bytes = base64.b64decode(image_data.split(",")[1])
# #             nparr = np.frombuffer(frame_bytes, np.uint8)
# #             frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
# #             processed_frame = self.yolo.process_frame(frame)
# #             processed_frame_bytes = base64.b64encode(processed_frame).decode('utf-8')

# #             self.send(text_data=json.dumps({
# #                 'type': 'processed_frame',
# #                 'data': {
# #                     'image_data': processed_frame_bytes
# #                 }
# #             }))

# #     def call_received(self, event):

# #         # print(event)
# #         print('Call received by ', self.my_name )
# #         self.send(text_data=json.dumps({
# #             'type': 'call_received',
# #             'data': event['data']
# #         }))


# #     def call_answered(self, event):

# #         # print(event)
# #         print(self.my_name, "'s call answered")
# #         self.send(text_data=json.dumps({
# #             'type': 'call_answered',
# #             'data': event['data']
# #         }))


#     def ICEcandidate(self, event):
#         self.send(text_data=json.dumps({
#             'type': 'ICEcandidate',
#             'data': event['data']
#         }))