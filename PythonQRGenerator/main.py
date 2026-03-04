import pyqrcode

url=input("ENTER URL PLEASE:")

qr_code=pyqrcode.create(url)
qr_code.svg("qrcode.svg",scale=5)



