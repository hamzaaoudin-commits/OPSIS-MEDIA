# OPSIS — applications iOS et Android (Capacitor)

Le code de l'application est le même que celui du site (`app/`). Ce dossier l'enveloppe dans deux vraies applications.

## Comptes à ouvrir (une seule fois)
| Service | Prix | Pour quoi |
|---|---|---|
| Apple Developer Program | 99 $/an | publier sur l'App Store |
| Google Play Console | 25 $ une fois | publier sur le Play Store |
| RevenueCat (gratuit au début) | 0 € | gérer l'abonnement 3,99 €/mois des deux stores |
| Supabase | 0 € | comptes, synchronisation (voir `docs/BACKEND.md`) |

Ensuite : `node tools/check-backend.js` vérifie que tout est branché.

## 1. Abonnement (RevenueCat)
1. App Store Connect → Abonnements : créer un groupe « OPSIS Originals » et un produit mensuel `opsis_monthly` à 3,99 €.
2. Play Console → Abonnements : même produit `opsis_monthly`, base plan mensuel à 3,99 €.
3. RevenueCat : créer le projet, ajouter l'app iOS et l'app Android, importer les produits, créer l'entitlement `premium`, une offering « default » avec un package mensuel.
4. Copier les clés publiques (`appl_…` et `goog_…`) dans `native/native.config.json` (`revenueCatIosKey`, `revenueCatAndroidKey`).
Tant que ces clés sont vides, l'app reste ouverte (pas de paywall).

## 2. Connexion Apple / Google
Renseigner dans `native.config.json` : `googleWebClientId`, `googleIosClientId` (Google Cloud → OAuth). Activer les fournisseurs Apple et Google dans Supabase → Authentication.

## 2 bis. Clés à renseigner, puis vérification
Remplir `native/native.config.json` (Supabase, RevenueCat, Google), puis lancer `npm run check` dans `native/` : il liste ce qui manque.
- Google Cloud : créer un client OAuth « Application Web » (`googleWebClientId`), un client « iOS » (bundle id `com.strawberryproduction.opsis`, `googleIosClientId`) et un client « Android » (package `com.strawberryproduction.opsis` + empreinte SHA-1 de la clé de signature, y compris celle de Play App Signing).
- Le script `npm run sync` ajoute tout seul la configuration Google dans Info.plist.

## 3. Préparer (Mac mini)
```
git clone <opsis-media> && cd opsis-media
node tools/build.js            # génère app/
cd native && npm ci
npm run sync                   # copie le web dans www/ et synchronise iOS/Android
```
## 4. iOS
`npx cap open ios` (Xcode récent requis, Capacitor 8) →
- Signing & Capabilities : choisir votre Team ; bundle id `com.strawberryproduction.opsis`
- Ajouter les capabilities **In-App Purchase** et **Sign in with Apple**
- Product → Archive → Distribute App → App Store Connect
- Dans App Store Connect : fiche (voir `docs/STORE.md`), captures `native/store/screenshots/iphone-*` et `ipad-*`, lier l'abonnement à la version, envoyer en revue.

## 5. Android
`npx cap open android` (Android Studio) →
- Créer la clé de signature (une seule fois, à garder précieusement, jamais dans git) :
  `keytool -genkey -v -keystore ~/opsis-release.jks -keyalg RSA -keysize 2048 -validity 10000 -alias opsis`
  puis créer `native/android/keystore.properties` avec `storeFile=/Users/…/opsis-release.jks`, `storePassword=…`, `keyAlias=opsis`, `keyPassword=…`.
- Augmenter `versionCode` dans `android/app/build.gradle` à chaque envoi.
- Build → Generate Signed Bundle (AAB) ou `cd android && ./gradlew bundleRelease`.
- Play Console → Production → importer l'AAB, remplir la fiche (`docs/STORE.md`), captures `android-phone-*`.
- Les nouveaux comptes personnels doivent faire un test fermé (12 testeurs, 14 jours) avant la production.

## Mises à jour
Modifier le web → `node tools/build.js` → `cd native && npm run sync` → ré-archiver, incrémenter la version/build.
