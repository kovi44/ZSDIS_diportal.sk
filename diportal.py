from io import BytesIO
import pycurl
import json
from pprint import pprint
from datetime import date
import calendar
import re
import sys
import os
import ast
from twocaptcha import TwoCaptcha

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

########### NEED TO CUSTOMIZED ################################################################################################################
username = "PLEASE FILL IT WITH VALID USERNAME"                             ## username for diportal.sk
password = "PLEASE FILL IT WITH VALID PASSWORD"                             ## password for diportal.sk
twocaptcha_api_key = "YOUR API KEY for 2captcha.com"                        ## api key for 2captcha.com service, need a subscription, place None if you would like to use just cookie mode
recaptcha_site_key = '6LfdaLUZAAAAAHCVziF1iDFvmCxAjlIP1xF6pjHg'             ## it's a unique recatcha key for diportal site assigned by google
debug = None                                                                ## If debug None then just clear Json output
###############################################################################################################################################
source = "KOC"
profileRole = "null"
loadProfileRoles = "true"
cookie_file = "cookie.txt"
############## URLS ###########################################################################################################################
login_site = 'https://www.diportal.sk/portal/#/verejne/prihlasenie'
login_process_api_url = "https://www.diportal.sk/portal/api/public/texts/getNewsAndAnnouncements"
login_process_api_url_2 = "https://www.diportal.sk/portal/api/security/login"
checkUser_url = "https://www.diportal.sk/portal/api/security/checkUser"
getUserData_url = 'https://www.diportal.sk/portal/api/commons/getUser'
getProfileData_url = 'https://www.diportal.sk/portal/api/interval-data/getProfileData'
getDeliveryPoints_url = 'https://www.diportal.sk/portal/api/delivery-points-list/loadDeliveryPoints'
getDevicesForDeliveryPoint_url = 'https://www.diportal.sk/portal/api/register-data/getDevicesForDeliveryPoint'
getRegisterData_url = 'https://www.diportal.sk/portal/api/register-data/getData'
##############################################################################################################################################
useragent =  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
secchua = "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\""
secchuaplatform = "\"macOS\""
##############################################################################################################################################
dict_main = {}
dict_main['userData'] = {}
dict_main['deliveryPoints'] = {}



api_key = os.getenv('APIKEY_2CAPTCHA', twocaptcha_api_key)
solver = TwoCaptcha(api_key)

def reCaptcha():
    try:
        result = solver.recaptcha(
            sitekey=recaptcha_site_key,
            url=login_site)

    except Exception as e:
        sys.exit(e)

    else:
        # dumps the json object into an element
        json_str = json.dumps(result)
        # load the json to a string
        resp = json.loads(json_str)
        return resp['code']

class Storage:
    def __init__(self):
        self.contents = ''
        self.line = 0

    def store(self, buf):
        self.line = self.line + 1
        self.contents = "%s%i: %s" % (self.contents, self.line, buf)

    def __str__(self):
        return self.contents

retrieved_body = Storage()
retrieved_headers = Storage()

headers = {}

def display_header(header_line):
    header_line = header_line.decode('iso-8859-1')

    # Ignore all lines without a colon
    if ':' not in header_line:
        return

    # Break the header line into header name and value
    h_name, h_value = header_line.split(':', 1)

    # Remove whitespace that may be present
    h_name = h_name.strip()
    h_value = h_value.strip()
    h_name = h_name.lower() # Convert header names to lowercase
    headers[h_name] = h_value # Header name and value.

today = date.today()
from_date = "{0}-{1}-01".format(today.year,today.month)
maxdays = calendar.monthrange(today.year, today.month)[1]
to_date   = "{0}-{1}-{2}".format(today.year,today.month,maxdays)

