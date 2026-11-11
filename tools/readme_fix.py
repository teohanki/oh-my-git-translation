NB = " "

NEW = [
    'The Windows build brings its own Git. On Linux and macOS, install Git first (`git --version` tells you if you have it). The app is not signed, so macOS blocks it on the first launch. Open System Settings → Privacy & Security, scroll down to Security, press Open Anyway and confirm. In the terminal, `xattr -cr "/Applications/Oh My Git!.app"` has the same effect. Tested on a Mac with an M1 Pro.',
    'Windows 版自带 Git。Linux 和 macOS 需要先安装 Git（在终端运行 `git --version` 可以检查）。应用没有签名，所以 macOS 在首次启动时会拦截它。打开系统设置 → Privacy & Security（隐私与安全性），向下滚动到 Security 部分，点击 Open Anyway（仍要打开）并确认。在终端运行 `xattr -cr "/Applications/Oh My Git!.app"` 效果相同。已在搭载 M1 Pro 的 Mac 上测试。',
    'La versión de Windows trae su propio Git. En Linux y macOS instala Git antes (`git --version` te dice si ya lo tienes). La app no está firmada, así que macOS la bloquea en el primer arranque. Abre Ajustes del Sistema → Privacy & Security (Privacidad y seguridad), baja hasta Security, pulsa Open Anyway (Abrir igualmente) y confirma. En la terminal, `xattr -cr "/Applications/Oh My Git!.app"` tiene el mismo efecto. Probado en un Mac con M1 Pro.',
    'La version Windows embarque son propre Git. Sous Linux et macOS, installez Git d\'abord (`git --version` indique si c\'est déjà fait). L\'application n\'est pas signée, donc macOS la bloque au premier lancement. Ouvrez Réglages Système → Privacy & Security (Confidentialité et sécurité), descendez jusqu\'à Security, cliquez sur Open Anyway (Ouvrir quand même) et confirmez. Dans le terminal, `xattr -cr "/Applications/Oh My Git!.app"` a le même effet. Testé sur un Mac avec une puce M1 Pro.',
    'A versão para Windows traz o próprio Git. No Linux e no macOS, instale o Git antes (`git --version` mostra se você já tem). O app não é assinado, então o macOS o bloqueia na primeira abertura. Abra Ajustes do Sistema → Privacy & Security (Privacidade e Segurança), role até Security, clique em Open Anyway (Abrir Mesmo Assim) e confirme. No terminal, `xattr -cr "/Applications/Oh My Git!.app"` tem o mesmo efeito. Testado em um Mac com M1 Pro.',
    'В сборку для Windows уже входит Git. На Linux и macOS Git нужно поставить заранее (`git --version` покажет, есть ли он). Приложение не подписано, поэтому при первом запуске macOS его блокирует. Откройте Системные настройки → Конфиденциальность и безопасность, прокрутите вниз до раздела «Безопасность», нажмите «Все равно открыть» и подтвердите. То же самое делает команда `xattr -cr "/Applications/Oh My Git!.app"` в терминале. Проверено на Mac с M1 Pro.',
    'Versi Windows sudah membawa Git sendiri. Di Linux dan macOS, pasang Git lebih dulu (`git --version` menunjukkan apakah sudah ada). Aplikasinya tidak ditandatangani, jadi macOS memblokirnya saat pertama dibuka. Buka Pengaturan Sistem → Privacy & Security (Privasi & Keamanan), gulir ke bagian Security, klik Open Anyway (Tetap Buka) dan konfirmasi. Di terminal, `xattr -cr "/Applications/Oh My Git!.app"` berefek sama. Diuji di Mac dengan M1 Pro.',
    'Die Windows-Version bringt ihr eigenes Git mit. Unter Linux und macOS installierst du Git vorher (`git --version` zeigt, ob es schon da ist). Die App ist nicht signiert, deshalb blockiert macOS sie beim ersten Start. Öffne Systemeinstellungen → Privacy & Security (Datenschutz & Sicherheit), scrolle zum Abschnitt Security, klicke auf Open Anyway (Trotzdem öffnen) und bestätige. Im Terminal hat `xattr -cr "/Applications/Oh My Git!.app"` dieselbe Wirkung. Getestet auf einem Mac mit M1 Pro.',
    'Windows 版には Git が同梱されています。Linux と macOS では先に Git をインストールしてください（ターミナルで `git --version` を実行すると確認できます）。アプリには署名がないため、macOS は初回起動時にブロックします。システム設定 → Privacy & Security（プライバシーとセキュリティ）を開き、Security の項目まで下にスクロールして、Open Anyway（このまま開く）を押し、確認します。ターミナルで `xattr -cr "/Applications/Oh My Git!.app"` を実行しても同じ結果になります。M1 Pro の Mac で動作を確認しました。',
    'Windows sürümü kendi Git\'iyle gelir. Linux ve macOS\'ta önce Git\'i kur (`git --version` kurulu olup olmadığını gösterir). Uygulama imzalı olmadığı için macOS ilk açılışta onu engeller. Sistem Ayarları → Privacy & Security (Gizlilik ve Güvenlik) bölümünü aç, Security kısmına kadar kaydır, Open Anyway (Yine de Aç) düğmesine bas ve onayla. Terminalde `xattr -cr "/Applications/Oh My Git!.app"` aynı etkiyi yapar. M1 Pro\'lu bir Mac\'te denendi.',
]

path = "README.md"
text = open(path, encoding="utf-8").read()
paragraphs = text.split("\n\n")
index = 0
for i, p in enumerate(paragraphs):
    if "xattr -cr" in p and p.startswith(("The Windows", "Windows ", "La ", "A versão", "В сборку", "Versi", "Die ", "Windows sürümü")):
        paragraphs[i] = NEW[index]
        index += 1
assert index == 10, index
open(path, "w", encoding="utf-8").write("\n\n".join(paragraphs))
