import asyncio
import random
import pandas as pd
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# --- CONFIGURATION ---
EXCEL_PATH = "comptes.xlsx"  # Vérifie que le fichier est dans le même dossier
PASSWORD_FIXE = "MonSuperMdp2026!"
URL_INSCRIPTION = "https://www.instant-gaming.com/fr/creer-un-compte/"

async def human_type(page, selector, text):
    """Simule une frappe clavier humaine avec des délais aléatoires"""
    await page.wait_for_selector(selector)
    for char in text:
        await page.type(selector, char, delay=random.randint(70, 200))

async def run_bot(email):
    async with async_playwright() as p:
        # Lancement classique sans proxy
        browser = await p.chromium.launch(headless=True) 
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # Activation du mode furtif
        await stealth_async(page)

        try:
            print(f"\n--- Inscription en cours : {email} ---")
            await page.goto(URL_INSCRIPTION, wait_until="networkidle")

            # 1. Remplissage de l'Email
            await human_type(page, "#ig-email", email)

            # 2. Mot de passe
            await human_type(page, "#ig-pass", PASSWORD_FIXE)

            # 3. Identité (Tu peux aussi les tirer d'Excel si tu veux)
            await human_type(page, "#ig-firstname", "Marc")
            await human_type(page, "#ig-lastname", "Lavoine")
            
            # 4. Date de naissance
            await human_type(page, "#ig-birthdate", "15/05/1992")

            # 5. Cocher les CGU
            # On clique sur le texte du label pour être sûr que le clic est bien pris en compte
            await page.click("label[for='ig-register-terms-input']")
            await asyncio.sleep(1)

            # 6. Petit mouvement de souris aléatoire avant de valider
            await page.mouse.move(random.randint(100, 600), random.randint(100, 600))

            # 7. Clic sur le bouton Envoyer
            print("Envoi du formulaire...")
            await page.click("#ajax-register-btn")

            # Attendre 10 secondes pour voir le message de confirmation
            await asyncio.sleep(10)
            
            # Vérification basique
            if "check-mail" in page.url:
                print(f"✅ Compte créé pour {email} (Vérifie tes mails)")
            else:
                print(f"⚠️ Formulaire envoyé pour {email}, vérifie manuellement si le compte est créé.")

        except Exception as e:
            print(f"❌ Erreur pour {email} : {e}")
        finally:
            await browser.close()

async def main():
    try:
        # Lecture du fichier Excel
        df = pd.read_excel(EXCEL_PATH)
        emails = df['email'].tolist()
        print(f"Nombre d'emails chargés : {len(emails)}")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier Excel : {e}")
        return

    for i, email in enumerate(emails):
        await run_bot(email)

        # Pause de 10 minutes (600 secondes) entre chaque compte
        if i < len(emails) - 1:
            # On ajoute un "jitter" de 30s pour ne pas être trop prévisible
            wait_sec = 600 + random.randint(-30, 30)
            print(f"Attente de {wait_sec // 60} minutes avant le prochain...")
            await asyncio.sleep(wait_sec)

if __name__ == "__main__":
    asyncio.run(main())
