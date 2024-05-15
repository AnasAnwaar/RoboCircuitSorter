import cv2
import torch
from numpy import random
import torch.backends.cudnn as cudnn
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import *
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

# Initialize decoded data variables
bat, cap, ind, res, tra, led = 0, 0, 0, 0, 0, 0

flag = True
robocammand = 0
def process_txt_file(file_path):
    # Initialize a dictionary to store decoded data
    decoded_data = {}

    # Open the text file in read mode
    with open(file_path, 'r') as file:
        # Read each line in the file
        for line in file:
            # Split each line into key and value
            key, value = line.strip().split(' = ')
            # Decode the value and store it in the dictionary
            decoded_data[key.strip()] = int(value.strip())

    return decoded_data

def detect_roi(im0, roi_boxes, det, names, colors):
    global bat, cap, ind, res, tra, led , flag , robocammand

    for box_coords in roi_boxes:
        cv2.rectangle(im0, (box_coords[0], box_coords[1]), (box_coords[2], box_coords[3]), (0, 255, 0), 2)

    roi_objects = {i: [] for i in range(len(roi_boxes))}

    for box_idx, box_coords in enumerate(roi_boxes):
        for *xyxy, conf, cls in reversed(det):
            if all(box_coords[0] < p < box_coords[2] and box_coords[1] < q < box_coords[3] for p, q in [xyxy[:2], xyxy[2:]]):
                label = f'{names[int(cls)]} {conf:.2f}'
                plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)
                roi_objects[box_idx].append(names[int(cls)])

    for i, objects in roi_objects.items():
        print(f'Objects in ROI {i + 1}: {", ".join(objects)}')

    for roi_idx, objects in roi_objects.items():
        if roi_idx == 0 and flag:
            for obj, qty_var in [("battery", "bat"), ("capacitor", "cap"), ("inductor", "ind"), ("resistor", "res"),
                                 ("transistor", "tra"), ("led", "led")]:
                if obj.lower() in objects and globals()[qty_var] > 0:
                    globals()[qty_var] -= 1
                    print(f"{obj.capitalize()} found in ROI {roi_idx + 1}")
                    robocammand = roi_idx + 1
                    print(f"Robotic arm cammand:  {robocammand} ")
                    flag = False

        if roi_idx == 1 and flag:
            for obj, qty_var in [("battery", "bat"), ("capacitor", "cap"), ("inductor", "ind"), ("resistor", "res"),
                                 ("transistor", "tra"), ("led", "led")]:
                if obj.lower() in objects and globals()[qty_var] > 0:
                    globals()[qty_var] -= 1
                    print(f"{obj.capitalize()} found in ROI {roi_idx + 1}")
                    robocammand = roi_idx + 1
                    print(f"Robotic arm cammand:  {robocammand} ")
                    flag = False

        if roi_idx == 2 and flag:
            for obj, qty_var in [("battery", "bat"), ("capacitor", "cap"), ("inductor", "ind"), ("resistor", "res"),
                                 ("transistor", "tra"), ("led", "led")]:
                if obj.lower() in objects and globals()[qty_var] > 0:
                    globals()[qty_var] -= 1
                    print(f"{obj.capitalize()} found in ROI {roi_idx + 1}")
                    robocammand = roi_idx + 1
                    print(f"Robotic arm cammand:  {robocammand} ")
                    flag = False

        if roi_idx == 3 and flag:
            for obj, qty_var in [("battery", "bat"), ("capacitor", "cap"), ("inductor", "ind"), ("resistor", "res"),
                                 ("transistor", "tra"), ("led", "led")]:
                if obj.lower() in objects and globals()[qty_var] > 0:
                    globals()[qty_var] -= 1
                    print(f"{obj.capitalize()} found in ROI {roi_idx + 1}")
                    robocammand = roi_idx + 1
                    print(f"Robotic arm cammand:  {robocammand} ")
                    flag = False


        if roi_idx == 4 and flag:
            for obj, qty_var in [("battery", "bat"), ("capacitor", "cap"), ("inductor", "ind"), ("resistor", "res"),
                                 ("transistor", "tra"), ("led", "led")]:
                if obj.lower() in objects and globals()[qty_var] > 0:
                    globals()[qty_var] -= 1
                    print(f"{obj.capitalize()} found in ROI {roi_idx + 1}")
                    robocammand = roi_idx + 1
                    print(f"Robotic arm cammand:  {robocammand} ")
                    flag = False

        if roi_idx == 5 and flag:
            for obj, qty_var in [("battery", "bat"), ("capacitor", "cap"), ("inductor", "ind"), ("resistor", "res"),
                                 ("transistor", "tra"), ("led", "led")]:
                if obj.lower() in objects and globals()[qty_var] > 0:
                    globals()[qty_var] -= 1
                    print(f"{obj.capitalize()} found in ROI {roi_idx + 1}")
                    robocammand = roi_idx + 1
                    print(f"Robotic arm cammand:  {robocammand} ")
                    flag = False



    flag = True

    print("Decoded Data:")
    print("Battery:", bat)
    print("Capacitor:", cap)
    print("Inductor:", ind)
    print("Resistor:", res)
    print("Transistor:", tra)
    print("LED:", led)

    return roi_objects






