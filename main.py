import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

# --- CONFIGURATION ---
TXT_PATH = "emails.txt"  # Ton fichier texte
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
    # Invention du nom et prénom
    prenom_invente = random.choice(LISTE_PRENOMS)
    nom_invente = random.choice(LISTE_NOMS)
    
    async with async_playwright() as p:
        # headless=True pour ne pas voir la fenêtre, False pour débugger
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

            # 3. Prénom et Nom
            await human_type(page, "#ig-firstname", prenom_invente)
            await human_type(page, "#ig-lastname", nom_invente)
            
            # 4. Date de naissance
            annee = random.randint(1990, 2005)
            date_str = f"{random.randint(10, 28)}/0{random.randint(1, 9)}/{annee}"
            await human_type(page, "#ig-birthdate", date_str)

            # 5. Cocher les CGU
            await page.click("label[for='ig-register-terms-input']")
            await asyncio.sleep(random.uniform(1, 2))

            # 6. Validation
            print("Clic sur Envoyer...")
            await page.click("#ajax-register-btn")

            # Attente de confirmation (URL ou message)
            await asyncio.sleep(10)
            
            if "check-mail" in page.url:
                print(f"✅ Compte créé avec succès pour {email}")
            else:
                print(f"⚠️ Formulaire soumis. Vérifie manuellement pour {email}")

        except Exception as e:
            print(f"❌ Erreur sur {email} : {e}")
        finally:
            await browser.close()

async def main():
    # Lecture du fichier TXT
    try:
        with open(TXT_PATH, "r", encoding="utf-8") as f:
            # On récupère chaque ligne, on enlève les espaces et on ignore les lignes vides
            emails = [line.strip() for line in f.readlines() if line.strip()]
        
        if not emails:
            print("Le fichier emails.txt est vide.")
            return
            
        print(f"Démarrage : {len(emails)} emails trouvés dans le fichier.")
    except FileNotFoundError:
        print(f"Erreur : Le fichier {TXT_PATH} n'existe pas.")
        return

    for i, email in enumerate(emails):
        await run_bot(email)

        # Pause de 10 minutes (600s) entre chaque compte
        if i < len(emails) - 1:
            attente = 600 + random.randint(-15, 30)
            print(f"Attente de {attente // 60} min avant le prochain mail...")
            await asyncio.sleep(attente)

if __name__ == "__main__":
    asyncio.run(main())
