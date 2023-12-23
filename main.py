import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
import time
import PySimpleGUI as sg
import matplotlib.pyplot as plt

# -*- coding: utf-8 -*-

lista_judete = []
lista_post = [28531, 28538, 28543, 28547, 28558]


def site_actions(site_i):
    global lista_judete
    global lista_post
    lista_cazuri = []
    adresa_site = f"https://www.mai.gov.ro/informare-covid-19-grupul-de-comunicare-strategica-1{site_i}-decembrie-ora-13-00-2/"
    driver.get(adresa_site)
    close_campanie(driver)
    if site_i == 0:
        for j in range(2, 44):
            adrr = f"//*[@id=\"post-28531\"]/div/div/table[1]/tbody/tr[{j}]/td[2]"
            element = driver.find_element(by=By.XPATH, value=adrr)
            lista_judete.append(element.text)
            time.sleep(0.1)

    for j in range(2, 44):
        adrr = f"//*[@id=\"post-{lista_post[site_i]}\"]/div/div/table[1]/tbody/tr[{j}]/td[3]"
        element = driver.find_element(by=By.XPATH, value=adrr)
        lista_cazuri.append(element.text.replace('.', ''))

    return lista_cazuri


def close_campanie(driverx):
    try:
        agree_button = WebDriverWait(driverx, 5).until(
            ec.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div[1]/button')))
    except BaseException as e:
        agree_button = None

    if agree_button:
        agree_button.click()


def save_csv(file, fld):
    if bool(dictionar):
        df = pd.DataFrame(dictionar)
        df.to_csv(f"{fld}/{file}.csv", index=False, encoding='utf-8-sig', float_format='%.3f')
        sg.popup("CSV file saved successfully.")
        window.close()
    else:
        sg.popup_error("Please retrieve the data first.")


global dictionar


sg.theme('DarkAmber')

layout = [
    [sg.Text("Excel name"), sg.Input(key='_IN_')],
    [sg.B("Retrieve data", key='Retrieve data')],
    [sg.B("Create graph", key='Create graph')],
    [sg.B("Save csv", key='FolderBrowse')]
]

window = sg.Window('Covid Web Scraper',
                   layout, element_justification='c')

while True:
    event, values = window.read()

    print(event, values)

    if event in (None, '_exit_'):
        break

    if event == "Retrieve data":
        option = webdriver.ChromeOptions()
        option.add_argument('start-maximized')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        dictionar = {'NR. CRT': [], 'Judet': [], '10.12': [], '11.12': [], '12.12': [], '13.12': [], '14.12': []}

        for i in range(5):
            if i == 0:
                dictionar['10.12'] = site_actions(i)
                dictionar['Judet'] = lista_judete
            if i == 1:
                dictionar['11.12'] = site_actions(i)
            if i == 2:
                dictionar['12.12'] = site_actions(i)
            if i == 3:
                dictionar['13.12'] = site_actions(i)
            if i == 4:
                dictionar['14.12'] = site_actions(i)

        nr_crt_list = []
        for crt in range(42):
            nr_crt_list.append(crt + 1)
        dictionar['NR. CRT'] = nr_crt_list

        driver.quit()

    if event == "Create graph":

        if bool(dictionar):
            total_cases = []
            for date in ['10.12', '11.12', '12.12', '13.12', '14.12']:
                aux = dictionar[date]
                int_list = [int(x) for x in aux]
                total_cases.append(sum(int_list))
                print(int_list)

            plt.plot(['10.12', '11.12', '12.12', '13.12', '14.12'], total_cases, marker='o')
            plt.xlabel('Date')
            plt.ylabel('Total Cases')
            plt.title('Confirmed cases of Covid in Romania')
            plt.ticklabel_format(style='plain', axis='y')
            plt.show()
        else:
            sg.popup_error("Please retrieve the data first.")

    if event == "FolderBrowse":
        if values['_IN_']:
            folder = sg.popup_get_folder('Select a folder to save the CSV file')
            if folder:
                save_csv(values['_IN_'], folder)
        else:
            sg.popup_error('Please insert a name for the CSV file.')

window.close()