#!/bin/bash

{ 
cat <<EOF
http://scm-l3.technorati.com/11/12/03/57331/qr-code-london.jpeg?t=20111203175457
http://www.3dcalifornia.com/wp-content/uploads/2011/01/qr-code.jpg
http://qrcodepress.com/wp-content/uploads/2011/02/QR-Codes-On-Wine.jpg
http://www.blueglass.com/wordpress/wp-content/uploads/2011/04/cnn_qr_code.jpg
http://cdn3.reelstatic.com/wp-content/uploads/2011/01/calvin-klein-jeans-f10-QR-code-billboard-070910-1024x731-600x428.jpg
http://www.qrstuff.com/images/sample.png
http://cdn.androidtapp.com/wp-content/uploads/2009/06/Barcode-Scanner-Focusing-on-QR-Code-on-Monitor.jpg
http://cortesdecima.com/wp-content/uploads/2008/10/qr-code-avin.jpg
EOF
} | xargs python web_zbar.py
