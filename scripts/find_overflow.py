import asyncio
from playwright.async_api import async_playwright

async def find_overflow():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for width in [320, 375, 768, 1024]:
            for tab in ['#workspace', '#catalogue']:
                await page.set_viewport_size({'width': width, 'height': 700})
                await page.goto(f'http://localhost:3000/{tab}', wait_until='networkidle')
                res = await page.evaluate('''() => {
                    const overflowing = [];
                    const all = document.querySelectorAll('*');
                    for (const el of all) {
                        const rect = el.getBoundingClientRect();
                        if (rect.right > window.innerWidth + 2) {
                            overflowing.push({
                                tag: el.tagName,
                                id: el.id,
                                text: el.innerText ? el.innerText.slice(0, 30) : '',
                                className: el.className ? el.className.toString().slice(0, 60) : '',
                                right: Math.round(rect.right),
                                width: Math.round(rect.width)
                            });
                        }
                    }
                    return overflowing.slice(0, 5);
                }''')
                if res:
                    print(f'=== OVERFLOW AT {width}px on {tab} ===')
                    for item in res:
                        print(f"  {item['tag']}.{item['className']} | text: {item['text']} | right: {item['right']}px, width: {item['width']}px")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(find_overflow())

