# 🧠 githetic

> Un git-like en python.

---

## 🔧 Objectif

Ce projet vise à implémenter une version simplifiée de Git en se concentrant sur ses fondements : les objets, les arbres, les commits, et les commandes utilisateur les plus utilisées. Le travail a été réparti en 4 parties indépendantes afin de couvrir l’essentiel du fonctionnement de Git.

---

## 👥 Répartition des tâches

| Étudiant  | Partie                      | Détails des commandes / fonctionnalités                      |
|----------|-----------------------------|--------------------------------------------------------------|
| Mikaël   | 🛠️ Plumbing Commands         | `hash-object`, `cat-file`, `write-tree`, `commit-tree`       |
| Mehdi    | 🧩 Commandes Porcelain 1     | `init`, `add`, `rm`, `commit`, `status`                      |
| Saad     | 🧰 Commandes Porcelain 2     | `checkout`, `reset`, `log`, `ls-files`, `ls-tree`, `rev-parse`, `show-ref` |
| Grégoire | 🚀 Fonctionnalités Avancées  | `merge`, gestion de `.gitignore`, gestion de l'index, gestion des erreurs globales |

---

## 🕒 Déroulement

Nous avons commencé par diviser le projet en quatre modules bien distincts, chacun étant conçu pour être autonome tout en contribuant à la cohérence globale de `githetic`.

Chaque membre de l’équipe a travaillé en parallèle sur sa partie, en s'assurant régulièrement de l’intégration avec les autres modules. 

Une fois chaque partie terminée, nous avons fusionné nos modules en effectuant des tests croisés afin de garantir l’interopérabilité et la stabilité globale du projet.

---

## ✅ Résultat

Le projet **githetic** fonctionne comme une base solide pour comprendre les principes fondamentaux de Git. Il permet de créer des objets Git à la main, de gérer des commits, d'explorer les références et même de simuler certaines opérations avancées comme les merges ou la gestion d’index.

---

## 💡 À retenir

- Une bonne répartition des tâches nous a permis de progresser rapidement sans conflit.
- Travailler sur les commandes dites "plumbing" donne une vraie vision de ce qu’il se passe sous le capot.
- Implémenter des fonctionnalités avancées comme `merge` ou `.gitignore` nous a permis d'aller plus loin que la simple manipulation d’objets.

---

> Fait avec 💻 et 🧠 par Mehdi Benchrif, Mikaël Lahlou, Saad Abi et Grégoire Mercier.
