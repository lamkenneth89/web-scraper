from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def scrape_retail_sales():
    # 設置Chrome驅動
    driver = webdriver.Chrome()
    
    try:
        # 打開網站
        driver.get("https://www.censtatd.gov.hk/en/")
        
        # 等待搜索按鈕出現並點擊
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-btn"))
        )
        search_button.click()
        
        # 找到搜索框並輸入搜索詞
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchBox"))
        )
        search_input.send_keys("retail sales statistics")
        search_input.send_keys(Keys.RETURN)
        
        # 等待表格加載
        time.sleep(5)  # 給頁面一些加載時間
        
        # 找到所有表格
        tables = driver.find_elements(By.TAG_NAME, "table")
        
        # 將所有表格數據存儲到列表中
        all_data = []
        for table in tables:
            df = pd.read_html(table.get_attribute('outerHTML'))[0]
            all_data.append(df)
        
        # 將所有數據合併成一個DataFrame
        final_df = pd.concat(all_data, ignore_index=True)
        
        # 保存為CSV文件
        final_df.to_csv('retail_sales_data.csv', index=False)
        print("數據已成功保存到 retail_sales_data.csv")
        
    except Exception as e:
        print(f"發生錯誤: {str(e)}")
        
    finally:
        # 關閉瀏覽器
        driver.quit()

if __name__ == "__main__":
    scrape_retail_sales()