def loginProcess(captcha):
    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, login_process_api_url)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.setopt(crl.SSL_VERIFYPEER, 1)
    crl.setopt(crl.SSL_VERIFYHOST, False)
    crl.setopt(crl.COOKIEJAR, cookie_file)
    crl.setopt(crl.WRITEFUNCTION, retrieved_body.store)
    crl.setopt(crl.HEADERFUNCTION, retrieved_headers.store)
    crl.setopt(crl.HTTPHEADER, [
        "Accept: application/json, text/plain, */*",
        "Accept-Language: en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control: no-cache",
        "Connection: keep-alive",
        "Host: www.diportal.sk",
        "Origin: https://www.diportal.sk",
        "Pragma: no-cache",
        "Referer: https://www.diportal.sk/portal/",
        "Sec-Fetch-Dest: empty",
        "Sec-Fetch-Mode: cors",
        "Sec-Fetch-Site: same-origin",
        "User-Agent: "+useragent+"",
        "content-type: application/json",
        "sec-ch-ua: "+secchua+"",
        "sec-ch-ua-mobile: ?0",
        "sec-ch-ua-platform: "+secchuaplatform+""
    ])
    crl.perform()
    get_body = b_obj.getvalue()
    crl.close()

    loginFormJson = "{\n  \"userId\": \""+username+"\",\n    \"password\": \""+password+"\",\n    \"invisibleRecaptchaResponse\": \""+captcha+"\"\n}"

    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, login_process_api_url_2)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.setopt(crl.SSL_VERIFYPEER, 1)
    crl.setopt(crl.SSL_VERIFYHOST, False)
    crl.setopt(crl.COOKIEFILE, cookie_file)
    crl.setopt(crl.COOKIEJAR, cookie_file)
    crl.setopt(crl.POST, 1)
    crl.setopt(crl.POSTFIELDS, loginFormJson)
    crl.setopt(crl.HEADERFUNCTION, display_header)
    crl.setopt(crl.HTTPHEADER, [
        "Accept: application/json, text/plain, */*",
        "Accept-Language: en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control: no-cache",
        "Connection: keep-alive",
        "Host: www.diportal.sk",
        "Origin: https://www.diportal.sk",
        "Pragma: no-cache",
        "Referer: https://www.diportal.sk/portal/",
        "Sec-Fetch-Dest: empty",
        "Sec-Fetch-Mode: cors",
        "Sec-Fetch-Site: same-origin",
        "User-Agent: "+useragent+"",
        "content-type: application/json",
        "sec-ch-ua: "+secchua+"",
        "sec-ch-ua-mobile: ?0",
        "sec-ch-ua-platform: "+secchuaplatform+""
    ])
    crl.perform()
    get_body = b_obj.getvalue()
    crl.close()

    data_dict = ast.literal_eval(str(headers))

    # Retrieve the CSRF value
    csrf_value = data_dict.get('x-csrf')

    if debug != None: print(f"CSRF Value: {csrf_value}")

    return csrf_value


def checkUser():
    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, checkUser_url)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.setopt(crl.SSL_VERIFYPEER, 1)
    crl.setopt(crl.SSL_VERIFYHOST, False)
    crl.setopt(crl.COOKIEFILE, cookie_file)
    crl.setopt(crl.WRITEFUNCTION, retrieved_body.store)
    crl.setopt(crl.HEADERFUNCTION, display_header)
    crl.setopt(crl.HTTPHEADER, [
        "Accept: application/json, text/plain, */*",
        "Accept-Language: en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control: no-cache",
        "Connection: keep-alive",
        "Host: www.diportal.sk",
        "Origin: https://www.diportal.sk",
        "Pragma: no-cache",
        "Referer: https://www.diportal.sk/portal/",
        "Sec-Fetch-Dest: empty",
        "Sec-Fetch-Mode: cors",
        "Sec-Fetch-Site: same-origin",
        "User-Agent: "+useragent+"",
        "content-type: application/json",
        "sec-ch-ua: "+secchua+"",
        "sec-ch-ua-mobile: ?0",
        "sec-ch-ua-platform: "+secchuaplatform+""
    ])
    crl.perform()
    get_body = b_obj.getvalue()
    crl.close()

    data_dict = ast.literal_eval(str(headers))
    csrf_value = None
    # Retrieve the CSRF value
    csrf_value = data_dict.get('x-csrf')

    if debug != None: print(f"CSRF Value: {csrf_value}")

    return csrf_value


