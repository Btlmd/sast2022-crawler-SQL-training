from selenium.webdriver.remote.webdriver import WebDriver as wd
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC
import selenium
from bs4 import BeautifulSoup as BS
import json

class WebVPN:
    def __init__(self, opt, headless=False):
        self.root_handle = None
        self.driver: wd = None
        self.passwd = opt["password"]
        self.userid = opt["username"]
        self.headless = headless

    def login_webvpn(self):
        d = self.driver
        if d is not None:
            d.close()
        d = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        d.get("https://webvpn.tsinghua.edu.cn/login")
        username = d.find_elements(By.XPATH,
                                   '//div[@class="login-form-item"]//input'
                                   )[0]
        password = d.find_elements(By.XPATH,
                                   '//div[@class="login-form-item password-field" and not(@id="captcha-wrap")]//input'
                                   )[0]
        username.send_keys(str(self.userid))
        password.send_keys(self.passwd)
        d.find_element(By.ID, "login").click()
        self.root_handle = d.current_window_handle
        self.driver = d
        return d

    def access(self, url_input):
        d = self.driver
        url = By.ID, "quick-access-input"
        btn = By.ID, "go"
        wdw(d, 5).until(EC.visibility_of_element_located(url))
        actions = AC(d)
        actions.move_to_element(d.find_element(*url))
        actions.click()
        actions.key_down(Keys.CONTROL).send_keys("A").key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()

        d.find_element(*url)
        d.find_element(*url).send_keys(url_input)
        d.find_element(*btn).click()

    def switch_another(self):
        d = self.driver
        assert len(d.window_handles) == 2
        wdw(d, 5).until(EC.number_of_windows_to_be(2))
        for window_handle in d.window_handles:
            if window_handle != d.current_window_handle:
                d.switch_to.window(window_handle)
                return

    def to_root(self):
        self.driver.switch_to.window(self.root_handle)

    def close_all(self):
        while True:
            try:
                l = len(self.driver.window_handles)
                if l == 0:
                    break
            except selenium.common.exceptions.InvalidSessionIdException:
                return
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.close()

    def login_info(self):
        d = self.driver
        username = By.ID, "userName"
        password = By.NAME, "password"
        wdw(d, 10).until(EC.visibility_of_element_located(username))
        d.find_element(*username).send_keys(str(self.userid))
        d.find_element(*password).send_keys(self.passwd)
        d.find_element(By.XPATH, '//td/input[@type="image"]').click()
        wdw(d, 15).until(EC.visibility_of_element_located((By.XPATH, '//span[text()="信息门户"]')))

    def get_grades(self):
        wdw(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'table1')))
        html = self.driver.find_elements(By.TAG_NAME, "HTML")[0].get_attribute("innerHTML")
        soup = BS(html, 'lxml')
        grades = []
        table = soup.select("#table1 tbody")[0].find_all('tr')
        # print(table)
        for tr in table:
            tds = list(tr.find_all('td'))
            if len(tds) == 0:
                continue
            grades += [{
                "id": tds[0].text.strip(),
                "name": tds[1].text.strip(),
                "credit": tds[2].text.strip(),
                "grade": tds[3].text.strip(),
                "points": tds[4].text.strip(),
                "term": tds[5].text.strip(),
            }]
        terms = {}
        pv = None
        for course in grades:
            if course["term"] != pv:
                terms[course["term"]] = []
                pv = course["term"]
            terms[course["term"]] += [course]

        term_gpa = {}
        for k, courses in terms.items():
            deno = 0
            summation = 0
            for c in courses:
                if c["points"] == "N/A":
                    continue
                summation += float(c["points"]) * int(c["credit"])
                deno += int(c["credit"])
            gpa = summation / deno
            term_gpa[k] = gpa

        for k, v in term_gpa.items():
            print(f"{k}: {round(v, 2)}")

if __name__ == "__main__":
    with open("settings.json", "r") as f:
        opt = json.load(f)

    v = WebVPN(opt)
    v.login_webvpn()
    v.access("info.tsinghua.edu.cn")
    v.switch_another()
    v.login_info()
    v.driver.close()
    v.to_root()
    v.access("zhjw.cic.tsinghua.edu.cn/cj.cjCjbAll.do?m=bks_cjdcx&cjdlx=zw")
    v.switch_another()
    v.get_grades()
    v.close_all()
