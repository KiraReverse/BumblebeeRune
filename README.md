# BumblebeeRune
BumblebeeRune

# Description:
- this is a runesolver for maplestory bot - Bumblebee (https://github.com/agumonlyt/Bumblebee)
- this act as a server while Bumblebee, as a client will send screenshot of rune arrows image using requests. 
- after received, a custom trained yolov4 model will detect the arrows and classify their direction. 
- then, 4 inputs (4 arrows) will response back to client (Bumblebee) and will press the corresponding arrow button. 
- please note that this model cannot solve weird arrows. 

# To start, type:
uvicorn pytorch_solver:app --host 192.168.0.131 --port 8001

replace 192.168.0.131 with your local ip address

# install the following:
- fastapi (pip install fastapi)
- pytorch (https://pytorch.org/get-started/locally/)
- if you do not know what CUDA version your GPU is running, type nvidia-smi at cmd. 
- 