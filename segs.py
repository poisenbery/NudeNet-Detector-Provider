from .nudenet import NudeDetector
from collections import namedtuple
import cv2
import numpy as np
import torch

SEG = namedtuple("SEG",
                 ['cropped_image', 'cropped_mask', 'confidence', 'crop_region', 'bbox', 'label', 'control_net_wrapper'],
                 defaults=[None])

class NudenetDetector: #I wrote this so it's probably bad
    def __init__(self):
        nude_detector = NudeDetector()
        
    def segsfilter(segs, labels): #stolen from Lieutenant Doctor Data. remove staticmethod bc I don't know what it does and it broke segs
        labels = set([label.strip() for label in labels])

        if 'all' in labels:
            return (segs, (segs[0], []), )
        else:
            res_segs = []
            remained_segs = []

            for x in segs[1]:
                if x.label in labels:
                    res_segs.append(x)
                elif 'eyes' in labels and x.label in ['left_eye', 'right_eye']:
                    res_segs.append(x)
                elif 'eyebrows' in labels and x.label in ['left_eyebrow', 'right_eyebrow']:
                    res_segs.append(x)
                elif 'pupils' in labels and x.label in ['left_pupil', 'right_pupil']:
                    res_segs.append(x)
                else:
                    remained_segs.append(x)

            return ((segs[0], res_segs), (segs[0], remained_segs), )

        def doit(self, segs, preset, labels): #stolen from Lieutenant Doctor Data
            labels = labels.split(',')
            return SEGSLabelFilter.filter(segs, labels)

    def normalize_region(limit, startp, size): #stolen from Lieutenant Doctor Data
        if startp < 0:
            new_endp = min(limit, size)
            new_startp = 0
        elif startp + size > limit:
            new_startp = max(0, limit - size)
            new_endp = limit
        else:
            new_startp = startp
            new_endp = min(limit, startp+size)

        return int(new_startp), int(new_endp)

    def post_crop_region(self, w, h, item_bbox, crop_region): #stolen from Lieutenant Doctor Data
        return crop_region

    def make_2d_mask(mask): #stolen from Lieutenant Doctor Data
        if len(mask.shape) == 4:
            return mask.squeeze(0).squeeze(0)

        elif len(mask.shape) == 3: #stolen from Lieutenant Doctor Data
            return mask.squeeze(0)
        return mask

    def dilate_mask(mask, dilation_factor, iter=1): #stolen from Lieutenant Doctor Data
        if dilation_factor == 0:
            return mask

        mask = NudenetDetector.make_2d_mask(mask)

        kernel = np.ones((abs(dilation_factor), abs(dilation_factor)), np.uint8)



        if dilation_factor > 0:
            result = cv2.dilate(mask, kernel, iter)
        else:
            result = cv2.erode(mask, kernel, iter)


            return result


    def make_crop_region(w, h, bbox, crop_factor, crop_min_size=None): #stolen from Lieutenant Doctor Data. Changed bbox_w and bbox_h since they were already in detection
        x1 = bbox[0]
        y1 = bbox[1]
        bbox_w = bbox[2]
        bbox_h = bbox[3]

        crop_w = bbox_w * crop_factor
        crop_h = bbox_h * crop_factor

        if crop_min_size is not None:
            crop_w = max(crop_min_size, crop_w)
            crop_h = max(crop_min_size, crop_h)

        kernel_x = x1 + bbox_w / 2
        kernel_y = y1 + bbox_h / 2

        new_x1 = int(kernel_x - crop_w / 2)
        new_y1 = int(kernel_y - crop_h / 2)

        # make sure position in (w,h)
        new_x1, new_x2 = NudenetDetector.normalize_region(w, new_x1, crop_w)
        new_y1, new_y2 = NudenetDetector.normalize_region(h, new_y1, crop_h)

        return [new_x1, new_y1, new_x2, new_y2]
        
    def detect(image, threshold, dilation, crop_factor, drop_size, detailer_hook=None):
        nude_detector = NudeDetector()
        nudes = nude_detector.detect(image)
        result = []
        h = image.shape[1]
        w = image.shape[2]
        for nude in nudes:
            scores = nude['score']
            labels = nude['class']
            boxes = nude['box']
            boxes = np.array(boxes)
            boxes = boxes.astype(np.uint32)
            x1 = boxes[0]
            y1 = boxes[1]
            x2 = boxes[0] + boxes[2]
            y2 = boxes[1] + boxes[3]

            crop_region = NudenetDetector.make_crop_region(w, h, boxes, crop_factor) #stolen from Lieutenant Doctor Data
            crop_x1, crop_y1, crop_x2, crop_y2, = crop_region
            cropped_mask = np.zeros((crop_y2 - crop_y1, crop_x2 - crop_x1))
            cropped_mask[y1 - crop_y1:y2 - crop_y1, x1 - crop_x1:x2 - crop_x1] = 1
            cropped_mask = NudenetDetector.dilate_mask(cropped_mask, dilation)

            item_bbox = (x1, y1, x2, y2)
            item = SEG(None, cropped_mask, scores, crop_region, item_bbox, labels, None)
            result.append(item)

        shape = h, w

        return shape, result

    
