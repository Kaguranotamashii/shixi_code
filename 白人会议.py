import asyncio
import random
import string
from playwright.async_api import async_playwright


async def fill_input_random_text(page):
    # 生成五位随机字母，确保没有重复
    random_text = ''.join(random.sample(string.ascii_lowercase, 5))
    # 等待输入框出现，直到出现再继续
    await page.wait_for_selector('//html/body/div[15]/div/div[2]/input[1]', timeout=0)  # 无限制等待
    await page.fill('//html/body/div[15]/div/div[2]/input[1]', random_text)

    # 点击按钮
    await page.click('//html/body/div[15]/div/div[3]/button[1]')


async def main():
    async with async_playwright() as p:
        # 启动浏览器（无头模式，节省资源）
        browser = await p.chromium.launch(headless=True)  # 或使用 p.webkit.launch()
        context = await browser.new_context()

        # 打开20个页面
        pages = []
        for _ in range(5):
            print("正在打开页面...")
            page = await context.new_page()
            print( "页面已打开")
            await page.goto('https://aimeeting-login.ssk.ai/join/?room=mzcat8l2c1cr')
            print("页面已加载")

            pages.append(page)
            # 依次在每个页面上填入随机五位字母，并点击按钮
            tasks = [fill_input_random_text(page) for page in pages]
            print("正在输入随机文本...")
            await asyncio.gather(*tasks)
            print("输入完成")



        # 关闭浏览器
        # await browser.close()


# 启动异步任务
asyncio.run(main())