def detect():
    class Args:
        def _init_(self):
            self.weights = 'realtimecomponentdetection.pt'
            self.source = '0'
            self.img_size = 640
            self.conf_thres = 0.65
            self.iou_thres = 0.45
            self.device = ''
            self.view_img = True
            self.save_txt = False
            self.save_conf = False
            self.nosave = False
            self.classes = None
            self.agnostic_nms = False
            self.augment = False
            self.update = False
            self.project = 'runs/detect'
            self.name = 'exp'
            self.exist_ok = False
            self.no_trace = False

    opt = Args()

    source, weights, imgsz, trace = opt.source, opt.weights, opt.img_size, not opt.no_trace
    save_img = not (opt.nosave or source.endswith('.txt'))
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))

    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))
    (save_dir / 'labels' if opt.save_txt else save_dir).mkdir(parents=True, exist_ok=True)

    set_logging()
    device = select_device(opt.device)
    half = device.type != 'cpu'

    model = attempt_load(weights, map_location=device)
    stride = int(model.stride.max())
    imgsz = check_img_size(imgsz, s=stride)

    if trace:
        model = TracedModel(model, device, opt.img_size)

    if half:
        model.half()

    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    vid_path, vid_writer = None, None
    if webcam:
        cudnn.benchmark = True
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))

    t0 = time.time()

    roi_boxes = [
        [50, 50, 150, 150],
        [200, 50, 300, 150],
        [350, 50, 450, 150],
        [500, 50, 600, 150],
        [50, 200, 150, 300],
        [500, 200, 600, 300]
    ]



    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        t1 = time_synchronized()
        with torch.no_grad():
            pred = model(img, augment=opt.augment)[0]
        t2 = time_synchronized()

        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
        t3 = time_synchronized()

        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        for i, det in enumerate(pred):
            if webcam:
                p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

            p = Path(p)
            save_path = str(save_dir / p.name)
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                roi_objects = detect_roi(im0, roi_boxes, det, names, colors)  # Call the ROI detection function
            else:
                # Draw ROI rectangles when no objects are detected
                for box_coords in roi_boxes:
                    cv2.rectangle(im0, (box_coords[0], box_coords[1]), (box_coords[2], box_coords[3]), (0, 255, 0), 2)

            print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')

            if opt.view_img:
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)

    if opt.save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if opt.save_txt else ''
        print(f"Results saved to {save_dir}{s}")

    print(f'Done. ({time.time() - t0:.3f}s)')



if _name_ == '_main_':
    file_path = 'C:/Users/HP/PycharmProjects/robocircuit/txtresult/1_text_20240424_1627.txt'
    decoded_data = process_txt_file(file_path)

    # Extract individual variables from the decoded data
    bat = decoded_data['Battery']
    cap = decoded_data['Capacitor']
    ind = decoded_data['Inductor']
    res = decoded_data['Resistor']
    tra = decoded_data['Transistor']
    led = decoded_data['Led']
    detect()