def requestDataPost(url0, data0):
    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, url0)
    crl.setopt(crl.COOKIEFILE, cookie_file)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.setopt(crl.SSL_VERIFYPEER, 1)
    crl.setopt(crl.SSL_VERIFYHOST, False)
    crl.setopt(crl.POST, 1)
    crl.setopt(crl.POSTFIELDS, data0)
    crl.setopt(crl.HTTPHEADER, [
        "Accept: application/json, text/plain, */*",
        "Accept-Language: en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control: no-cache",
        "Connection: keep-alive",
        "Host: www.diportal.sk",
        "Origin: https://www.diportal.sk",
        "Pragma: no-cache",
        "Referer: https://www.diportal.sk/portal/",
        "Sec-Fetch-Dest: empty",
        "Sec-Fetch-Mode: cors",
        "Sec-Fetch-Site: same-origin",
        "User-Agent: "+useragent+"",
        "X-CSRF: {0}".format(xcsrf),
        "content-type: application/json",
        "sec-ch-ua: "+secchua+"",
        "sec-ch-ua-mobile: ?0",
        "sec-ch-ua-platform: "+secchuaplatform+""
    ])
    crl.perform()
    get_body = b_obj.getvalue()
    crl.close()
    if re.search(b"Chybov", get_body.decode('latin-1').encode("utf-8")):
        print("Error, seem to be cookie issue!")
        exit(0)
    elif re.search(b"Request Rejected", get_body.decode('latin-1').encode("utf-8")):
        print("Error, seem to be cookie issue!")
        exit(0)
    return get_body

def requestDataGet(url0):
    b_obj = BytesIO()
    crl = pycurl.Curl()
    crl.setopt(crl.URL, url0)
    crl.setopt(crl.COOKIEFILE, cookie_file)
    crl.setopt(crl.WRITEDATA, b_obj)
    crl.setopt(crl.SSL_VERIFYPEER, 1)
    crl.setopt(crl.SSL_VERIFYHOST, False)
    crl.setopt(crl.HTTPHEADER, [
        "Accept: application/json, text/plain, */*",
        "Accept-Language: en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control: no-cache",
        "Connection: keep-alive",
        "Host: www.diportal.sk",
        "Origin: https://www.diportal.sk",
        "Pragma: no-cache",
        "Referer: https://www.diportal.sk/portal/",
        "Sec-Fetch-Dest: empty",
        "Sec-Fetch-Mode: cors",
        "Sec-Fetch-Site: same-origin",
        "User-Agent: "+useragent+"",
        "X-CSRF: {0}".format(xcsrf),
        "content-type: application/json",
        "sec-ch-ua: "+secchua+"",
        "sec-ch-ua-mobile: ?0",
        "sec-ch-ua-platform: "+secchuaplatform+""
    ])
    crl.perform()
    get_body = b_obj.getvalue()
    crl.close()
    if re.search(b"Chybov", get_body.decode('latin-1').encode("utf-8")):
        print("Error, seem to be cookie issue!")
        exit(0)
    elif re.search(b"Request Rejected", get_body.decode('latin-1').encode("utf-8")):
        print("Error, seem to be cookie issue!")
        exit(0)
    return get_body

def getIntervalData(deliveryPointId0,from_date0,to_date0,profileRole0,loadProfileRoles0,businessPartnerId0,businessRoleId0,source0):

    post_data = "{\n  \"filter\": {\n    \"deliveryPointId\": \""+deliveryPointId0+"\",\n    \"from\": \""+from_date0+"\",\n    \"to\": \""+to_date0+"\",\n    \"profileRole\": "+profileRole0+",\n    \"loadProfileRoles\": "+loadProfileRoles0+"\n  },\n  \"businessPartnerId\": \""+businessPartnerId0+"\",\n  \"businessRoleId\": \""+businessRoleId0+"\",\n  \"source\": \""+source0+"\"\n}"

    data = json.loads(requestDataPost(getProfileData_url, post_data))
    if "dailyIntervalData" in data["data"]["profileData"]:
            if debug != None: print("\n{0}:".format(deliveryPointId0))
            dict_main['deliveryPoints'][deliveryPointId0]["intervalData"] = data['data']['profileData']['dailyIntervalData']
            no = len(data["data"]["profileData"]["dailyIntervalData"])
            for xn in range(no):
                if data["data"]["profileData"]["dailyIntervalData"][xn]["dailyState"] == "ALL_VALID":
                    date = data["data"]["profileData"]["dailyIntervalData"][xn]["date"]
                    consumption = data["data"]["profileData"]["dailyIntervalData"][xn]["consumption"]
                    measuredValueUnit = data["data"]["profileData"]["measuredValueUnit"]
                    if debug != None: print("{0} - {1} {2}".format(date,consumption,measuredValueUnit))

