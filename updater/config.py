import deepl
import sqlite3

class Config:
    
    db_connection = sqlite3.connect('world_headline.db')
    
    country_names = ['United States', 'China', 'German', 'Japan', 'India', 'United Kingdom', 'Franch', 'Russia', 'Korea']
    
    news_empty_img_url = "https://via.placeholder.com/150"
    
    src_lang_by_counrty = {
            'United States' : 'EN',
            'China'         : 'ZH',
            'German'        : 'DE',
            'Japan'         : 'JA',
            'India'         : 'EN',
            'United Kingdom': 'EN',
            'Franch'        : 'FR',
            'Russia'        : 'RU',
            'Korea'         : 'KO'
        }
    
    target_lang_by_country = {
            'United States' : 'EN-US',
            'China'         : 'ZH',
            'German'        : 'DE',
            'Japan'         : 'JA',
            'India'         : 'EN-GB',
            'United Kingdom': 'EN-GB',
            'Franch'        : 'FR',
            'Russia'        : 'RU',
            'Korea'         : 'KO'                       
        }
    
    target_langs = ['EN-US', 'ZH', 'DE', 'JA', 'EN-GB', 'FR', 'RU', 'KO']
    deepl_auth_key = '2f9ac10f-8d05-4dd1-b715-00f03482f297:fx'
    deepl_translator = deepl.Translator(deepl_auth_key)