# Description:
- this is a runesolver for MapleStorySEA bot - Bumblebee (https://github.com/agumonlyt/Bumblebee)
- this act as a server while Bumblebee, as a client will send screenshot of rune arrows image using post request. 
- after received, a custom trained yolov4 model will detect the arrows and classify their direction. 
- 4 inputs (4 arrows) will be respond back to the client (Bumblebee) to press down the corresponding arrow buttons. 
