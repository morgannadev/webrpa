# Import for the Web Bot
from botcity.web import WebBot, Browser, By
from botcity.web.parsers import table_to_dict

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Import pandas para transformar em csv
import pandas

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

def main():
    # Runner passes the server url, the id of the task being executed,
    # the access token and the parameters that this task receives (when applicable).
    maestro = BotMaestroSDK.from_sys_args()
    ## Fetch the BotExecution with details from the task, including parameters
    execution = maestro.get_execution()

    print(f"Task ID is: {execution.task_id}")
    print(f"Task Parameters are: {execution.parameters}")

    bot = WebBot()

    # Configure whether or not to run on headless mode
    bot.headless = False

    # Uncomment to change the default Browser to Firefox
    bot.browser = Browser.FIREFOX

    # Uncomment to set the WebDriver path
    bot.driver_path = r"C:\Users\Administrator\Documents\Projects\webrpa\WebRPA\resources\geckodriver.exe"

    # Opens the BotCity website.
    bot.browse("https://buscacepinter.correios.com.br/app/endereco/index.php")

    # Implement here your logic...
    # value_ = bot.find_element("", By.CLASS_NAME)
    campo_endereco = bot.find_element("endereco", By.ID)
    campo_endereco.send_keys("Avenida Brasil")

    bot.wait(1000)

    # botao_buscar = bot.find_element("btn_pesquisar", By.ID)
    # botao_buscar.click()
    bot.enter()

    tabela_enderecos = bot.find_element("resultado-DNEC", By.ID)
    lista_enderecos = table_to_dict(tabela_enderecos)
    for endereco in lista_enderecos:
        print(endereco)
    
    data_frame = pandas.DataFrame(lista_enderecos)
    data_frame.to_csv('test_pandas.csv')

    # Wait 3 seconds before closing
    bot.wait(3000)

    # Finish and clean up the Web Browser
    # You MUST invoke the stop_browser to avoid
    # leaving instances of the webdriver open
    bot.stop_browser()

    # Uncomment to mark this task as finished on BotMaestro
    # maestro.finish_task(
    #     task_id=execution.task_id,
    #     status=AutomationTaskFinishStatus.SUCCESS,
    #     message="Task Finished OK."
    # )


def not_found(label):
    print(f"Element not found: {label}")


if __name__ == '__main__':
    main()