def getUserData():

    data = json.loads(requestDataGet(getUserData_url))
    if "lastName" in data["data"]:
            if debug != None: print("User data:")
            resp = {}
            resp['lastName'] = data["data"]["lastName"]
            resp['firstName'] = data["data"]["firstName"]
            resp['email'] = data["data"]["email"]
            resp['city'] = data["data"]["city"]
            resp['businessPartnerId'] = data["data"]["businessPartnerAssignments"][0]["businessPartnerId"]
            resp['businessRoleId'] = data["data"]["businessPartnerAssignments"][0]["businessRoleIds"][0]
            if debug != None: print("Last Name: " + resp['lastName'])
            if debug != None: print("First Name: " + resp['firstName'])
            if debug != None: print("Email: " + resp['email'])
            if debug != None: print("City: " + resp['city'])
            if debug != None: print("businessPartnerId: " + resp['businessPartnerId'])
            if debug != None: print("businessRoleId: " + resp['businessRoleId'] )
            dict_main['userData'] = data['data']
            del dict_main['userData']['businessPartnerAssignments']
            del dict_main['userData']['roles']
            del dict_main['userData']['customizationParameters']
            del dict_main['userData']['accountInformation']
            del dict_main['userData']['permissions']
            del dict_main['userData']['menuItems']
            del dict_main['userData']['allowExvyRequest']
            del dict_main['userData']['verificationMethod']
            del dict_main['userData']['locked']
            del dict_main['userData']['passwordChangeRequired']

            return resp


def getDeliveryPoints(businessPartnerId0, businessRoleId0):

    post_data = "{ \"filter\": {\"onlyActive\": true,\"smartMeterEnabled\": null,\"dateFrom\": \"\",\"dateTo\": \"\"},\"businessPartnerId\": \""+businessPartnerId0+"\",\"businessRoleId\": \""+businessRoleId0+"\"}"

    data = json.loads(requestDataPost(getDeliveryPoints_url, post_data))
    if "city" in data["data"][0]:
        #y = json.dumps(data)
        if debug != None: print("DeliveryPoints:")
        dict_deliveryPointId = {}
        no = len(data["data"])
        for xn in range(no):
            dict_deliveryPointId[xn] = data["data"][xn]["deliveryPointId"]
            if debug != None: print("DeliveryPointId is "+data["data"][xn]["deliveryPointId"])
            dict_main['deliveryPoints'][data["data"][xn]["deliveryPointId"]] = {}
        return dict_deliveryPointId

def getDevicesForDeliveryPoints(businessPartnerId0, businessRoleId0,to_date0,deliveryPointId0):

    post_data = "{ \"filter\": {\"dateTo\": \""+to_date0+"\",\"dateFrom\": \"2021-01-01\",\"deliveryPointId\": \""+deliveryPointId0+"\"},\"businessPartnerId\": \""+businessPartnerId0+"\",\"businessRoleId\": \""+businessRoleId0+"\"}"
    
    data = json.loads(requestDataPost(getDevicesForDeliveryPoint_url, post_data))
    if "serialNumber" in data["data"][0]:
        #y = json.dumps(data)
        if debug != None: print("DeliveryPoints Devices:")
        dict_devices = {}
        dict_devices['serialNumber'] = data["data"][0]["serialNumber"]
        if debug != None: print("serialNumber is "+data["data"][0]["serialNumber"])
        dict_devices['equipmentNumber'] = data["data"][0]["equipmentNumber"]
        if debug != None: print("equipmentNumber is "+data["data"][0]["equipmentNumber"])
        return dict_devices

