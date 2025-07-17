from PIL import Image

def decode(img_path):
    img = Image.open(img_path)
    img = img.convert("RGB")
    pixels = img.getdata()
    bits = ""
    for pixel in pixels:
        for channel in pixel:
            bits += str(channel & 1)
    byte_list = []
    for i in range(0, len(bits), 8):
        byte_str = bits[i:i+8]
        byte = int(byte_str, 2)
        byte_list.append(byte)
        if len(byte_list) >= 4 and byte_list[-4:] == [0,0,0,0]:
            byte_list = byte_list[:-4]
            break
    try:
        message = bytes(byte_list).decode("utf-8")
    except Exception as e:
        message = "<解碼失敗，可能是圖片已壓縮或容量不夠>"
    print("藏在圖片裡的訊息：", message)
    return message

decode(r"C:\Users\evan1\Downloads\Doro-1.png")