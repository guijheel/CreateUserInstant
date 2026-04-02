import asyncio
import random
import pandas as pd
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# --- CONFIGURATION ---
EXCEL_PATH = "comptes.xlsx"
PASSWORD_FIXE = "MonSuperMdp2026!"
URL_INSCRIPTION = "https://www.instant-gaming.com/fr/creer-un-compte/"

# Listes pour l'invention des noms
LISTE_PRENOMS = ["Thomas", "Nicolas", "Julien", "Kevin", "Lucas", "Antoine", "Maxime", "Alexandre", "Mathieu", "Clément"]
LISTE_NOMS = ["Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre", "Michel", "Garcia", "David", "Bertrand"]

async def human_type(page, selector, text):
    """Simule une frappe clavier humaine"""
    await page.wait_for_selector(selector)
    for char in text:
        await page.type(selector, char, delay=random.randint(50, 150))

async def run_bot(email):
    # Invention du nom et prénom pour ce compte précis
    prenom_invente = random.choice(LISTE_PRENOMS)
    nom_invente = random.choice(LISTE_NOMS)
    
    async with async_playwright() as p:
        # headless=False si tu veux voir le navigateur s'ouvrir
        browser = await p.chromium.launch(headless=True) 
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        await stealth_async(page)

        try:
            print(f"\n--- Inscription : {email} ({prenom_invente} {nom_invente}) ---")
            await page.goto(URL_INSCRIPTION, wait_until="networkidle")

            # 1. Email
            await human_type(page, "#ig-email", email)

            # 2. Mot de passe
            await human_type(page, "#ig-pass", PASSWORD_FIXE)

            # 3. Prénom et Nom inventés
            await human_type(page, "#ig-firstname", prenom_invente)
            await human_type(page, "#ig-lastname", nom_invente)
            
            # 4. Date de naissance aléatoire (entre 18 et 35 ans)
            annee = random.randint(1990, 2005)
            jour = str(random.randint(10, 28))
            mois = f"0{random.randint(1, 9)}"
            await human_type(page, "#ig-birthdate", f"{jour}/{mois}/{annee}")

            # 5. CGU
            await page.click("label[for='ig-register-terms-input']")
            await asyncio.sleep(random.uniform(1, 3))

            # 6. Validation
            print("Envoi du formulaire...")
            await page.click("#ajax-register-btn")

            # Attendre de voir si l'URL change ou si un message d'erreur apparaît
            await asyncio.sleep(8)
            
            if "check-mail" in page.url:
                print(f"✅ Succès pour {email}")
            else:
                print(f"⚠️ Terminé pour {email}. Vérifie si le compte est créé.")

        except Exception as e:
            print(f"❌ Erreur pour {email} : {e}")
        finally:
            await browser.close()

async def main():
    try:
        # On ne récupère que la colonne 'email'
        df = pd.read_excel(EXCEL_PATH)
        emails = df['email'].dropna().tolist() # .dropna() enlève les lignes vides
        print(f"Démarrage : {len(emails)} emails chargés.")
    except Exception as e:
        print(f"Erreur Excel : {e}")
        return

    for i, email in enumerate(emails):
        await run_bot(email)

        if i < len(emails) - 1:
            # Pause de 10 minutes (600s) + un peu de hasard
            attente = 600 + random.randint(-20, 40)
            print(f"Prochain compte dans {attente // 60} min {attente % 60} sec...")
            await asyncio.sleep(attente)

if __name__ == "__main__":
    asyncio.run(main())