def getRegisterData(deliveryPointId1,to_date0,deviceSerialNumber0,deviceEquipmentNumber0,businessPartnerId0,businessRoleId0):

    post_data = "{\n  \"filter\": {\n    \"deliveryPointId\": \""+deliveryPointId1+"\",\n    \"dateFrom\": \"2022-12-31\",\n    \"dateTo\": \""+to_date0+"\",\n    \"deviceSerialNumber\": \""+deviceSerialNumber0+"\",\n    \"deviceEquipmentNumber\": \""+deviceEquipmentNumber0+"\"\n  },\n  \"businessPartnerId\": \""+businessPartnerId0+"\",\n  \"businessRoleId\": \""+businessRoleId0+"\"\n}";

    data = json.loads(requestDataPost(getRegisterData_url, post_data))
    if "deviceSerialNumber" in data["data"][0]:
            if debug != None: print("\nRegistered data:")
            dict_main['deliveryPoints'][deliveryPointId1]["registerData"] = data['data']
            no = len(data["data"])
            for xn in range(no):
                if data["data"][xn]["deviceSerialNumber"] == deviceSerialNumber0:
                    settlementDate = data["data"][xn]["settlementDate"]
                    counterId = data["data"][xn]["counterId"]
                    settlementState = data["data"][xn]["settlementState"];
                    if debug != None: print("{0} - {1} {2} kWh".format(settlementDate,counterId,settlementState))


#### MAIN PART ####


if (os.path.isfile(cookie_file)):
    xcsrf = checkUser()
    if xcsrf != None:
        if debug != None: print("We got valid cookies")
        user_data = getUserData()
        deliveryPoints = getDeliveryPoints(user_data['businessPartnerId'], user_data['businessRoleId'])
        for key in deliveryPoints:
            getIntervalData(deliveryPoints[key],from_date,to_date,profileRole,loadProfileRoles,user_data['businessPartnerId'],user_data['businessRoleId'],source)
            devices = getDevicesForDeliveryPoints(user_data['businessPartnerId'], user_data['businessRoleId'],to_date,deliveryPoints[key])
            getRegisterData(deliveryPoints[key],to_date,devices['serialNumber'],devices['equipmentNumber'],user_data['businessPartnerId'],user_data['businessRoleId'])
        
    else:
        if debug != None: print("Cookies already expired")
        if twocaptcha_api_key != None:
            xcsrf = loginProcess(reCaptcha())
            user_data = getUserData()
            deliveryPoints = getDeliveryPoints(user_data['businessPartnerId'], user_data['businessRoleId'])
            for key in deliveryPoints:
                getIntervalData(deliveryPoints[key],from_date,to_date,profileRole,loadProfileRoles,user_data['businessPartnerId'],user_data['businessRoleId'],source)
                devices = getDevicesForDeliveryPoints(user_data['businessPartnerId'], user_data['businessRoleId'],to_date,deliveryPoints[key])
                getRegisterData(deliveryPoints[key],to_date,devices['serialNumber'],devices['equipmentNumber'],user_data['businessPartnerId'],user_data['businessRoleId'])
        else:
            if debug != None: print("Missing 2captcha api key!")
else:
    if twocaptcha_api_key != None:
        if debug != None: print("Fresh login process initiated")
        xcsrf = loginProcess(reCaptcha())
        user_data = getUserData()
        deliveryPoints = getDeliveryPoints(user_data['businessPartnerId'], user_data['businessRoleId'])
        for key in deliveryPoints:
            getIntervalData(deliveryPoints[key],from_date,to_date,profileRole,loadProfileRoles,user_data['businessPartnerId'],user_data['businessRoleId'],source)
            devices = getDevicesForDeliveryPoints(user_data['businessPartnerId'], user_data['businessRoleId'],to_date,deliveryPoints[key])
            getRegisterData(deliveryPoints[key],to_date,devices['serialNumber'],devices['equipmentNumber'],user_data['businessPartnerId'],user_data['businessRoleId'])
    else:
        if debug != None: print("Missing 2captcha api key!")


print(json.dumps(dict_main, indent=2))
