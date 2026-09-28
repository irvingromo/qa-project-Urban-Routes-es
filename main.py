import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""
    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    # 1. LOCALIZADORES (Utilizando al menos 4 tipos distintos)[cite: 4]
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.XPATH, "//button[contains(text(), 'Pedir un taxi')]")
    comfort_tariff = (By.XPATH, "//div[contains(text(), 'Comfort')]")
    phone_field_button = (By.CLASS_NAME, 'np-text')
    phone_input = (By.ID, 'phone')
    next_button = (By.XPATH, "//button[text()='Siguiente']")
    sms_code_input = (By.ID, 'code')
    confirm_button = (By.XPATH, "//button[text()='Confirmar']")
    payment_method_button = (By.CLASS_NAME, 'pp-text')
    add_card_button = (By.CLASS_NAME, 'pp-plus-container')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.CSS_SELECTOR,
                       '.card-input#code')  # El botón enlace se activa al perder el enfoque de este campo[cite: 2]
    link_card_button = (By.XPATH, "//button[text()='Enlace']")
    close_payment_modal_button = (By.CSS_SELECTOR, '.payment-picker .close-button')
    message_input = (By.ID, 'comment')
    blanket_tissues_switch = (By.CSS_SELECTOR, '.reqs-body .switch')
    ice_cream_plus_button = (By.CLASS_NAME, 'counter-plus')
    ice_cream_counter = (By.CLASS_NAME, 'counter-value')
    order_taxi_button = (By.CLASS_NAME, 'smart-button')
    modal_driver_info = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver

    # 2. MÉTODOS DE INTERACCIÓN (Comienzan con verbos descriptivos)[cite: 4]
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_request_taxi(self):
        # Uso de esperas explícitas[cite: 4]
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.request_taxi_button)
        )
        self.driver.find_element(*self.request_taxi_button).click()

    def select_comfort_tariff(self):
        WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.comfort_tariff)
        )
        self.driver.find_element(*self.comfort_tariff).click()

    def click_phone_field(self):
        self.driver.find_element(*self.phone_field_button).click()

    def set_phone_number(self, phone):
        WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of_element_located(self.phone_input)
        )
        self.driver.find_element(*self.phone_input).send_keys(phone)

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def set_sms_code(self, code):
        WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of_element_located(self.sms_code_input)
        )
        self.driver.find_element(*self.sms_code_input).send_keys(code)

    def click_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    def click_payment_method(self):
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card(self):
        WebDriverWait(self.driver, 3).until(
            expected_conditions.element_to_be_clickable(self.add_card_button)
        )
        self.driver.find_element(*self.add_card_button).click()

    def set_card_number(self, card_number):
        WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of_element_located(self.card_number_input)
        )
        self.driver.find_element(*self.card_number_input).send_keys(card_number)

    def set_card_code(self, card_code):
        code_element = self.driver.find_element(*self.card_code_input)
        code_element.send_keys(card_code)
        # Se simula presionar TAB para cambiar el enfoque y activar el botón "Enlace"[cite: 2]
        code_element.send_keys(Keys.TAB)

    def click_link_card(self):
        WebDriverWait(self.driver, 3).until(
            expected_conditions.element_to_be_clickable(self.link_card_button)
        )
        self.driver.find_element(*self.link_card_button).click()

    def close_payment_modal(self):
        self.driver.find_element(*self.close_payment_modal_button).click()

    def set_message_for_driver(self, message):
        self.driver.find_element(*self.message_input).send_keys(message)

    def click_blanket_tissues_switch(self):
        self.driver.find_element(*self.blanket_tissues_switch).click()

    def add_ice_creams(self, count):
        for _ in range(count):
            self.driver.find_element(*self.ice_cream_plus_button).click()

    def get_ice_cream_count(self):
        return self.driver.find_element(*self.ice_cream_counter).text

    def click_order_taxi(self):
        self.driver.find_element(*self.order_taxi_button).click()

    def wait_for_driver_info(self):
        # Esta es la parte opcional: Espera extensa porque el conductor tarda unos segundos en ser asignado[cite: 2]
        WebDriverWait(self.driver, 40).until(
            expected_conditions.text_to_be_present_in_element(
                self.modal_driver_info, 'min'  # Verifica el texto de tiempo de llegada[cite: 3]
            )
        )
        return self.driver.find_element(*self.modal_driver_info).text


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        # Se añade un implicit wait global por precaución
        cls.driver.implicitly_wait(3)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to

        routes_page.set_from(address_from)
        routes_page.set_to(address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_tariff(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_request_taxi()
        routes_page.select_comfort_tariff()
        # Se valida que el texto 'Comfort' aparezca en la tarifa seleccionada (activa)
        assert "Comfort" in self.driver.find_element(By.XPATH, "//div[contains(@class, 'active')]").text

    def test_fill_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_phone_field()
        routes_page.set_phone_number(data.phone_number)
        routes_page.click_next_button()

        # Interceptamos el código enviado[cite: 2]
        sms_code = retrieve_phone_code(self.driver)
        routes_page.set_sms_code(sms_code)
        routes_page.click_confirm_button()

        assert self.driver.find_element(*routes_page.phone_field_button).text == data.phone_number

    def test_add_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_payment_method()
        routes_page.click_add_card()

        routes_page.set_card_number(data.card_number)
        routes_page.set_card_code(data.card_code)
        routes_page.click_link_card()
        routes_page.close_payment_modal()

        # Validación de cierre del modal y confirmación del método
        assert self.driver.find_element(*routes_page.payment_method_button).text == "Tarjeta"

    def test_write_message_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_message_for_driver(data.message_for_driver)
        assert self.driver.find_element(*routes_page.message_input).get_property('value') == data.message_for_driver

    def test_request_blanket_and_tissues(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_blanket_tissues_switch()
        # Validar que el input interno invisible haya cambiado su estado a seleccionado
        assert self.driver.find_element(By.CSS_SELECTOR, '.reqs-body .switch input').is_selected()

    def test_order_two_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_ice_creams(2)
        assert routes_page.get_ice_cream_count() == '2'

    def test_order_taxi_and_wait_for_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_order_taxi()

        # Valida que el modal cambie a la asignación de conductor[cite: 3]
        driver_info = routes_page.wait_for_driver_info()
        assert "min" in driver_info

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()