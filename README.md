# Wiibrlyt
![Logo de Wiibrlyt](banner.png)


**Wiibrlyt** est un logiciel Windows permettant de convertir les fichiers `.brlyt` (layouts graphiques Wii) et `.brlan` (animations) vers un format XML lisible : `.xmlyt`. Il s’adresse principalement aux créateurs et moddeurs de chaînes Wii, qu’elles soient officielles ou personnalisées, souhaitant modifier, comprendre ou documenter les interfaces et animations utilisées dans leurs projets.

---

## 🎯 Objectif

Wiibrlyt permet de convertir des fichiers plus facilement et simplement grâce au moteur 
Benzi.exe, plutôt que de passer par la ligne de commande.

---

## 🧰 Fonctionnalités

- ✅ Conversion des fichiers `.brlyt` **et** `.brlan` vers `.xmlyt .xmlan`
- 🖱️ Interface graphique conviviale avec sélection de fichiers
- 📤 Export XML indenté, clair et modifiable
- 🔍 Analyse des structures internes (groupes d'image .tpl, panes, matériaux, animations…)
- 🧠 Fiabilité assurée grâce au moteur **Benzin**
- 📝 Logs d’activité pour chaque conversion

---

## 🧑‍💻 Utilisation

- 1 Déchiffrer le dossier .zip
- 2 Lancez `Wiibrlyt.exe`
- 3 Cliquez sur **"Ouvrir un fichier"**
- 4 Sélectionnez un fichier `.brlyt` ou `.brlan`
- 5 Cliquez sur **"Convertir les fichiers"**
- 6 Le fichier `.xmlyt .xmlan` est généré dans le même dossier que l’original

## 🖥️ Compatibilité

| Plateforme | Statut        |
|------------|---------------|
| Windows 11/10 | ✅ Supporté    |
| Linux         | ❌ Non Supporté   |
| macOS         | ❌ Non Supporté    |

---

## 🔧 Détails techniques

- **Langage** : Python 
- **Compilation** : Pyinstaler(exécutable natif Windows)
- **Parsing** : moteur Benzin intégré
- **Interface** : simple GUI avec sélection de fichiers
- **Format de sortie** : `.xmlyt` ou `.xmlan` (XML personnalisé)

---

## 🎯 Destiné à

Wiibrlyt permet d’extraire, analyser et modifier les layouts et animations de chaînes Wii officielles et personnalisées. Il est destiné à la personnalisation, l’adaptation ou l’étude de ces chaînes, mais **ne permet pas de créer une chaîne complète à partir de zéro**.

---

## 📄 Licence

Ce projet est sous licence **MIT**. Vous êtes libre de l’utiliser, le modifier et le redistribuer selon les termes de cette licence.

---

## 🤝 Contribuer

Les contributions sont bienvenues ! Proposez vos améliorations, corrigez des bugs ou ouvrez des issues pour suggérer de nouvelles fonctionnalités.
---

## 💡 Exemple

```bash
Input : opening.brlyt
Output : opening.xmlyt
