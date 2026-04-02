import asyncio
import random
import pandas as pd
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# --- CONFIGURATION ---
EXCEL_PATH = "comptes.xlsx"
PROXY_PATH = "proxies.txt"
PASSWORD_FIXE = "MonSuperMdp2026!"
URL_INSCRIPTION = "https://www.instant-gaming.com/fr/creer-un-compte/"

async def human_type(element, text):
    """Tape du texte de manière humaine"""
    for char in text:
        await element.type(char, delay=random.randint(50, 150))

async def run_bot(email, proxy):
    async with async_playwright() as p:
        # Configuration Proxy
        browser_args = {}
        if proxy:
            browser_args['proxy'] = {"server": f"http://{proxy}"}
            
        browser = await p.chromium.launch(headless=True, **browser_args)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        await stealth_async(page)

        try:
            print(f"--- Tentative pour : {email} ---")
            await page.goto(URL_INSCRIPTION, wait_until="networkidle")

            # Remplissage des champs (Sélecteurs IG)
            await page.fill("#ig-email", email)
            await page.fill("#ig-pass", PASSWORD_FIXE)
            await page.fill("#ig-firstname", "Jean") # Tu peux varier via Excel aussi
            await page.fill("#ig-lastname", "Dupont")
            
            # Date de naissance aléatoire (Majeur)
            birth = f"{random.randint(10,28)}/0{random.randint(1,9)}/1995"
            await page.fill("#ig-birthdate", birth)

            # Accepter les CGU (clic sur la zone visuelle)
            await page.click("label[for='ig-register-terms-input']")

            # Pause aléatoire "réflexion humaine"
            await asyncio.sleep(random.uniform(2, 5))

            # Clic sur envoyer
            await page.click("#ajax-register-btn")

            # Attendre de voir si on change de page ou si une erreur apparaît
            await page.wait_for_timeout(5000)
            print(f"Fini pour {email}. Vérifie le résultat.")

        except Exception as e:
            print(f"Erreur sur {email} : {e}")
        finally:
            await browser.close()

async def main():
    # 1. Charger les emails depuis Excel
    df = pd.read_excel(EXCEL_PATH)
    emails = df['email'].tolist()

    # 2. Charger les proxies
    with open(PROXY_PATH, 'r') as f:
        proxies = [line.strip() for line in f.readlines() if line.strip()]

    for i, email in enumerate(emails):
        proxy = proxies[i % len(proxies)] if proxies else None
        
        await run_bot(email, proxy)

        # 3. La pause de 10 minutes (600 secondes)
        if i < len(emails) - 1:
            wait_sec = 600 + random.randint(-20, 40)
            print(f"Patienter {wait_sec} secondes avant le prochain compte...")
            await asyncio.sleep(wait_sec)

if __name__ == "__main__":
    asyncio.run(main())
