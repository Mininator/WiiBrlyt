# Wiibrlyt

**Wiibrlyt** est un logiciel Windows permettant de convertir les fichiers `.brlyt` (layouts graphiques Wii) et `.brlan` (animations) vers un format XML lisible : `.xmlyt`. Il s’adresse principalement aux créateurs et moddeurs de chaînes Wii, qu’elles soient officielles ou personnalisées, souhaitant modifier, comprendre ou documenter les interfaces et animations utilisées dans leurs projets.

---

## 🎯 Objectif

Wiibrlyt offre une interface simple, stable et accessible pour explorer et exporter des fichiers `.brlyt` / `.brlan` dans un format structuré lisible par l’humain. Le format `.xmlyt` facilite l’analyse, la modification manuelle ou la génération de fichiers via d'autres outils.

---

## 🧰 Fonctionnalités

- ✅ Conversion des fichiers `.brlyt` **et** `.brlan` vers `.xmlyt .xmlan`
- 🖱️ Interface graphique conviviale avec sélection de fichiers
- 📤 Export XML indenté, clair et modifiable
- 🔍 Analyse des structures internes (groupes, panes, matériaux, animations…)
- 🧠 Fiabilité assurée grâce au moteur **Benzin**
- 📝 Logs d’activité pour chaque conversion

---

## 🧑‍💻 Utilisation

1. Placez le fichier dans le dossier que vous avez téléchargé.
2. Lancez `Wiibrlyt.exe`
3. Cliquez sur **"Ouvrir un fichier"**
4. Sélectionnez un fichier `.brlyt` ou `.brlan`
5. Cliquez sur **"Convertir"**
6. Le fichier `.xmlyt .xmlan` est généré dans le même dossier que l’original

## ⚠️ Attention 
Veuillez bien désactiver votre antivirus.
---

## 🖥️ Compatibilité

| Plateforme | Statut        |
|------------|---------------|
| Windows 10 | ✅ Supporté    |
| Windows 11 | ✅ Supporté    |
| Linux      | ❌ à suivre    |
| macOS      | ❌ à suivre    |

---

## 🔧 Détails techniques

- **Langage** : Python 3
- **Compilation** : Nuitka (exécutable natif Windows)
- **Parsing** : moteur Benzin intégré
- **Interface** : simple GUI avec sélection de fichiers
- **Format de sortie** : `.xmlyt` (XML personnalisé)

---

## 🎯 Destiné à

Wiibrlyt permet d’extraire, analyser et modifier les layouts et animations de chaînes Wii officielles et personnalisées. Il est destiné à la personnalisation, l’adaptation ou l’étude de ces chaînes, mais **ne permet pas de créer une chaîne complète à partir de zéro**.

---

## 📦 État du projet

- Version actuelle : `v1.0.0`
- Statut : Stable
- Fonctionnalités à venir :
  - Prise en charge de `.brlyt` / `.brlan`
  - Affichage visuel de la hiérarchie
  - Conversion par lot

---

## 📄 Licence

Ce projet est sous licence **MIT**. Vous êtes libre de l’utiliser, le modifier et le redistribuer selon les termes de cette licence.

---

## 🤝 Contribuer

Les contributions sont bienvenues ! Proposez vos améliorations, corrigez des bugs ou ouvrez des issues pour suggérer de nouvelles fonctionnalités.

---

## 📬 Contact

Pour toute question ou retour :

- GitHub issues
- [Ton e-mail ou lien Discord ici]

---

## 💡 Exemple

```bash
Input : opening.brlyt
Output : opening.xmlyt
