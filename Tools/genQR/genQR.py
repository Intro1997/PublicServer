import qrcode
WIFI_WPA_SEQ_MODE = 'WPA'
WIFI_WEP_SEQ_MODE = 'WEP'
WIFI_WPA2_EAP_SEQ_MODE = 'WPA2-EAP'
 
def genWifiQRCode(wifi_name, seq_mode, eap_encryption_method='', eap_id='', password='', hide_ssid="false", output_path='./wifi_qrcode.png'):
  password_len = len(password)
  if password_len < 8 and seq_mode == 'WPA':
    raise Exception("Sequrity mode is %s, but password length is less than %d." % (seq_mode, password_len))
  elif password_len < 5 and seq_mode == 'WEP':
    raise Exception("Sequrity mode is %s, but password length is less than %d." % (seq_mode, password_len))
  elif password_len < 1 and seq_mode == 'WPA2-EAP':
    raise Exception("Sequrity mode is %s, but password length is less than %d." % (seq_mode, password_len))
  elif len(eap_id) < 1 and seq_mode == 'WPA2-EAP':
    raise Exception("Sequrity mode is %s, but password length is less than %d." % (seq_mode, password_len))
  
  data = "WIFI:"
  if seq_mode == "WPA2-EAP":
    data = data + "T:%s;E:%s;I:%s;S:%s;P:%s;H:%s;" % (seq_mode, eap_encryption_method, eap_id, wifi_name, password, hide_ssid)
  else:
    data = data + "T:%s;S:%s;P:%s;H:%s;" % (seq_mode, wifi_name, password, hide_ssid)

  img = qrcode.make(data)
  with open(output_path, 'wb') as f:
    img.save(f)
  print("WIFI QRCode had been saved in %s" % (output_path))