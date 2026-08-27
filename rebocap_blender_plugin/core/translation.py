import bpy

TRANSLATIONS = {
    "Connection": {
        "zh_CN": "连接与录制",
        "ja_JP": "接続と録画",
        "zh_TW": "連接與錄製",
        "es_ES": "Conexión y Grabación",
        "fr_FR": "Connexion et Enregistrement",
        "ko_KR": "연결 및 녹화",
        "ru_RU": "Подключение и запись",
        "en_US": "Connection & Recording",
        "it_IT": "Connessione e Registrazione"
    },
    "Character Skeleton": {
        "zh_CN": "创建角色骨架",
        "ja_JP": "キャラクタースケルトンを作成",
        "zh_TW": "創建角色骨架",
        "es_ES": "Crear Esqueleto",
        "fr_FR": "Créer un Squelette",
        "ko_KR": "캐릭터 골격 생성",
        "ru_RU": "Создание скелета персонажа",
        "en_US": "Create Character Skeleton",
        "it_IT": "Crea Scheletro Personaggio"
    },
    "FK Animation Mode": {
        "zh_CN": "角色骨骼直驱模式 (FK Animation)",
        "ja_JP": "キャラクターFKモード (FK Animation)",
        "zh_TW": "角色骨骼直驅模式 (FK Animation)",
        "es_ES": "Modo de Animación FK",
        "fr_FR": "Mode d'Animation FK",
        "ko_KR": "캐릭터 FK 모드",
        "ru_RU": "Режим FK анимации",
        "en_US": "FK Animation Mode",
        "it_IT": "Modalità Animazione FK"
    },
    "Tracking Point Mode": {
        "zh_CN": "追踪点模式 (Tracking Point Mode)",
        "ja_JP": "トラッキングポイントモード (Tracking Point)",
        "zh_TW": "追蹤點模式 (Tracking Point Mode)",
        "es_ES": "Modo de Puntos de Rastreo",
        "fr_FR": "Mode Points de Suivi",
        "ko_KR": "트래킹 포인트 모드",
        "ru_RU": "Режим точек отслеживания",
        "en_US": "Tracking Point Mode",
        "it_IT": "Modalità Punti di Tracciamento"
    },
    "Version: Beta 11.5": {
        "zh_CN": "Version: Beta 11.5",
        "ja_JP": "Version: Beta 11.5",
        "en_US": "Version: Beta 11.5",
        "zh_TW": "Version: Beta 11.5",
        "es_ES": "Version: Beta 11.5",
        "fr_FR": "Version: Beta 11.5",
        "ko_KR": "Version: Beta 11.5",
        "ru_RU": "Version: Beta 11.5",
        "it_IT": "Versione: Beta 11.5"
    },
    "Version: Beta 11.4": {
        "zh_CN": "Version: Beta 11.4",
        "ja_JP": "Version: Beta 11.4",
        "zh_TW": "Version: Beta 11.4",
        "en_US": "Version: Beta 11.4",
        "es_ES": "Version: Beta 11.4",
        "fr_FR": "Version: Beta 11.4",
        "ko_KR": "Version: Beta 11.4",
        "ru_RU": "Version: Beta 11.4",
        "it_IT": "Versione: Beta 11.4"
    },
    "Version: Beta 11.3": {
        "zh_CN": "Version: Beta 11.3",
        "ja_JP": "Version: Beta 11.3",
        "zh_TW": "Version: Beta 11.3",
        "en_US": "Version: Beta 11.3",
        "es_ES": "Version: Beta 11.3",
        "fr_FR": "Version: Beta 11.3",
        "ko_KR": "Version: Beta 11.3",
        "ru_RU": "Version: Beta 11.3",
        "it_IT": "Versione: Beta 11.3"
    },
    "Version: Beta 11.2": {
        "zh_CN": "Version: Beta 11.2",
        "ja_JP": "Version: Beta 11.2",
        "zh_TW": "Version: Beta 11.2",
        "en_US": "Version: Beta 11.2",
        "es_ES": "Version: Beta 11.2",
        "fr_FR": "Version: Beta 11.2",
        "ko_KR": "Version: Beta 11.2",
        "ru_RU": "Version: Beta 11.2",
        "it_IT": "Versione: Beta 11.2"
    },
    "Version: Beta 11.1": {
        "zh_CN": "Version: Beta 11.1",
        "ja_JP": "Version: Beta 11.1",
        "zh_TW": "Version: Beta 11.1",
        "en_US": "Version: Beta 11.1",
        "es_ES": "Version: Beta 11.1",
        "fr_FR": "Version: Beta 11.1",
        "ko_KR": "Version: Beta 11.1",
        "ru_RU": "Version: Beta 11.1",
        "it_IT": "Versione: Beta 11.1"
    },
    "Restore T-Pose": {
        "zh_CN": "恢复 T-Pose",
        "ja_JP": "Tポーズに戻す",
        "zh_TW": "恢復 T-Pose",
        "es_ES": "Restaurar T-Pose",
        "fr_FR": "Restaurer T-Pose",
        "ko_KR": "T-포즈 복구",
        "ru_RU": "Сброс T-Pose",
        "en_US": "Restore T-Pose",
        "it_IT": "Ripristina T-Pose"
    },
    "Wait": {
        "zh_CN": "等待",
        "ja_JP": "待機",
        "zh_TW": "等待",
        "es_ES": "Esperar",
        "fr_FR": "Attendre",
        "ko_KR": "대기",
        "ru_RU": "Ожидание",
        "en_US": "Wait",
        "it_IT": "Attendi"
    },
    "No bone selected.": {
        "zh_CN": "未选中任何骨骼。",
        "ja_JP": "ボーンが選択されていません。",
        "zh_TW": "未選中任何骨骼。",
        "en_US": "No bone selected.",
        "es_ES": "Ningún hueso seleccionado.",
        "fr_FR": "Aucun os sélectionné.",
        "ko_KR": "선택된 뼈가 없습니다.",
        "ru_RU": "Кость не выбрана.",
        "it_IT": "Nessun osso selezionato."
    },
    "Please select an armature object.": {
        "zh_CN": "请选择一个骨架物体。",
        "ja_JP": "アーマチュアオブジェクトを選択してください。",
        "zh_TW": "請選擇一個骨架物體。",
        "en_US": "Please select an armature object.",
        "es_ES": "Por favor seleccione un objeto de armadura.",
        "fr_FR": "Veuillez sélectionner un objet armature.",
        "ko_KR": "아마추어 오브젝트를 선택하십시오.",
        "ru_RU": "Пожалуйста, выберите объект арматуры.",
        "it_IT": "Seleziona un oggetto armatura."
    },
    "Selected bone": {
        "zh_CN": "已选骨骼",
        "ja_JP": "選択されたボーン",
        "zh_TW": "已選骨骼",
        "en_US": "Selected bone",
        "es_ES": "Hueso seleccionado",
        "fr_FR": "Os sélectionné",
        "ko_KR": "선택된 뼈",
        "ru_RU": "Выбранная кость",
        "it_IT": "Osso selezionato"
    },
    "Bone map exported successfully": {
        "zh_CN": "骨骼映射导出成功",
        "ja_JP": "ボーンマップのエクスポートに成功しました",
        "zh_TW": "骨骼映射導出成功",
        "en_US": "Bone map exported successfully",
        "es_ES": "Mapeo de huesos exportado con éxito",
        "fr_FR": "Mappage d'os exporté avec succès",
        "ko_KR": "뼈 매핑을 성공적으로 내보냈습니다",
        "ru_RU": "Карта костей успешно экспортирована",
        "it_IT": "Mappatura delle ossa esportata con successo"
    },
    "Bone map imported successfully": {
        "zh_CN": "骨骼映射导入成功",
        "ja_JP": "ボーンマップのインポートに成功しました",
        "zh_TW": "骨骼映射導入成功",
        "en_US": "Bone map imported successfully",
        "es_ES": "Mapeo de huesos importado con éxito",
        "fr_FR": "Mappage d'os importé avec succès",
        "ko_KR": "뼈 매핑을 성공적으로 가져왔습니다",
        "ru_RU": "Карта костей успешно импортирована",
        "it_IT": "Mappatura delle ossa importata con successo"
    },
    "Import failed": {
        "zh_CN": "导入失败",
        "ja_JP": "インポートに失敗しました",
        "zh_TW": "導入失敗",
        "en_US": "Import failed",
        "es_ES": "Error al importar",
        "fr_FR": "Échec de l'importation",
        "ko_KR": "가져오기 실패",
        "ru_RU": "Ошибка импорта",
        "it_IT": "Importazione non riuscita"
    },
    "* Please bind Pelvis and Legs first": {
        "zh_CN": "* 请先绑定骨盆和腿部骨骼",
        "ja_JP": "* 最初に骨盤と脚のボーンをバインドしてください",
        "zh_TW": "* 請先綁定骨盆和腿部骨骼",
        "en_US": "* Please bind Pelvis and Legs first",
        "es_ES": "* Primero vincule la pelvis y las piernas",
        "fr_FR": "* Veuillez d'abord lier le bassin et les jambes",
        "ko_KR": "* 먼저 골반과 다리 뼈를 바인딩하세요",
        "ru_RU": "* Сначала привяжите таз и кости ног",
        "it_IT": "* Associa prima il bacino e le ossa delle gambe"
    },
    "Ankle Height": {
        "zh_CN": "脚踝高度",
        "ja_JP": "足首の高さ",
        "zh_TW": "腳踝高度",
        "en_US": "Ankle Height",
        "es_ES": "Altura del tobillo",
        "fr_FR": "Hauteur de la cheville",
        "ko_KR": "발목 높이",
        "ru_RU": "Высота лодыжки",
        "it_IT": "Altezza Caviglia"
    },
    "Mode: Applied Skeleton": {
        "zh_CN": "模式: 已应用骨架",
        "ja_JP": "モード: 適用済み骨格",
        "zh_TW": "模式: 已應用骨架",
        "en_US": "Mode: Applied Skeleton",
        "es_ES": "Modo: Esqueleto aplicado",
        "fr_FR": "Mode : Squelette appliqué",
        "ko_KR": "모드: 적용된 골격",
        "ru_RU": "Режим: Примененный скелет",
        "it_IT": "Modalità: Scheletro Applicato"
    },
    "Mode: Manual Skeleton": {
        "zh_CN": "模式: 手动骨架",
        "ja_JP": "モード: 手動骨格",
        "zh_TW": "模式: 手動骨架",
        "en_US": "Mode: Manual Skeleton",
        "es_ES": "Modo: Esqueleto manual",
        "fr_FR": "Mode : Squelette manuel",
        "ko_KR": "모드: 수동 골격",
        "ru_RU": "Режим: Ручной скелет",
        "it_IT": "Modalità: Scheletro Manuale"
    },
    "✅ Rebocap Standard": {
        "zh_CN": "✅ Rebocap 标准骨骼 (Rebocap Standard)",
        "ja_JP": "✅ Rebocap 標準ボーン (Rebocap Standard)",
        "zh_TW": "✅ Rebocap 標準骨骼 (Rebocap Standard)",
        "en_US": "✅ Rebocap Standard",
        "es_ES": "✅ Estándar Rebocap",
        "fr_FR": "✅ Standard Rebocap",
        "ko_KR": "✅ Rebocap 표준",
        "ru_RU": "✅ Стандарт Rebocap",
        "it_IT": "✅ Standard Rebocap"
    },
    "✅ Unreal Engine (UE4/UE5/MetaHuman)": {
        "zh_CN": "✅ 虚幻引擎标准 (UE4/UE5/MetaHuman)",
        "ja_JP": "✅ Unreal Engine 標準 (UE4/UE5/MetaHuman)",
        "zh_TW": "✅ 虛幻引擎標準 (UE4/UE5/MetaHuman)",
        "en_US": "✅ Unreal Engine (UE4/UE5/MetaHuman)",
        "es_ES": "✅ Unreal Engine (UE4/UE5/MetaHuman)",
        "fr_FR": "✅ Unreal Engine (UE4/UE5/MetaHuman)",
        "ko_KR": "✅ 언리얼 엔진 (UE4/UE5/MetaHuman)",
        "ru_RU": "✅ Unreal Engine (UE4/UE5/MetaHuman)",
        "it_IT": "✅ Unreal Engine (UE4/UE5/MetaHuman)"
    },
    "✅ VRM Humanoid": {
        "zh_CN": "✅ VRM 人形骨架 (VRM Humanoid)",
        "ja_JP": "✅ VRM ヒューマノイド (VRM Humanoid)",
        "zh_TW": "✅ VRM 人形骨架 (VRM Humanoid)",
        "en_US": "✅ VRM Humanoid",
        "es_ES": "✅ VRM Humanoide",
        "fr_FR": "✅ VRM Humanoïde",
        "ko_KR": "✅ VRM 휴머노이드",
        "ru_RU": "✅ VRM Гуманоид",
        "it_IT": "✅ VRM Umanoide"
    },
    "保持角色当前起点 (Keep Character Position)": {
        "zh_CN": "保持角色当前起点 (Keep Character Position)",
        "ja_JP": "キャラクターの現在位置を保持 (Keep Position)",
        "en_US": "Keep Character Position",
        "zh_TW": "保持角色當前起點",
        "es_ES": "Mantener Posición Inicial",
        "fr_FR": "Garder Position Initiale",
        "ko_KR": "현재 위치 유지",
        "ru_RU": "Сохранить начальную позицию",
        "it_IT": "Mantieni Posizione Attuale del Personaggio"
    },
    "挂载与导出帧率设置 (FPS Mode):": {
        "zh_CN": "挂载与导出帧率设置 (FPS Mode):",
        "ja_JP": "適用とエクスポートのFPS設定 (FPS Mode):",
        "en_US": "Apply / Export FPS Settings:",
        "zh_TW": "掛載與導出幀率設置 (FPS Mode):",
        "es_ES": "Configuración de FPS de Aplicación / Exportación:",
        "fr_FR": "Paramètres FPS d'Application / Exportation :",
        "ko_KR": "적용 및 내보내기 FPS 설정 (FPS Mode):",
        "ru_RU": "Настройки FPS применения и экспорта:",
        "it_IT": "Impostazioni FPS di Applicazione ed Esportazione:"
    },
    "导出片段json": {
        "zh_CN": "导出片段json",
        "ja_JP": "テイクJSONを書き出し",
        "en_US": "Export Take JSON",
        "zh_TW": "導出片段json",
        "es_ES": "Exportar JSON de Toma",
        "fr_FR": "Exporter JSON de Prise",
        "ko_KR": "테이크 JSON 내보내기",
        "ru_RU": "Экспорт JSON дубля",
        "it_IT": "Esporta JSON Registrazione"
    },
    "导入片段json": {
        "zh_CN": "导入片段json",
        "ja_JP": "テイクJSONを読み込み",
        "en_US": "Import Take JSON",
        "zh_TW": "導入片段json",
        "es_ES": "Importar JSON de Toma",
        "fr_FR": "Importer JSON de Prise",
        "ko_KR": "테이크 JSON 가져오기",
        "ru_RU": "Импорт JSON дубля",
        "it_IT": "Importa JSON Registrazione"
    },
    "插件录制时按60fps记录母带保存，": {
        "zh_CN": "插件录制时按60fps记录母带保存，",
        "ja_JP": "録画は60fpsのマスターとして保存され、",
        "en_US": "Recordings are saved at 60fps master,",
        "zh_TW": "插件錄製時按60fps記錄母帶保存，",
        "es_ES": "Las grabaciones se guardan a 60 fps maestro,",
        "fr_FR": "Les enregistrements sont enregistrés en 60fps master,",
        "ko_KR": "녹화는 60fps 마스터로 저장되며,",
        "ru_RU": "Запись сохраняется с качеством 60 FPS мастер-трека,",
        "it_IT": "Le registrazioni sono salvate con un master a 60 fps,"
    },
    "通过该选项转换帧率挂载到blender时间轴上。": {
        "zh_CN": "通过该选项转换帧率挂载到blender时间轴上。",
        "ja_JP": "この設定で変換して時間軸に適用されます。",
        "en_US": "converted to the selected FPS on apply.",
        "zh_TW": "通過該選項轉換幀率掛載到blender時間軸上。",
        "es_ES": "se convierte a los FPS seleccionados al aplicar.",
        "fr_FR": "converti au FPS sélectionné lors de l'application.",
        "ko_KR": "적용 시 선택한 FPS로 변환되어 타임라인에 등록됩니다.",
        "ru_RU": "преобразуется в выбранный FPS при применении на шкалу.",
        "it_IT": "convertite agli FPS selezionati durante l'applicazione."
    },
    "插件录制时按60fps记录母带保存，通过该选项转换帧率挂载到blender时间轴上。": {
        "zh_CN": "插件录制时按60fps记录母带保存，通过该选项转换帧率挂载到blender时间轴上。",
        "ja_JP": "録画は60fpsのマスターとして保存され、この設定で変換してタイムラインに適用されます。",
        "en_US": "Recordings are saved at 60fps master, and converted to the target FPS on apply.",
        "zh_TW": "插件錄製時按60fps記錄母帶保存，通過該選項轉換幀率掛載到blender時間軸上。",
        "es_ES": "Las grabaciones se guardan en 60 FPS maestro y se convierten a los FPS de destino al aplicar.",
        "fr_FR": "Les enregistrements sont en 60fps master et convertis au FPS cible lors de l'application.",
        "ko_KR": "녹화는 60fps 마스터로 저장되며, 적용 시 대상 FPS로 변환되어 타임라인에 등록됩니다.",
        "ru_RU": "Записи сохраняются в мастере 60 FPS и преобразуются в целевой FPS при переносе на таймлайн.",
        "it_IT": "Le registrazioni sono salvate in formato master a 60 fps e convertite agli FPS di destinazione al momento dell'applicazione sulla timeline."
    },
    "👤 显示人偶骨骼HUD": {
        "zh_CN": "👤 显示人偶骨骼HUD",
        "ja_JP": "👤 人形ボーンHUD画面を開く (Puppet HUD) ➔",
        "en_US": "👤 Toggle Puppet Canvas HUD ➔",
        "zh_TW": "👤 顯示人偶骨骼HUD",
        "es_ES": "👤 Mostrar HUD de Marioneta ➔",
        "fr_FR": "👤 Afficher HUD Marionnette ➔",
        "ko_KR": "👤 퍼펫 스켈레톤 HUD 표시 ➔",
        "ru_RU": "👤 Показать HUD марионетки ➔",
        "it_IT": "👤 Mostra HUD Scheletro Marionetta ➔"
    },
    "👤 隐藏人偶骨骼HUD": {
        "zh_CN": "👤 隐藏人偶骨骼HUD",
        "ja_JP": "👤 人形ボーンHUD画面を閉じる (Hide HUD)",
        "en_US": "👤 Close Puppet Canvas HUD",
        "zh_TW": "👤 隱藏人偶骨骼HUD",
        "es_ES": "👤 Ocultar HUD de Marioneta",
        "fr_FR": "👤 Masquer HUD Marionnette",
        "ko_KR": "👤 퍼펫 스켈레톤 HUD 숨기기",
        "ru_RU": "👤 Скрыть HUD марионетки",
        "it_IT": "👤 Nascondi HUD Scheletro Marionetta"
    },
    "👤 打开人偶骨骼映射画布 (Puppet View) ➔": {
        "zh_CN": "👤 打开人偶骨骼映射画布 (Puppet View) ➔",
        "ja_JP": "👤 人形ボーンマッピング画面を開く (Puppet View) ➔",
        "en_US": "👤 Open Puppet Bone Mapper ➔",
        "zh_TW": "👤 打開人偶骨骼映射畫布 (Puppet View) ➔",
        "es_ES": "👤 Abrir Mapeador de Huesos ➔",
        "fr_FR": "👤 Ouvrir le Mappeur de Marionnette ➔",
        "ko_KR": "👤 퍼펫 뼈 매핑 캔버스 열기 ➔",
        "ru_RU": "👤 Открыть карту марионетки ➔",
        "it_IT": "👤 Apri Mappatura Ossa Marionetta ➔"
    },
    "Rebocap 人偶画布 (Skeleton View)": {
        "zh_CN": "Rebocap 人偶画布 (Skeleton View)",
        "ja_JP": "Rebocap 人形キャンバス (Skeleton View)",
        "en_US": "Rebocap Skeleton View",
        "zh_TW": "Rebocap 人偶畫布 (Skeleton View)",
        "es_ES": "Rebocap Vista de Esqueleto",
        "fr_FR": "Vue du Squelette Rebocap",
        "ko_KR": "Rebocap 퍼펫 캔버스",
        "ru_RU": "Холст марионетки Rebocap",
        "it_IT": "Rebocap Vista Marionetta"
    },
    "FK 骨骼映射清单 (FK Definition):": {
        "zh_CN": "FK 骨骼映射清单 (FK Definition):",
        "ja_JP": "FKボーン定義リスト (FK Definition):",
        "en_US": "FK Bone Definition:",
        "zh_TW": "FK 骨骼映射清單 (FK Definition):",
        "es_ES": "Lista de Mapeo de Huesos FK:",
        "fr_FR": "Définition des Os FK :",
        "ko_KR": "FK 뼈 매핑 목록:",
        "ru_RU": "Список сопоставления FK костей:",
        "it_IT": "Elenco Mappatura Ossa FK:"
    },
    "四肢对称映射:": {
        "zh_CN": "四肢对称映射:",
        "ja_JP": "四肢対称マッピング:",
        "en_US": "Limbs Mapping:",
        "zh_TW": "四肢對稱映射:",
        "es_ES": "Mapeo Simétrico de Extremidades:",
        "fr_FR": "Mappage Symétrique des Membres :",
        "ko_KR": "사지 대칭 매핑:",
        "ru_RU": "Симметричное сопоставление конечностей:",
        "it_IT": "Mappatura Simmetrica degli Arti:"
    },
    "Left (左)": {
        "zh_CN": "Left (左)",
        "ja_JP": "Left (左)",
        "en_US": "Left",
        "zh_TW": "Left (左)",
        "es_ES": "Izquierda",
        "fr_FR": "Gauche",
        "ko_KR": "왼쪽 (Left)",
        "ru_RU": "Левая (Left)",
        "it_IT": "Sinistra (Left)"
    },
    "Right (右)": {
        "zh_CN": "Right (右)",
        "ja_JP": "Right (右)",
        "en_US": "Right",
        "zh_TW": "Right (右)",
        "es_ES": "Derecha",
        "fr_FR": "Droite",
        "ko_KR": "오른쪽 (Right)",
        "ru_RU": "Правая (Right)",
        "it_IT": "Destra (Right)"
    },
    "清空全部": {
        "zh_CN": "清空全部",
        "ja_JP": "すべてクリア",
        "en_US": "Clear All",
        "zh_TW": "清空全部",
        "es_ES": "Borrar Todo",
        "fr_FR": "Tout Effacer",
        "ko_KR": "모두 지우기",
        "ru_RU": "Очистить всё",
        "it_IT": "Cancella Tutto"
    },
    "片段名称": {
        "zh_CN": "片段名称",
        "ja_JP": "テイク名",
        "en_US": "Take Name",
        "zh_TW": "片段名稱",
        "es_ES": "Nombre de Toma",
        "fr_FR": "Nom de la Prise",
        "ko_KR": "테이크 이름",
        "ru_RU": "Имя дубля",
        "it_IT": "Nome Registrazione"
    },
    "类型": {
        "zh_CN": "类型",
        "ja_JP": "タイプ",
        "en_US": "Type",
        "zh_TW": "類型",
        "es_ES": "Tipo",
        "fr_FR": "Type",
        "ko_KR": "유형",
        "ru_RU": "Тип",
        "it_IT": "Tipo"
    },
    "总帧数": {
        "zh_CN": "总帧数",
        "ja_JP": "総フレーム数",
        "en_US": "Total Frames",
        "zh_TW": "總幀數",
        "es_ES": "Fotogramas Totales",
        "fr_FR": "Total Images",
        "ko_KR": "총 프레임",
        "ru_RU": "Всего кадров",
        "it_IT": "Fotogrammi Totali"
    },
    "自动匹配场景 (Auto Scene)": {
        "en_US": "Auto Match Scene (Auto Scene)",
        "zh_CN": "自动匹配场景 (Auto Scene)",
        "ja_JP": "シーン自動マッチ (Auto Scene)",
        "zh_TW": "自動匹配場景 (Auto Scene)",
        "es_ES": "Coincidencia Automática (Auto Scene)",
        "fr_FR": "Auto-adaptation Scène (Auto Scene)",
        "ko_KR": "자동 씬 일치 (Auto Scene)",
        "ru_RU": "Автосогласование сцены (Auto Scene)",
        "it_IT": "Adatta Automaticamente alla Scena (Auto Scene)"
    },
    "24 FPS (电影/标准动画 Film)": {
        "en_US": "24 FPS (Film/Animation)",
        "zh_CN": "24 FPS (电影/标准动画 Film)",
        "ja_JP": "24 FPS (映画/アニメ Film)",
        "zh_TW": "24 FPS (電影/標準動畫 Film)",
        "es_ES": "24 FPS (Cine/Animación)",
        "fr_FR": "24 FPS (Cinéma/Animation)",
        "ko_KR": "24 FPS (영화/애니메이션)",
        "ru_RU": "24 FPS (Кино/Анимация)",
        "it_IT": "24 FPS (Cinema/Animazione Film)"
    },
    "30 FPS (电视/短视频 TV/Video)": {
        "en_US": "30 FPS (TV/Video)",
        "zh_CN": "30 FPS (电视/短视频 TV/Video)",
        "ja_JP": "30 FPS (テレビ/動画 TV/Video)",
        "zh_TW": "30 FPS (電視/短視頻 TV/Video)",
        "es_ES": "30 FPS (TV/Video)",
        "fr_FR": "30 FPS (TV/Vidéo)",
        "ko_KR": "30 FPS (TV/동영상)",
        "ru_RU": "30 FPS (ТВ/Видео)",
        "it_IT": "30 FPS (TV/Video)"
    },
    "60 FPS (原生动捕/流畅游戏 60Hz)": {
        "en_US": "60 FPS (Native Mocap 60Hz)",
        "zh_CN": "60 FPS (原生动捕/流畅游戏 60Hz)",
        "ja_JP": "60 FPS (ネイティブ/ゲーム 60Hz)",
        "zh_TW": "60 FPS (原生動捕/流暢遊戲 60Hz)",
        "es_ES": "60 FPS (Mocap Nativo 60Hz)",
        "fr_FR": "60 FPS (Mocap Natif 60Hz)",
        "ko_KR": "60 FPS (네이티브 모캡 60Hz)",
        "ru_RU": "60 FPS (Нативный мокап 60Hz)",
        "it_IT": "60 FPS (Mocap Nativo/Gioco 60Hz)"
    },
    "自定义帧率 (Custom...)": {
        "en_US": "Custom FPS (Custom...)",
        "zh_CN": "自定义帧率 (Custom...)",
        "ja_JP": "カスタムFPS (Custom...)",
        "zh_TW": "自定義幀率 (Custom...)",
        "es_ES": "FPS Personalizado (Custom...)",
        "fr_FR": "FPS Personnalisé (Custom...)",
        "ko_KR": "사용자 지정 FPS (Custom...)",
        "ru_RU": "Пользовательский FPS (Custom...)",
        "it_IT": "FPS Personalizzato (Custom...)"
    },
    "自定义帧率 (Target FPS)": {
        "zh_CN": "自定义帧率 (Target FPS)",
        "ja_JP": "カスタムFPS (Target FPS)",
        "en_US": "Target FPS",
        "zh_TW": "自定義幀率 (Target FPS)",
        "es_ES": "FPS Objetivo",
        "fr_FR": "FPS Cible",
        "ko_KR": "목표 FPS",
        "ru_RU": "Целевой FPS",
        "it_IT": "FPS Obiettivo"
    },
    "场景帧率:": {
        "zh_CN": "场景帧率:",
        "ja_JP": "シーンFPS:",
        "en_US": "Scene FPS:",
        "zh_TW": "場景幀率:",
        "es_ES": "FPS de Escena:",
        "fr_FR": "FPS Scène :",
        "ko_KR": "씬 FPS:",
        "ru_RU": "FPS сцены:",
        "it_IT": "FPS Scena:"
    },
    "尺寸单位:": {
        "zh_CN": "尺寸单位:",
        "ja_JP": "単位スケール:",
        "en_US": "Unit Scale:",
        "zh_TW": "尺寸單位:",
        "es_ES": "Unidades:",
        "fr_FR": "Unité :",
        "ko_KR": "단위 비율:",
        "ru_RU": "Единицы измерения:",
        "it_IT": "Scala Unità:"
    },
    "确定要删除此动捕记录吗？": {
        "zh_CN": "确定要删除此动捕记录吗？",
        "ja_JP": "このキャプチャ記録を削除しますか？",
        "en_US": "Are you sure you want to delete this take?",
        "zh_TW": "確定要刪除此動捕記錄嗎？",
        "es_ES": "¿Seguro que desea eliminar esta toma?",
        "fr_FR": "Voulez-vous vraiment supprimer cette prise ?",
        "ko_KR": "이 캡처 기록을 삭제하시겠습니까?",
        "ru_RU": "Удалить эту запись дубля?",
        "it_IT": "Sei sicuro di voler eliminare questa registrazione?"
    },
    "此操作将永久删除相关动作数据。": {
        "zh_CN": "此操作将永久删除相关动作数据。",
        "ja_JP": "関連するアクションデータは完全に削除されます。",
        "en_US": "This will permanently remove the associated action data.",
        "zh_TW": "此操作將永久刪除相關動作數據。",
        "es_ES": "Esto eliminará permanentemente los datos de animación asociados.",
        "fr_FR": "Cette action supprimera définitivement les données d'action associées.",
        "ko_KR": "이 작업은 관련 모션 데이터를 영구적으로 삭제합니다.",
        "ru_RU": "Это действие навсегда удалит связанные данные анимации.",
        "it_IT": "Questa operazione eliminerà definitivamente i dati di animazione associati."
    },
    "动捕记录已删除": {
        "zh_CN": "动捕记录已删除",
        "ja_JP": "キャプチャ記録が削除されました",
        "en_US": "Take deleted",
        "zh_TW": "動捕記錄已刪除",
        "es_ES": "Toma eliminada",
        "fr_FR": "Prise supprimée",
        "ko_KR": "캡처 기록이 삭제되었습니다",
        "ru_RU": "Дубль удален",
        "it_IT": "Registrazione eliminata"
    },
    "Port": {
        "zh_CN": "端口",
        "ja_JP": "ポート",
        "zh_TW": "端口",
        "en_US": "Port",
        "es_ES": "Puerto",
        "fr_FR": "Port",
        "ko_KR": "포트",
        "ru_RU": "Порт",
        "it_IT": "Porta"
    },
    "Connect": {
        "zh_CN": "连接",
        "ja_JP": "接続",
        "zh_TW": "連接 (Connect)",
        "es_ES": "Conectar",
        "fr_FR": "Connecter",
        "ko_KR": "연결 (Connect)",
        "ru_RU": "Подключить",
        "en_US": "连接",
        "it_IT": "Connetti"
    },
    "Disconnect": {
        "zh_CN": "断开连接",
        "ja_JP": "切断",
        "zh_TW": "斷開連接",
        "es_ES": "Desconectar",
        "fr_FR": "Déconnecter",
        "ko_KR": "연결 끊기",
        "ru_RU": "Отключить",
        "en_US": "断开连接",
        "it_IT": "Disconnetti"
    },
    "Connected": {
        "zh_CN": "已连接",
        "ja_JP": "接続済み",
        "zh_TW": "已連接",
        "en_US": "Connected",
        "es_ES": "Conectado",
        "fr_FR": "Connecté",
        "ko_KR": "연결됨",
        "ru_RU": "Подключено",
        "it_IT": "Connesso"
    },
    "Pause Control": {
        "zh_CN": "暂停控制 (手动调整动作)",
        "ja_JP": "一時停止 (手動調整)",
        "zh_TW": "暫停控制 (手動調整動作)",
        "en_US": "Pause Control",
        "es_ES": "Pausar Control",
        "fr_FR": "Pause du Contrôle",
        "ko_KR": "제어 일시중지",
        "ru_RU": "Пауза управления",
        "it_IT": "Metti in Pausa Controllo"
    },
    "Restore Pose": {
        "zh_CN": "恢复原始姿态 (T-Pose)",
        "ja_JP": "元のポーズを復元 (T-Pose)",
        "zh_TW": "恢復原始姿態 (T-Pose)",
        "en_US": "Restore Pose (T-Pose)",
        "es_ES": "Restaurar Pose (T-Pose)",
        "fr_FR": "Restaurer la Pose (T-Pose)",
        "ko_KR": "기본 포즈 복원 (T-Pose)",
        "ru_RU": "Восстановить позу (T-Pose)",
        "it_IT": "Ripristina Posa (T-Pose)"
    },
    "Start Record": {
        "zh_CN": "开始录制",
        "ja_JP": "録画開始",
        "zh_TW": "開始錄製",
        "es_ES": "Iniciar Grabación",
        "fr_FR": "Démarrer lEnregistrement",
        "ko_KR": "녹화 시작",
        "ru_RU": "Начать запись",
        "en_US": "开始录制",
        "it_IT": "Avvia Registrazione"
    },
    "Stop Record": {
        "zh_CN": "停止录制",
        "ja_JP": "録画停止",
        "zh_TW": "停止錄製",
        "es_ES": "Detener Grabación",
        "fr_FR": "Arrêter lEnregistrement",
        "ko_KR": "녹화 중지",
        "ru_RU": "Остановить запись",
        "en_US": "停止录制",
        "it_IT": "Ferma Registrazione"
    },
    "Enable Debug Logs": {
        "zh_CN": "开启系统调试日志",
        "ja_JP": "システムデバッグログを有効化",
        "zh_TW": "開啟系統調試日誌",
        "en_US": "Enable Debug Logs",
        "es_ES": "Habilitar Registros de Depuración",
        "fr_FR": "Activer les Journaux de Débogage",
        "ko_KR": "디버그 로그 활성화",
        "ru_RU": "Включить журналы отладки",
        "it_IT": "Abilita Log di Debug"
    },
    "Save Bone": {
        "zh_CN": "导出骨架文件",
        "ja_JP": "スケルトンファイルをエクスポート",
        "zh_TW": "導出骨架文件",
        "en_US": "Export Skeleton File",
        "es_ES": "Exportar Archivo de Esqueleto",
        "fr_FR": "Exporter le Fichier Squelette",
        "ko_KR": "골격 파일 내보내기",
        "ru_RU": "Экспорт файла скелета",
        "it_IT": "Esporta File Scheletro"
    },
    "Export Skeleton File": {
        "zh_CN": "导出骨架文件",
        "ja_JP": "スケルトンファイルをエクスポート",
        "zh_TW": "導出骨架文件",
        "en_US": "Export Skeleton File",
        "es_ES": "Exportar Archivo de Esqueleto",
        "fr_FR": "Exporter le Fichier Squelette",
        "ko_KR": "골격 파일 내보내기",
        "ru_RU": "Экспорт файла скелета",
        "it_IT": "Esporta File Scheletro"
    },
    "Please bind Pelvis and Legs first": {
        "zh_CN": "* 请先绑定 Pelvis(骨盆) 和双腿骨骼",
        "ja_JP": "* 最初に Pelvis (骨盤) と脚をバインドしてください",
        "zh_TW": "* 請先綁定 Pelvis(骨盆) 和雙腿骨骼",
        "en_US": "* Please bind Pelvis and Legs first",
        "es_ES": "* Primero vincule la pelvis y las piernas",
        "fr_FR": "* Veuillez d'abord lier le bassin et les jambes",
        "ko_KR": "* 먼저 골반과 다리 뼈를 바인딩하세요",
        "ru_RU": "* Сначала привяжите таз и кости ног",
        "it_IT": "* Associa prima il bacino e le ossa delle gambe"
    },
    "Foot Contact Positions": {
        "zh_CN": "足底接触点配置",
        "ja_JP": "足の接地ポイント設定",
        "zh_TW": "足底接觸點配置",
        "en_US": "Foot Contact Positions",
        "es_ES": "Posiciones de Contacto del Pie",
        "fr_FR": "Points de Contact des Pieds",
        "ko_KR": "발 접촉 지점 설정",
        "ru_RU": "Точки контакта стопы",
        "it_IT": "Posizioni di Contatto del Piede"
    },
    "Place All 6 Contact Points": {
        "zh_CN": "放置全部 6 个接触点",
        "ja_JP": "6つの接触点をすべて配置",
        "zh_TW": "放置全部 6 個接觸點",
        "en_US": "Place All 6 Contact Points",
        "es_ES": "Colocar los 6 Puntos de Contacto",
        "fr_FR": "Placer les 6 Points de Contact",
        "ko_KR": "6개 접촉점 모두 배치",
        "ru_RU": "Разместить все 6 точек контакта",
        "it_IT": "Posiziona Tutti i 6 Punti di Contatto"
    },
    "Left": {
        "zh_CN": "左脚",
        "ja_JP": "左足",
        "zh_TW": "左腳",
        "en_US": "Left Foot",
        "es_ES": "Pie Izquierdo",
        "fr_FR": "Pied Gauche",
        "ko_KR": "왼발",
        "ru_RU": "Левая стопа",
        "it_IT": "Piede Sinistro"
    },
    "Right": {
        "zh_CN": "右脚",
        "ja_JP": "右足",
        "zh_TW": "右腳",
        "en_US": "Right Foot",
        "es_ES": "Pie Derecho",
        "fr_FR": "Pied Droit",
        "ko_KR": "오른발",
        "ru_RU": "Правая стопа",
        "it_IT": "Piede Destro"
    },
    "Right (Control)": {
        "zh_CN": "右脚 (主控)",
        "ja_JP": "右足 (コントロール)",
        "zh_TW": "右腳 (主控)",
        "en_US": "Right Foot (Master)",
        "es_ES": "Pie Derecho (Control)",
        "fr_FR": "Pied Droit (Maître)",
        "ko_KR": "오른발 (메인)",
        "ru_RU": "Правая стопа (мастер)",
        "it_IT": "Piede Destro (Principale)"
    },
    "Left (Mirrored)": {
        "zh_CN": "左脚 (自动镜像)",
        "ja_JP": "左足 (ミラー)",
        "zh_TW": "左腳 (自動鏡像)",
        "en_US": "Left Foot (Mirrored)",
        "es_ES": "Pie Izquierdo (Espejado)",
        "fr_FR": "Pied Gauche (Miroir)",
        "ko_KR": "왼발 (자동 미러)",
        "ru_RU": "Левая стопа (зеркально)",
        "it_IT": "Piede Sinistro (Specchiato)"
    },
    "Set Point": {
        "zh_CN": "放置节点",
        "ja_JP": "ポイントを配置",
        "zh_TW": "放置節點",
        "en_US": "Set Point",
        "es_ES": "Colocar Punto",
        "fr_FR": "Définir le Point",
        "ko_KR": "포인트 배치",
        "ru_RU": "Установить точку",
        "it_IT": "Imposta Punto"
    },
    "Auto Mirrored": {
        "zh_CN": "已自动镜像",
        "ja_JP": "自動ミラー済み",
        "zh_TW": "已自動鏡像",
        "en_US": "Auto Mirrored",
        "es_ES": "Espejado Automático",
        "fr_FR": "Miroir Automatique",
        "ko_KR": "자동 미러링됨",
        "ru_RU": "Зеркально",
        "it_IT": "Specchiato Automaticamente"
    },
    "Drive Type": {
        "zh_CN": "驱动模式",
        "ja_JP": "駆動モード",
        "zh_TW": "驅動模式",
        "en_US": "Drive Type",
        "es_ES": "Tipo de Control",
        "fr_FR": "Type de Commande",
        "ko_KR": "구동 모드",
        "ru_RU": "Тип привода",
        "it_IT": "Tipo di Guida"
    },
    "Source": {
        "zh_CN": "源骨架",
        "ja_JP": "ソース骨格",
        "zh_TW": "源骨架",
        "en_US": "Source Armature",
        "es_ES": "Esqueleto Origen",
        "fr_FR": "Armature Source",
        "ko_KR": "소스 골격",
        "ru_RU": "Исходный скелет",
        "it_IT": "Armatura Sorgente"
    },
    "Auto Detect Config Path": {
        "zh_CN": "自动检测配置文件路径",
        "ja_JP": "設定ファイルパスを自動検出",
        "zh_TW": "自動檢測配置文件路徑",
        "en_US": "Auto Detect Config Path",
        "es_ES": "Autodetectar Ruta de Configuración",
        "fr_FR": "Détecter Auto Chemin Config",
        "ko_KR": "설정 경로 자동 감지",
        "ru_RU": "Автопоиск пути к конфигурации",
        "it_IT": "Rileva Automaticamente Percorso Config"
    },
    "Auto Detect": {
        "zh_CN": "自动检测骨骼名称",
        "ja_JP": "ボーン名を自動検出",
        "zh_TW": "自動檢測骨骼名稱",
        "en_US": "Auto Detect",
        "es_ES": "Detección Automática",
        "fr_FR": "Détection Automatique",
        "ko_KR": "뼈 자동 감지",
        "ru_RU": "Автоопределение",
        "it_IT": "Rilevamento Automatico"
    },
    "Supports Mixamo & VRM naming rules": {
        "zh_CN": "支持 Mixamo 和 VRM 命名规则",
        "ja_JP": "Mixamo および VRM の命名規則をサポート",
        "zh_TW": "支持 Mixamo 和 VRM 命名規則",
        "en_US": "Supports Mixamo & VRM naming rules",
        "es_ES": "Compatible con Mixamo y VRM",
        "fr_FR": "Supporte Mixamo et VRM",
        "ko_KR": "Mixamo 및 VRM 명명 규칙 지원",
        "ru_RU": "Поддержка правил именования Mixamo и VRM",
        "it_IT": "Supporta regole di denominazione Mixamo e VRM"
    },
    "Setup Character Bones": {
        "zh_CN": "一键配置角色骨骼绑定",
        "ja_JP": "キャラクターボーンを自動設定",
        "zh_TW": "一鍵配置角色骨骼綁定",
        "en_US": "Setup Character Bones",
        "es_ES": "Configurar Huesos del Personaje",
        "fr_FR": "Configurer les Os du Personnage",
        "ko_KR": "캐릭터 뼈 원클릭 설정",
        "ru_RU": "Настройка костей персонажа",
        "it_IT": "Configura Ossa del Personaggio"
    },
    "Import JSON": {
        "zh_CN": "📥 导入配置 JSON",
        "ja_JP": "📥 JSON インポート",
        "zh_TW": "📥 導入配置 JSON",
        "en_US": "📥 Import Config JSON",
        "es_ES": "📥 Importar JSON",
        "fr_FR": "📥 Importer JSON",
        "ko_KR": "📥 설정 JSON 가져오기",
        "ru_RU": "📥 Импорт JSON",
        "it_IT": "📥 Importa Configurazione JSON"
    },
    "Export JSON": {
        "zh_CN": "📤 导出配置 JSON",
        "ja_JP": "📤 JSON エクスポート",
        "zh_TW": "📤 導出配置 JSON",
        "en_US": "📤 Export Config JSON",
        "es_ES": "📤 Exportar JSON",
        "fr_FR": "📤 Exporter JSON",
        "ko_KR": "📤 설정 JSON 내보내기",
        "ru_RU": "📤 Экспорт JSON",
        "it_IT": "📤 Esporta Configurazione JSON"
    },
    "View Supported Formats": {
        "zh_CN": "查看支持的预设格式",
        "ja_JP": "サポートされているフォーマットを表示",
        "zh_TW": "查看支持的預設格式",
        "en_US": "View Supported Formats",
        "es_ES": "Ver Formatos Compatibles",
        "fr_FR": "Voir Formats Supportés",
        "ko_KR": "지원되는 포맷 보기",
        "ru_RU": "Поддерживаемые форматы",
        "it_IT": "Mostra Formati Supportati"
    },
    "Hide Supported Formats": {
        "zh_CN": "收起支持的预设格式",
        "ja_JP": "サポートされているフォーマットを隠す",
        "zh_TW": "收起支持的預設格式",
        "en_US": "Hide Supported Formats",
        "es_ES": "Ocultar Formatos Compatibles",
        "fr_FR": "Masquer Formats Supportés",
        "ko_KR": "지원되는 포맷 숨기기",
        "ru_RU": "Скрыть форматы",
        "it_IT": "Nascondi Formati Supportati"
    },
    "✅ Mixamo (with/without prefix)": {
        "zh_CN": "✅ Mixamo (带/不带前缀)",
        "ja_JP": "✅ Mixamo (プレフィックスあり/なし)",
        "zh_TW": "✅ Mixamo (帶/不帶前綴)",
        "en_US": "✅ Mixamo (with/without prefix)",
        "es_ES": "✅ Mixamo (con/sin prefijo)",
        "fr_FR": "✅ Mixamo (avec/sans préfixe)",
        "ko_KR": "✅ Mixamo (접두사 유/무)",
        "ru_RU": "✅ Mixamo (с префиксом/без)",
        "it_IT": "✅ Mixamo (con/senza prefisso)"
    },
    "Generate Nodes": {
        "zh_CN": "生成骨架追踪点",
        "ja_JP": "トラッキングポイントを生成",
        "zh_TW": "生成骨架追蹤點",
        "en_US": "Generate Tracking Nodes",
        "es_ES": "Generar Nodos de Rastreo",
        "fr_FR": "Générer Nœuds de Suivi",
        "ko_KR": "트래킹 노드 생성",
        "ru_RU": "Создать точки трекинга",
        "it_IT": "Genera Nodi di Tracciamento"
    },
    "Node Size (mm)": {
        "zh_CN": "追踪点大小 (mm)",
        "ja_JP": "トラッキングポイントサイズ (mm)",
        "zh_TW": "追蹤點大小 (mm)",
        "en_US": "Node Size (mm)",
        "es_ES": "Tamaño del Nodo (mm)",
        "fr_FR": "Taille du Nœud (mm)",
        "ko_KR": "노드 크기 (mm)",
        "ru_RU": "Размер узла (мм)",
        "it_IT": "Dimensione Nodo (mm)"
    },
    "Cancel Usage": {
        "zh_CN": "取消使用角色",
        "ja_JP": "キャラクターの使用をキャンセル",
        "zh_TW": "取消使用角色",
        "en_US": "Cancel Character Usage",
        "es_ES": "Cancelar Uso de Personaje",
        "fr_FR": "Annuler l'Utilisation",
        "ko_KR": "캐릭터 사용 취소",
        "ru_RU": "Отменить использование персонажа",
        "it_IT": "Annulla Uso Personaggio"
    },
    "Use Rebocap Character": {
        "zh_CN": "使用 Rebocap 角色",
        "ja_JP": "Rebocap キャラクターを使用",
        "zh_TW": "使用 Rebocap 角色",
        "en_US": "Use Rebocap Character",
        "es_ES": "Usar Personaje Rebocap",
        "fr_FR": "Utiliser Personnage Rebocap",
        "ko_KR": "Rebocap 캐릭터 사용",
        "ru_RU": "Использовать персонажа Rebocap",
        "it_IT": "Usa Personaggio Rebocap"
    },
    "Config Path": {
        "zh_CN": "上位软件配置路径 (Config Path)",
        "ja_JP": "ホストソフトウェア設定パス (Config Path)",
        "zh_TW": "上位軟件配置路徑 (Config Path)",
        "en_US": "Config Path",
        "es_ES": "Ruta de Configuración",
        "fr_FR": "Chemin de Config",
        "ko_KR": "설정 경로 (Config Path)",
        "ru_RU": "Путь конфигурации (Config Path)",
        "it_IT": "Percorso Configurazione"
    },
    "Read Data": {
        "zh_CN": "读取骨骼长度",
        "ja_JP": "ボーンの長さを読み込む",
        "zh_TW": "讀取骨骼長度",
        "en_US": "Read Bone Lengths",
        "es_ES": "Leer Longitud de Huesos",
        "fr_FR": "Lire Longueur des Os",
        "ko_KR": "뼈 길이 읽기",
        "ru_RU": "Считать длины костей",
        "it_IT": "Leggi Dati"
    },
    "Auto Refresh": {
        "zh_CN": "自动刷新",
        "ja_JP": "自動更新",
        "zh_TW": "自動刷新",
        "en_US": "Auto Refresh",
        "es_ES": "Actualización Automática",
        "fr_FR": "Actualisation Auto",
        "ko_KR": "자동 새로고침",
        "ru_RU": "Автообновление",
        "it_IT": "Aggiornamento Automatico"
    },
    "Current Bone Lengths": {
        "zh_CN": "当前骨骼长度",
        "ja_JP": "現在のボーンの長さ",
        "zh_TW": "當前骨骼長度",
        "en_US": "Current Bone Lengths",
        "es_ES": "Longitudes Actuales de Huesos",
        "fr_FR": "Longueurs d'Os Actuelles",
        "ko_KR": "현재 뼈 길이",
        "ru_RU": "Текущие длины костей",
        "it_IT": "Lunghezze Ossa Attuali"
    },
    "Neck & Head": {
        "zh_CN": "头颈 (Neck & Head)",
        "ja_JP": "頭と首 (Neck & Head)",
        "zh_TW": "頭頸 (Neck & Head)",
        "en_US": "Neck & Head",
        "es_ES": "Cuello y Cabeza",
        "fr_FR": "Cou et Tête",
        "ko_KR": "목과 머리",
        "ru_RU": "Шея и голова",
        "it_IT": "Collo e Testa"
    },
    "Chest": {
        "zh_CN": "胸腔 (Chest)",
        "ja_JP": "胸 (Chest)",
        "zh_TW": "胸腔 (Chest)",
        "en_US": "Chest",
        "es_ES": "Pecho",
        "fr_FR": "Poitrine",
        "ko_KR": "가슴 (Chest)",
        "ru_RU": "Грудь (Chest)",
        "it_IT": "Petto"
    },
    "Spine": {
        "zh_CN": "脊椎 (Spine)",
        "ja_JP": "脊椎 (Spine)",
        "zh_TW": "脊椎 (Spine)",
        "en_US": "Spine",
        "es_ES": "Columna",
        "fr_FR": "Colonne",
        "ko_KR": "척추 (Spine)",
        "ru_RU": "Позвоночник (Spine)",
        "it_IT": "Spina Dorsale"
    },
    "Shoulder Width": {
        "zh_CN": "肩宽 (Shoulder Width)",
        "ja_JP": "肩幅 (Shoulder Width)",
        "zh_TW": "肩寬 (Shoulder Width)",
        "en_US": "Shoulder Width",
        "es_ES": "Ancho de Hombros",
        "fr_FR": "Largeur d'Épaules",
        "ko_KR": "어깨 너비",
        "ru_RU": "Ширина плеч",
        "it_IT": "Larghezza Spalle"
    },
    "Upper Arm": {
        "zh_CN": "大臂 (Upper Arm)",
        "ja_JP": "上腕 (Upper Arm)",
        "zh_TW": "大臂 (Upper Arm)",
        "en_US": "Upper Arm",
        "es_ES": "Brazo Superior",
        "fr_FR": "Bras Supérieur",
        "ko_KR": "상완 (Upper Arm)",
        "ru_RU": "Плечо (Upper Arm)",
        "it_IT": "Braccio Superiore"
    },
    "Lower Arm": {
        "zh_CN": "小臂 (Lower Arm)",
        "ja_JP": "前腕 (Lower Arm)",
        "zh_TW": "小臂 (Lower Arm)",
        "en_US": "Lower Arm",
        "es_ES": "Antebrazo",
        "fr_FR": "Avant-bras",
        "ko_KR": "전완 (Lower Arm)",
        "ru_RU": "Предплечье (Lower Arm)",
        "it_IT": "Avambraccio"
    },
    "Hip Width": {
        "zh_CN": "胯宽 (Hip Width)",
        "ja_JP": "股幅 (Hip Width)",
        "zh_TW": "胯寬 (Hip Width)",
        "en_US": "Hip Width",
        "es_ES": "Ancho de Cadera",
        "fr_FR": "Largeur de Hanches",
        "ko_KR": "골반 너비",
        "ru_RU": "Ширина бедер",
        "it_IT": "Larghezza Fianchi"
    },
    "Hip Height": {
        "zh_CN": "跨高 (Hip Height)",
        "ja_JP": "股の高さ (Hip Height)",
        "zh_TW": "跨高 (Hip Height)",
        "en_US": "Hip Height",
        "es_ES": "Altura de Cadera",
        "fr_FR": "Hauteur de Hanches",
        "ko_KR": "골반 높이",
        "ru_RU": "Высота бедер",
        "it_IT": "Altezza Fianchi"
    },
    "Upper Leg": {
        "zh_CN": "大腿 (Upper Leg)",
        "ja_JP": "大腿 (Upper Leg)",
        "zh_TW": "大腿 (Upper Leg)",
        "en_US": "Upper Leg",
        "es_ES": "Muslo",
        "fr_FR": "Cuisse",
        "ko_KR": "허벅지 (Upper Leg)",
        "ru_RU": "Бедро (Upper Leg)",
        "it_IT": "Coscia"
    },
    "Lower Leg": {
        "zh_CN": "小腿 (Lower Leg)",
        "ja_JP": "下腿 (Lower Leg)",
        "zh_TW": "小腿 (Lower Leg)",
        "en_US": "Lower Leg",
        "es_ES": "Pierna Inferior",
        "fr_FR": "Jambe Inférieure",
        "ko_KR": "종아리 (Lower Leg)",
        "ru_RU": "Голень (Lower Leg)",
        "it_IT": "Gamba Inferiore"
    },
    "Foot": {
        "zh_CN": "脚掌 (Foot)",
        "ja_JP": "足 (Foot)",
        "zh_TW": "腳掌 (Foot)",
        "en_US": "Foot",
        "es_ES": "Pie",
        "fr_FR": "Pied",
        "ko_KR": "발 (Foot)",
        "ru_RU": "Стопа (Foot)",
        "it_IT": "Piede"
    },
    "History & Takes": {
        "zh_CN": "录制历史与回放 (History & Takes)",
        "ja_JP": "録画履歴と再生 (History & Takes)",
        "zh_TW": "錄製歷史與回放 (History & Takes)",
        "en_US": "History & Takes",
        "es_ES": "Historial y Tomas",
        "fr_FR": "Historique et Prises",
        "ko_KR": "녹화 기록 및 테이크",
        "ru_RU": "История и дубли",
        "it_IT": "Cronologia e Registrazioni"
    },
    "Apply Take": {
        "zh_CN": "挂载到时间轴 (Apply Take)",
        "ja_JP": "タイムラインに適用 (Apply Take)",
        "zh_TW": "掛載到時間軸 (Apply Take)",
        "en_US": "Apply Take",
        "es_ES": "Aplicar a Línea de Tiempo",
        "fr_FR": "Appliquer à la Chronologie",
        "ko_KR": "타임라인에 적용",
        "ru_RU": "Применить к шкале",
        "it_IT": "Applica alla Timeline (Apply Take)"
    },
    "Delete Take": {
        "zh_CN": "删除记录 (Delete Take)",
        "ja_JP": "記録削除 (Delete Take)",
        "zh_TW": "刪除記錄 (Delete Take)",
        "en_US": "Delete Take",
        "es_ES": "Eliminar Toma",
        "fr_FR": "Supprimer la Prise",
        "ko_KR": "테이크 삭제",
        "ru_RU": "Удалить дубль",
        "it_IT": "Elimina Registrazione (Delete Take)"
    },
    "Scene FPS:": {
        "zh_CN": "场景帧率 (Scene FPS):",
        "en_US": "场景帧率 (Scene FPS):",
        "zh_TW": "场景帧率 (Scene FPS):",
        "ja_JP": "场景帧率 (Scene FPS):",
        "es_ES": "场景帧率 (Scene FPS):",
        "fr_FR": "场景帧率 (Scene FPS):",
        "ko_KR": "场景帧率 (Scene FPS):",
        "ru_RU": "场景帧率 (Scene FPS):",
        "it_IT": "FPS Scena:"
    },
    "Apply / Export FPS Settings:": {
        "zh_CN": "挂载 / 导出帧率设置:",
        "en_US": "挂载 / 导出帧率设置:",
        "zh_TW": "挂载 / 导出帧率设置:",
        "ja_JP": "挂载 / 导出帧率设置:",
        "es_ES": "挂载 / 导出帧率设置:",
        "fr_FR": "挂载 / 导出帧率设置:",
        "ko_KR": "挂载 / 导出帧率设置:",
        "ru_RU": "挂载 / 导出帧率设置:",
        "it_IT": "Impostazioni FPS di Applicazione / Esportazione:"
    },
    "Apply FPS Mode": {
        "zh_CN": "应用帧率模式",
        "zh_TW": "應用幀率模式",
        "en_US": "Apply FPS Mode",
        "ja_JP": "適用FPSモード",
        "es_ES": "Modo FPS de Aplicación",
        "fr_FR": "Mode FPS d'Application",
        "ko_KR": "적용 FPS 모드",
        "ru_RU": "Режим FPS применения",
        "it_IT": "Modalità FPS di Applicazione"
    },
    "Auto (Scene)": {
        "zh_CN": "自动 (场景帧率)",
        "zh_TW": "自動 (場景幀率)",
        "en_US": "Auto (Scene FPS)",
        "ja_JP": "自動 (シーンFPS)",
        "es_ES": "Auto (FPS de Escena)",
        "fr_FR": "Auto (FPS Scène)",
        "ko_KR": "자동 (씬 FPS)",
        "ru_RU": "Авто (FPS сцены)",
        "it_IT": "Auto (Scena)"
    },
    "Custom": {
        "zh_CN": "自定义",
        "zh_TW": "自定義",
        "en_US": "Custom",
        "ja_JP": "カスタム",
        "es_ES": "Personalizado",
        "fr_FR": "Personnalisé",
        "ko_KR": "사용자 지정",
        "ru_RU": "Пользовательский",
        "it_IT": "Personalizzato"
    },
    "Target FPS": {
        "zh_CN": "目标帧率",
        "zh_TW": "目標幀率",
        "en_US": "Target FPS",
        "ja_JP": "ターゲットFPS",
        "es_ES": "FPS Objetivo",
        "fr_FR": "FPS Cible",
        "ko_KR": "목표 FPS",
        "ru_RU": "Целевой FPS",
        "it_IT": "FPS Obiettivo"
    },
    "A2T Pose Calibration (A-Pose to T-Pose)": {
        "zh_CN": "A2T 姿态校准 (A-Pose 转 T-Pose)",
        "ja_JP": "A2T ポーズキャリブレーション (A-Pose to T-Pose)",
        "zh_TW": "A2T 姿態校準 (A-Pose 轉 T-Pose)",
        "en_US": "A2T Pose Calibration (A-Pose to T-Pose)",
        "es_ES": "Calibración de Pose A2T (A-Pose a T-Pose)",
        "fr_FR": "Étalonnage de Pose A2T (A-Pose en T-Pose)",
        "ko_KR": "A2T 포즈 캘리브레이션 (A-Pose to T-Pose)",
        "ru_RU": "Калибровка позы A2T (A-Pose в T-Pose)",
        "it_IT": "Calibrazione Posa A2T (Posa A a Posa T)"
    },
    "Enable A2T Calibration": {
        "zh_CN": "启用 A2T 姿态校准",
        "ja_JP": "A2T キャリブレーションを有効化",
        "zh_TW": "啟用 A2T 姿態校準",
        "en_US": "Enable A2T Calibration",
        "es_ES": "Habilitar Calibración A2T",
        "fr_FR": "Activer l'Étalonnage A2T",
        "ko_KR": "A2T 캘리브레이션 활성화",
        "ru_RU": "Включить калибровку A2T",
        "it_IT": "Abilita Calibrazione A2T"
    },
    "* A2T Disabled (Direct Mocap Mapping)": {
        "zh_CN": "* A2T 已停用 (直连动捕映射)",
        "ja_JP": "* A2T 無効 (直接マッピング)",
        "zh_TW": "* A2T 已停用 (直連動捕映射)",
        "en_US": "* A2T Disabled (Direct Mocap Mapping)",
        "es_ES": "* A2T Deshabilitado (Mapeo Directo)",
        "fr_FR": "* A2T Désactivé (Mappage Direct)",
        "ko_KR": "* A2T 비활성화 (직접 매핑)",
        "ru_RU": "* A2T отключен (прямой мокап)",
        "it_IT": "* A2T Disabilitato (Mappatura Diretta Mocap)"
    },
    "Preset Template:": {
        "zh_CN": "预设模板:",
        "ja_JP": "プリセットテンプレート:",
        "zh_TW": "預設模板:",
        "en_US": "Preset Template:",
        "es_ES": "Plantilla Preestablecida:",
        "fr_FR": "Modèle Prédéfini :",
        "ko_KR": "프리셋 템플릿:",
        "ru_RU": "Предустановленный шаблон:",
        "it_IT": "Modello Predefinito:"
    },
    "Preview in Viewport": {
        "zh_CN": "👁️ 实时视口预览",
        "ja_JP": "👁️ ビューポートプレビュー",
        "zh_TW": "👁️ 實時視口預覽",
        "en_US": "👁️ Viewport Preview",
        "es_ES": "👁️ Vista Previa en Visor",
        "fr_FR": "👁️ Aperçu Vue 3D",
        "ko_KR": "👁️ 뷰포트 미리보기",
        "ru_RU": "👁️ Предпросмотр во вьюпорте",
        "it_IT": "👁️ Anteprima nella Vista 3D"
    },
    "Reset Offsets": {
        "zh_CN": "重置所有偏移",
        "ja_JP": "オフセットをリセット",
        "zh_TW": "重置所有偏移",
        "en_US": "Reset All Offsets",
        "es_ES": "Restablecer Desplazamientos",
        "fr_FR": "Réinitialiser Décalages",
        "ko_KR": "오프셋 초기화",
        "ru_RU": "Сбросить все смещения",
        "it_IT": "Reimposta Tutti gli Offset"
    },
    "Symmetrical Edit (Mirror Left -> Right)": {
        "zh_CN": "对称镜像编辑 (左侧同步右侧)",
        "ja_JP": "対称ミラー編集 (左から右へ)",
        "zh_TW": "對稱鏡像編輯 (左側同步右側)",
        "en_US": "Symmetrical Edit (Mirror Left -> Right)",
        "es_ES": "Edición Simétrica (Espejo Izq -> Der)",
        "fr_FR": "Édition Symétrique (Miroir G -> D)",
        "ko_KR": "대칭 미러 편집 (좌 -> 우)",
        "ru_RU": "Симметричное ред. (зеркало Л -> П)",
        "it_IT": "Modifica Simmetrica (Specchia Sinistra -> Destra)"
    },
    "1. Left Arm": {
        "zh_CN": "1. 左上肢 (Left Arm)",
        "ja_JP": "1. 左腕 (Left Arm)",
        "zh_TW": "1. 左上肢 (Left Arm)",
        "en_US": "1. Left Arm",
        "es_ES": "1. Brazo Izquierdo",
        "fr_FR": "1. Bras Gauche",
        "ko_KR": "1. 왼팔 (Left Arm)",
        "ru_RU": "1. Левая рука (Left Arm)",
        "it_IT": "1. Braccio Sinistro (Left Arm)"
    },
    "2. Right Arm": {
        "zh_CN": "2. 右上肢 (Right Arm)",
        "ja_JP": "2. 右腕 (Right Arm)",
        "zh_TW": "2. 右上肢 (Right Arm)",
        "en_US": "2. Right Arm",
        "es_ES": "2. Brazo Derecho",
        "fr_FR": "2. Bras Droit",
        "ko_KR": "2. 오른팔 (Right Arm)",
        "ru_RU": "2. Правая рука (Right Arm)",
        "it_IT": "2. Braccio Destro (Right Arm)"
    },
    "(Mirrored)": {
        "zh_CN": "(镜像联动中)",
        "ja_JP": "(ミラー連動中)",
        "zh_TW": "(鏡像聯動中)",
        "en_US": "(Mirrored)",
        "es_ES": "(Espejado)",
        "fr_FR": "(Miroir actif)",
        "ko_KR": "(미러링 연동)",
        "ru_RU": "(зеркально)",
        "it_IT": "(Specchiato)"
    },
    "3. Left Leg": {
        "zh_CN": "3. 左下肢 (Left Leg)",
        "ja_JP": "3. 左脚 (Left Leg)",
        "zh_TW": "3. 左下肢 (Left Leg)",
        "en_US": "3. Left Leg",
        "es_ES": "3. Pierna Izquierda",
        "fr_FR": "3. Jambe Gauche",
        "ko_KR": "3. 왼다리 (Left Leg)",
        "ru_RU": "3. Левая нога (Left Leg)",
        "it_IT": "3. Gamba Sinistra (Left Leg)"
    },
    "4. Right Leg": {
        "zh_CN": "4. 右下肢 (Right Leg)",
        "ja_JP": "4. 右脚 (Right Leg)",
        "zh_TW": "4. 右下肢 (Right Leg)",
        "en_US": "4. Right Leg",
        "es_ES": "4. Pierna Derecha",
        "fr_FR": "4. Jambe Droite",
        "ko_KR": "4. 오른다리 (Right Leg)",
        "ru_RU": "4. Правая нога (Right Leg)",
        "it_IT": "4. Gamba Destra (Right Leg)"
    },
    "5. Root & Spine & Head": {
        "zh_CN": "5. 躯干与头部 (Root & Spine & Head)",
        "ja_JP": "5. 体幹と頭部 (Root & Spine & Head)",
        "zh_TW": "5. 軀幹與頭部 (Root & Spine & Head)",
        "en_US": "5. Root & Spine & Head",
        "es_ES": "5. Torso y Cabeza",
        "fr_FR": "5. Buste et Tête",
        "ko_KR": "5. 몸통 및 머리",
        "ru_RU": "5. Торс и голова",
        "it_IT": "5. Busto e Testa (Root & Spine & Head)"
    },
    "Left Clavicle (Collar)": {
        "zh_CN": "左锁骨 (Clavicle / Collar)",
        "ja_JP": "左鎖骨 (Clavicle / Collar)",
        "zh_TW": "左鎖骨 (Clavicle / Collar)",
        "en_US": "Left Clavicle (Collar)",
        "es_ES": "Clavícula Izquierda",
        "fr_FR": "Clavicule Gauche",
        "ko_KR": "왼쪽 쇄골",
        "ru_RU": "Левая ключица",
        "it_IT": "Clavicola Sinistra"
    },
    "Left UpperArm (Shoulder)": {
        "zh_CN": "左大臂 (UpperArm / Shoulder)",
        "ja_JP": "左上腕 (UpperArm / Shoulder)",
        "zh_TW": "左大臂 (UpperArm / Shoulder)",
        "en_US": "Left UpperArm (Shoulder)",
        "es_ES": "Brazo Sup. Izquierdo",
        "fr_FR": "Bras Sup. Gauche",
        "ko_KR": "왼쪽 상완",
        "ru_RU": "Левое плечо",
        "it_IT": "Braccio Superiore Sinistro (Spalla)"
    },
    "Left LowerArm (Elbow)": {
        "zh_CN": "左小臂 (LowerArm / Elbow)",
        "ja_JP": "左前腕 (LowerArm / Elbow)",
        "zh_TW": "左小臂 (LowerArm / Elbow)",
        "en_US": "Left LowerArm (Elbow)",
        "es_ES": "Antebrazo Izquierdo",
        "fr_FR": "Avant-bras Gauche",
        "ko_KR": "왼쪽 전완",
        "ru_RU": "Левое предплечье",
        "it_IT": "Avambraccio Sinistro (Gomito)"
    },
    "Left Hand (Wrist)": {
        "zh_CN": "左手/手腕 (Hand / Wrist)",
        "ja_JP": "左手/手首 (Hand / Wrist)",
        "zh_TW": "左手/手腕 (Hand / Wrist)",
        "en_US": "Left Hand (Wrist)",
        "es_ES": "Mano/Muñeca Izquierda",
        "fr_FR": "Main/Poignet Gauche",
        "ko_KR": "왼손/손목",
        "ru_RU": "Левая кисть/запястье",
        "it_IT": "Mano/Polso Sinistro"
    },
    "Right Clavicle (Collar)": {
        "zh_CN": "右锁骨 (Clavicle / Collar)",
        "ja_JP": "右鎖骨 (Clavicle / Collar)",
        "zh_TW": "右鎖骨 (Clavicle / Collar)",
        "en_US": "Right Clavicle (Collar)",
        "es_ES": "Clavícula Derecha",
        "fr_FR": "Clavicule Droite",
        "ko_KR": "오른쪽 쇄골",
        "ru_RU": "Правая ключица",
        "it_IT": "Clavicola Destra"
    },
    "Right UpperArm (Shoulder)": {
        "zh_CN": "右大臂 (UpperArm / Shoulder)",
        "ja_JP": "右上腕 (UpperArm / Shoulder)",
        "zh_TW": "右大臂 (UpperArm / Shoulder)",
        "en_US": "Right UpperArm (Shoulder)",
        "es_ES": "Brazo Sup. Derecho",
        "fr_FR": "Bras Sup. Droit",
        "ko_KR": "오른쪽 상완",
        "ru_RU": "Правое плечо",
        "it_IT": "Braccio Superiore Destro (Spalla)"
    },
    "Right LowerArm (Elbow)": {
        "zh_CN": "右小臂 (LowerArm / Elbow)",
        "ja_JP": "右前腕 (LowerArm / Elbow)",
        "zh_TW": "右小臂 (LowerArm / Elbow)",
        "en_US": "Right LowerArm (Elbow)",
        "es_ES": "Antebrazo Derecho",
        "fr_FR": "Avant-bras Droit",
        "ko_KR": "오른쪽 전완",
        "ru_RU": "Правое предплечье",
        "it_IT": "Avambraccio Destro (Gomito)"
    },
    "Right Hand (Wrist)": {
        "zh_CN": "右手/手腕 (Hand / Wrist)",
        "ja_JP": "右手/手首 (Hand / Wrist)",
        "zh_TW": "右手/手腕 (Hand / Wrist)",
        "en_US": "Right Hand (Wrist)",
        "es_ES": "Mano/Muñeca Derecha",
        "fr_FR": "Main/Poignet Droit",
        "ko_KR": "오른손/손목",
        "ru_RU": "Правая кисть/запястье",
        "it_IT": "Mano/Polso Destro"
    },
    "Left Thigh (Hip)": {
        "zh_CN": "左大腿 (Thigh / Hip)",
        "ja_JP": "左太もも (Thigh / Hip)",
        "zh_TW": "左大腿 (Thigh / Hip)",
        "en_US": "Left Thigh (Hip)",
        "es_ES": "Muslo Izquierdo",
        "fr_FR": "Cuisse Gauche",
        "ko_KR": "왼쪽 허벅지",
        "ru_RU": "Левое бедро",
        "it_IT": "Coscia Sinistra"
    },
    "Left Calf (Knee)": {
        "zh_CN": "左小腿 (Calf / Knee)",
        "ja_JP": "左すね (Calf / Knee)",
        "zh_TW": "左小腿 (Calf / Knee)",
        "en_US": "Left Calf (Knee)",
        "es_ES": "Pantorrilla Izquierda",
        "fr_FR": "Mollet Gauche",
        "ko_KR": "왼쪽 종아리",
        "ru_RU": "Левая голень",
        "it_IT": "Polpaccio Sinistro (Ginocchio)"
    },
    "Left Foot (Ankle)": {
        "zh_CN": "左脚踝 (Foot / Ankle)",
        "ja_JP": "左足首 (Foot / Ankle)",
        "zh_TW": "左腳踝 (Foot / Ankle)",
        "en_US": "Left Foot (Ankle)",
        "es_ES": "Tobillo Izquierdo",
        "fr_FR": "Cheville Gauche",
        "ko_KR": "왼쪽 발목",
        "ru_RU": "Левая лодыжка",
        "it_IT": "Piede/Caviglia Sinistra"
    },
    "Right Thigh (Hip)": {
        "zh_CN": "右大腿 (Thigh / Hip)",
        "ja_JP": "右太もも (Thigh / Hip)",
        "zh_TW": "右大腿 (Thigh / Hip)",
        "en_US": "Right Thigh (Hip)",
        "es_ES": "Muslo Derecho",
        "fr_FR": "Cuisse Droite",
        "ko_KR": "오른쪽 허벅지",
        "ru_RU": "Правое бедро",
        "it_IT": "Coscia Destra"
    },
    "Right Calf (Knee)": {
        "zh_CN": "右小腿 (Calf / Knee)",
        "ja_JP": "右すね (Calf / Knee)",
        "zh_TW": "右小腿 (Calf / Knee)",
        "en_US": "Right Calf (Knee)",
        "es_ES": "Pantorrilla Derecha",
        "fr_FR": "Mollet Droit",
        "ko_KR": "오른쪽 종아리",
        "ru_RU": "Правая голень",
        "it_IT": "Polpaccio Destro (Ginocchio)"
    },
    "Right Foot (Ankle)": {
        "zh_CN": "右脚踝 (Foot / Ankle)",
        "ja_JP": "右足首 (Foot / Ankle)",
        "zh_TW": "右腳踝 (Foot / Ankle)",
        "en_US": "Right Foot (Ankle)",
        "es_ES": "Tobillo Derecho",
        "fr_FR": "Cheville Droite",
        "ko_KR": "오른쪽 발목",
        "ru_RU": "Правая лодыжка",
        "it_IT": "Piede/Caviglia Destra"
    },
    "Pelvis (Hips)": {
        "zh_CN": "骨盆 (Pelvis / Hips)",
        "ja_JP": "骨盤 (Pelvis / Hips)",
        "zh_TW": "骨盆 (Pelvis / Hips)",
        "en_US": "Pelvis (Hips)",
        "es_ES": "Pelvis (Caderas)",
        "fr_FR": "Bassin (Hanches)",
        "ko_KR": "골반 (Pelvis / Hips)",
        "ru_RU": "Таз (Pelvis / Hips)",
        "it_IT": "Bacino (Pelvis / Fianchi)"
    },
    "Spine1 (Waist)": {
        "zh_CN": "腰椎 (Spine1 / Waist)",
        "ja_JP": "腰 (Spine1 / Waist)",
        "zh_TW": "腰椎 (Spine1 / Waist)",
        "en_US": "Spine1 (Waist)",
        "es_ES": "Cintura (Spine1)",
        "fr_FR": "Taille (Spine1)",
        "ko_KR": "허리 (Spine1 / Waist)",
        "ru_RU": "Поясница (Spine1 / Waist)",
        "it_IT": "Spina 1 (Vita)"
    },
    "Spine2 (Chest)": {
        "zh_CN": "胸部 (Spine2 / Chest)",
        "ja_JP": "胸 (Spine2 / Chest)",
        "zh_TW": "胸部 (Spine2 / Chest)",
        "en_US": "Spine2 (Chest)",
        "es_ES": "Pecho (Spine2)",
        "fr_FR": "Poitrine (Spine2)",
        "ko_KR": "가슴 (Spine2 / Chest)",
        "ru_RU": "Грудь (Spine2 / Chest)",
        "it_IT": "Spina 2 (Petto)"
    },
    "Spine3 (Up Chest)": {
        "zh_CN": "上胸部 (Spine3 / Up Chest)",
        "ja_JP": "上胸 (Spine3 / Up Chest)",
        "zh_TW": "上胸部 (Spine3 / Up Chest)",
        "en_US": "Spine3 (Up Chest)",
        "es_ES": "Pecho Superior (Spine3)",
        "fr_FR": "Haut de Poitrine (Spine3)",
        "ko_KR": "상부 가슴 (Spine3)",
        "ru_RU": "Верхняя часть груди (Spine3)",
        "it_IT": "Spina 3 (Petto Superiore)"
    },
    "Neck": {
        "zh_CN": "颈部 (Neck)",
        "ja_JP": "首 (Neck)",
        "zh_TW": "頸部 (Neck)",
        "en_US": "Neck",
        "es_ES": "Cuello",
        "fr_FR": "Cou",
        "ko_KR": "목 (Neck)",
        "ru_RU": "Шея (Neck)",
        "it_IT": "Collo"
    },
    "Head": {
        "zh_CN": "头部 (Head)",
        "ja_JP": "頭 (Head)",
        "zh_TW": "頭部 (Head)",
        "en_US": "Head",
        "es_ES": "Cabeza",
        "fr_FR": "Tête",
        "ko_KR": "머리 (Head)",
        "ru_RU": "Голова (Head)",
        "it_IT": "Testa"
    },
    "Import Bone Map JSON": {
        "en_US": "Import JSON",
        "zh_CN": "导入映射json",
        "ja_JP": "マッピングJSONをインポート",
        "zh_TW": "導入映射json",
        "es_ES": "Importar Configuración",
        "fr_FR": "Importer Configuration",
        "ko_KR": "설정 가져오기",
        "ru_RU": "Импорт настроек",
        "it_IT": "Importa Configurazione"
    },
    "Export Bone Map JSON": {
        "en_US": "Export JSON",
        "zh_CN": "导出映射json",
        "ja_JP": "マッピングJSONをエクスポート",
        "zh_TW": "導出映射json",
        "es_ES": "Exportar Configuración",
        "fr_FR": "Exporter Configuration",
        "ko_KR": "설정 내보내기",
        "ru_RU": "Экспорт настроек",
        "it_IT": "Esporta Configurazione"
    },
    "请先选择一个骨架和骨骼 (Select an armature)": {
        "en_US": "Please select an armature and bone first",
        "zh_CN": "请先选择一个骨架和骨骼",
        "ja_JP": "先にアーマチュアとボーンを選択してください",
        "zh_TW": "請先選擇一個骨架和骨骼",
        "es_ES": "Seleccione una armadura y hueso primero",
        "fr_FR": "Veuillez d'abord sélectionner une armature et un os",
        "ko_KR": "먼저 아마추어와 뼈를 선택하세요",
        "ru_RU": "Сначала выберите арматуру и кость",
        "it_IT": "Seleziona prima un'armatura e un osso"
    },
    "未选中任何骨骼 (No bone selected)": {
        "en_US": "No bone selected",
        "zh_CN": "未选中任何骨骼",
        "ja_JP": "ボーンが選択されていません",
        "zh_TW": "未選中任何骨骼",
        "es_ES": "Ningún hueso seleccionado",
        "fr_FR": "Aucun os sélectionné",
        "ko_KR": "선택된 뼈가 없습니다",
        "ru_RU": "Кость не выбрана",
        "it_IT": "Nessun osso selezionato"
    },
    "(点击绑定)": {
        "en_US": "(Click to Bind)",
        "zh_CN": "(点击绑定)",
        "ja_JP": "(クリックでバインド)",
        "zh_TW": "(點擊綁定)",
        "es_ES": "(Clic para Vincular)",
        "fr_FR": "(Cliquer pour Lier)",
        "ko_KR": "(클릭하여 바인딩)",
        "ru_RU": "(Нажмите для привязки)",
        "it_IT": "(Clicca per Associare)"
    },
    "💡 点击插槽绑定当前选中骨骼": {
        "en_US": "💡 Click a slot to bind the selected bone",
        "zh_CN": "💡 点击插槽绑定当前选中骨骼",
        "ja_JP": "💡 スロットをクリックして選択中のボーンをバインド",
        "zh_TW": "💡 點擊插槽綁定當前選中骨骼",
        "es_ES": "💡 Haz clic en una ranura para vincular el hueso seleccionado",
        "fr_FR": "💡 Cliquez sur un emplacement pour lier l'os sélectionné",
        "ko_KR": "💡 슬롯을 클릭하여 선택한 뼈를 바인딩합니다",
        "ru_RU": "💡 Нажмите на слот, чтобы привязать выбранную кость",
        "it_IT": "💡 Clicca su uno slot per associare l'osso selezionato"
    },
    "按场景帧率显示动捕 (Sync Viewport to Scene FPS)": {
        "en_US": "Sync Viewport to Scene FPS",
        "zh_CN": "按场景帧率显示动捕 (Sync Viewport to Scene FPS)",
        "ja_JP": "シーンFPSに合わせて表示 (Sync Viewport to Scene FPS)",
        "zh_TW": "按場景幀率顯示動捕",
        "es_ES": "Sincronizar Visor con FPS",
        "fr_FR": "Sync. Vue avec FPS de Scène",
        "ko_KR": "뷰포트 FPS 동기화",
        "ru_RU": "Синхр. FPS вьюпорта",
        "it_IT": "Sincronizza Vista con FPS della Scena"
    },
    "勾选后以角色当前物体位置为参考系动捕，不会强制吸回世界原点": {
        "en_US": "Capture relative to the character's current position instead of snapping to world origin.",
        "zh_CN": "勾选后以角色当前物体位置为参考系动捕，不会强制吸回世界原点",
        "ja_JP": "現在のオブジェクト位置を基準にしてキャプチャし、ワールド原点に強制的に戻りません。",
        "zh_TW": "勾選後以角色當前物體位置為參考系動捕，不會強制吸回世界原點",
        "es_ES": "Captura relativa a la posición actual del personaje en lugar de ajustarse al origen del mundo.",
        "fr_FR": "Capture relative à la position actuelle du personnage au lieu de s'aligner sur l'origine du monde.",
        "ko_KR": "캐릭터의 현재 위치를 기준으로 캡처하며, 월드 원점으로 강제 이동하지 않습니다.",
        "ru_RU": "Захват относительно текущей позиции персонажа вместо привязки к началу координат мира.",
        "it_IT": "Se attivo, il motion capture usa la posizione attuale dell'oggetto come riferimento invece di forzare l'origine del mondo."
    },
    "勾选后视口刷新率将降至与当前场景FPS一致以节省GPU性能；取消勾选则保持默认的最高实时刷新率": {
        "en_US": "When checked, the viewport refresh rate drops to match the scene FPS to save GPU; otherwise, it runs at max real-time refresh rate.",
        "zh_CN": "勾选后视口刷新率将降至与当前场景FPS一致以节省GPU性能；取消勾选则保持默认的最高实时刷新率",
        "ja_JP": "チェックすると、ビューポートの更新がシーンのFPSに同期されGPUの負荷を減らします。チェックを外すと最高リアルタイム更新レートを維持します。",
        "zh_TW": "勾選後視口刷新率將降至與當前場景FPS一致以節省GPU性能；取消勾選則保持默認的最高實時刷新率",
        "es_ES": "Al marcar, la actualización del visor baja para coincidir con los FPS de la escena y ahorrar GPU.",
        "fr_FR": "Si cochée, le taux de rafraîchissement s'aligne sur les FPS pour économiser le GPU.",
        "ko_KR": "선택 시 뷰포트 새로 고침 빈도가 씬 FPS와 일치하도록 낮아져 GPU를 절약합니다.",
        "ru_RU": "При включении частота обновления вьюпорта снижается до FPS сцены для экономии GPU.",
        "it_IT": "Se attivo, la frequenza di aggiornamento della vista scende agli FPS della scena per risparmiare GPU; altrimenti usa il massimo in tempo reale."
    },
    "💡 悬停查看对应骨骼，点击绿点快速选中": {
        "en_US": "💡 Hover to view bone name, click green dot to select",
        "zh_CN": "💡 悬停查看对应骨骼，点击绿点快速选中",
        "ja_JP": "💡 ホバーでボーン名を確認、緑の点をクリックで選択",
        "zh_TW": "💡 懸停查看對應骨骼，點擊綠點快速選中",
        "es_ES": "💡 Pasa el ratón para ver el nombre del hueso, haz clic en el punto verde para seleccionar",
        "fr_FR": "💡 Survolez pour voir le nom de l'os, cliquez sur le point vert pour sélectionner",
        "ko_KR": "💡 마우스를 올려 뼈 이름을 확인하고, 녹색 점을 클릭하여 선택합니다",
        "ru_RU": "💡 Наведите курсор, чтобы увидеть имя кости, нажмите зеленую точку для выбора",
        "it_IT": "💡 Passa il mouse per vedere il nome dell'osso, clicca sul punto verde per selezionare"
    },
    "💡 语言设置已保存！": {
        "en_US": "💡 Language saved!",
        "zh_CN": "💡 语言设置已保存！",
        "ja_JP": "💡 言語設定を保存しました！",
        "zh_TW": "💡 語言設置已保存！",
        "es_ES": "💡 ¡Idioma guardado!",
        "fr_FR": "💡 Langue sauvegardée !",
        "ko_KR": "💡 언어 설정이 저장되었습니다!",
        "ru_RU": "💡 Язык сохранен!",
        "it_IT": "💡 Impostazione della lingua salvata!"
    },
    "部分悬停提示需要重启 Blender 才能生效。": {
        "en_US": "Please restart Blender to apply tooltips.",
        "zh_CN": "部分悬停提示需要重启 Blender 才能生效。",
        "ja_JP": "ツールチップを適用するにはBlenderを再起動してください。",
        "zh_TW": "部分懸停提示需要重啟 Blender 才能生效。",
        "es_ES": "Reinicie Blender para aplicar los mensajes de información (tooltips).",
        "fr_FR": "Veuillez redémarrer Blender pour appliquer les info-bulles.",
        "ko_KR": "일부 툴팁은 Blender를 다시 시작해야 적용됩니다.",
        "ru_RU": "Перезапустите Blender, чтобы применить всплывающие подсказки.",
        "it_IT": "Alcuni tooltip richiedono il riavvio di Blender per essere applicati."
    },
    "自动根据当前 Blender 场景帧率重采样动作关键帧": {
        "en_US": "Automatically resample keyframes to match the current Blender scene FPS.",
        "zh_CN": "自动根据当前 Blender 场景帧率重采样动作关键帧",
        "ja_JP": "現在のBlenderシーンのFPSに合わせてキーフレームを自動的にリサンプリングします。",
        "zh_TW": "自動根據當前 Blender 場景幀率重採樣動作關鍵幀",
        "es_ES": "Remuestrear automáticamente fotogramas clave según los FPS de la escena.",
        "fr_FR": "Rééchantillonner automatiquement les images clés selon les FPS de la scène.",
        "ko_KR": "현재 Blender 씬 FPS에 맞게 모션 키프레임을 자동으로 리샘플링합니다.",
        "ru_RU": "Автоматически передискретизировать ключевые кадры под FPS сцены.",
        "it_IT": "Campiona automaticamente i fotogrammi chiave in base agli FPS attuali della scena di Blender."
    },
    "匹配 24 FPS 标准电影与影视动画帧率": {
        "en_US": "Match 24 FPS standard film and animation framerate.",
        "zh_CN": "匹配 24 FPS 标准电影与影视动画帧率",
        "ja_JP": "24 FPS の標準的な映画・アニメーションのフレームレートに合わせます。",
        "zh_TW": "匹配 24 FPS 標準電影與影視動畫幀率",
        "es_ES": "Coincidir con 24 FPS estándar de cine y animación.",
        "fr_FR": "Aligner sur 24 FPS standard cinéma et animation.",
        "ko_KR": "24 FPS 표준 영화 및 애니메이션 프레임 속도에 맞춥니다.",
        "ru_RU": "Соответствие 24 FPS стандарта кино и анимации.",
        "it_IT": "Adatta alla frequenza standard di 24 FPS per cinema e animazione."
    },
    "匹配 30 FPS 电视与视频帧率": {
        "en_US": "Match 30 FPS TV and video framerate.",
        "zh_CN": "匹配 30 FPS 电视与视频帧率",
        "ja_JP": "30 FPS のテレビ・動画のフレームレートに合わせます。",
        "zh_TW": "匹配 30 FPS 電視與視頻幀率",
        "es_ES": "Coincidir con 30 FPS estándar de TV y vídeo.",
        "fr_FR": "Aligner sur 30 FPS standard TV et vidéo.",
        "ko_KR": "30 FPS TV 및 비디오 프레임 속도에 맞춥니다.",
        "ru_RU": "Соответствие 30 FPS стандарта ТВ и видео.",
        "it_IT": "Adatta alla frequenza standard di 30 FPS per TV e video."
    },
    "匹配 60 FPS 原生动捕高帧率": {
        "en_US": "Match 60 FPS native high framerate mocap.",
        "zh_CN": "匹配 60 FPS 原生动捕高帧率",
        "ja_JP": "60 FPS のネイティブ高フレームレートキャプチャに合わせます。",
        "zh_TW": "匹配 60 FPS 原生動捕高幀率",
        "es_ES": "Coincidir con 60 FPS nativos de alta velocidad.",
        "fr_FR": "Aligner sur 60 FPS natifs haute fréquence.",
        "ko_KR": "60 FPS 네이티브 고프레임 모캡에 맞춥니다.",
        "ru_RU": "Соответствие 60 FPS нативного высокочастотного мокапа.",
        "it_IT": "Adatta alla frequenza nativa elevata di 60 FPS del motion capture."
    },
    "手动指定任意目标帧率数值": {
        "en_US": "Manually specify any target framerate value.",
        "zh_CN": "手动指定任意目标帧率数值",
        "ja_JP": "任意のターゲットフレームレート数値を手動で指定します。",
        "zh_TW": "手動指定任意目標幀率數值",
        "es_ES": "Especificar manualmente cualquier valor de FPS objetivo.",
        "fr_FR": "Spécifier manuellement une valeur de FPS cible.",
        "ko_KR": "임의의 목표 프레임 속도 값을 직접 지정합니다.",
        "ru_RU": "Вручную указать любое значение целевого FPS.",
        "it_IT": "Specifica manualmente qualsiasi valore di frequenza fotogrammi obiettivo."
    },
    "默认 (Default)": {
        "en_US": "Default",
        "zh_TW": "默認 (Default)",
        "ja_JP": "デフォルト (Default)",
        "es_ES": "Predeterminado",
        "fr_FR": "Défaut",
        "ko_KR": "기본 (Default)",
        "ru_RU": "По умолчанию",
        "zh_CN": "默认 (Default)",
        "it_IT": "Predefinito (Default)"
    },
    "无 (None)": {
        "en_US": "None",
        "zh_TW": "無 (None)",
        "ja_JP": "なし (None)",
        "es_ES": "Ninguno",
        "fr_FR": "Aucun",
        "ko_KR": "없음 (None)",
        "ru_RU": "Нет",
        "zh_CN": "无 (None)",
        "it_IT": "Nessuno (None)"
    },
    "比例:": {
        "en_US": "Scale:",
        "zh_TW": "比例:",
        "ja_JP": "スケール:",
        "es_ES": "Escala:",
        "fr_FR": "Échelle :",
        "ko_KR": "비율:",
        "ru_RU": "Масштаб:",
        "zh_CN": "比例:",
        "it_IT": "Scala:"
    },
    "英制:": {
        "en_US": "Imperial:",
        "zh_TW": "英制:",
        "ja_JP": "ヤード・ポンド法:",
        "es_ES": "Imperial:",
        "fr_FR": "Impérial :",
        "ko_KR": "야드파운드법:",
        "ru_RU": "Имперская:",
        "zh_CN": "英制:",
        "it_IT": "Imperiale:"
    },
    "公制:": {
        "en_US": "Metric:",
        "zh_TW": "公制:",
        "ja_JP": "メートル法:",
        "es_ES": "Métrico:",
        "fr_FR": "Métrique :",
        "ko_KR": "미터법:",
        "ru_RU": "Метрическая:",
        "zh_CN": "公制:",
        "it_IT": "Metrico:"
    },
    "米 (m)": {
        "en_US": "Meters (m)",
        "zh_TW": "米 (m)",
        "ja_JP": "メートル (m)",
        "es_ES": "Metros (m)",
        "fr_FR": "Mètres (m)",
        "ko_KR": "미터 (m)",
        "ru_RU": "Метры (m)",
        "zh_CN": "米 (m)",
        "it_IT": "Metri (m)"
    },
    "厘米 (cm)": {
        "en_US": "Centimeters (cm)",
        "zh_TW": "厘米 (cm)",
        "ja_JP": "センチメートル (cm)",
        "es_ES": "Centímetros (cm)",
        "fr_FR": "Centimètres (cm)",
        "ko_KR": "센티미터 (cm)",
        "ru_RU": "Сантиметры (cm)",
        "zh_CN": "厘米 (cm)",
        "it_IT": "Centimetri (cm)"
    },
    "毫米 (mm)": {
        "en_US": "Millimeters (mm)",
        "zh_TW": "毫米 (mm)",
        "ja_JP": "ミリメートル (mm)",
        "es_ES": "Milímetros (mm)",
        "fr_FR": "Millimètres (mm)",
        "ko_KR": "밀리미터 (mm)",
        "ru_RU": "Миллиметры (mm)",
        "zh_CN": "毫米 (mm)",
        "it_IT": "Millimetri (mm)"
    },
    "千米 (km)": {
        "en_US": "Kilometers (km)",
        "zh_TW": "千米 (km)",
        "ja_JP": "キロメートル (km)",
        "es_ES": "Kilómetros (km)",
        "fr_FR": "Kilomètres (km)",
        "ko_KR": "킬로미터 (km)",
        "ru_RU": "Километры (km)",
        "zh_CN": "千米 (km)",
        "it_IT": "Chilometri (km)"
    },
    "自适应 (Adaptive)": {
        "en_US": "Adaptive",
        "zh_TW": "自適應 (Adaptive)",
        "ja_JP": "アダプティブ (Adaptive)",
        "es_ES": "Adaptativo",
        "fr_FR": "Adaptatif",
        "ko_KR": "적응형 (Adaptive)",
        "ru_RU": "Адаптивно",
        "zh_CN": "自适应 (Adaptive)",
        "it_IT": "Adattivo (Adaptive)"
    },
    "修改场景帧率 (Change Scene FPS)": {
        "zh_CN": "修改场景帧率",
        "zh_TW": "修改場景幀率",
        "en_US": "Change Scene FPS",
        "ja_JP": "シーンFPSを変更",
        "es_ES": "Cambiar FPS de Escena",
        "fr_FR": "Modifier les FPS de la Scène",
        "ko_KR": "씬 FPS 변경",
        "ru_RU": "Изменить FPS сцены",
        "it_IT": "Modifica FPS della Scena"
    },
    "Language Changed": {
        "zh_CN": "语言已更改",
        "zh_TW": "語言已更改",
        "en_US": "Language Changed",
        "ja_JP": "言語が変更されました",
        "es_ES": "Idioma Cambiado",
        "fr_FR": "Langue Modifiée",
        "ko_KR": "언어 변경됨",
        "ru_RU": "Язык изменен",
        "it_IT": "Lingua Modificata"
    },
    "Rebocap 人偶骨骼映射器 (Puppet Bone Mapper)": {
        "zh_CN": "Rebocap 人偶骨骼映射器 (Puppet Bone Mapper)",
        "zh_TW": "Rebocap 人偶骨骼映射器 (Puppet Bone Mapper)",
        "en_US": "Rebocap Puppet Bone Mapper",
        "ja_JP": "Rebocap 人形ボーンマッピング画面 (Puppet View)",
        "es_ES": "Mapeador de Huesos Rebocap (Puppet Bone Mapper)",
        "fr_FR": "Mappeur d'Os Rebocap (Puppet Bone Mapper)",
        "ko_KR": "Rebocap 퍼펫 뼈 매퍼",
        "ru_RU": "Карта марионетки Rebocap",
        "it_IT": "Mappatore Ossa Marionetta Rebocap"
    },
    "清空全部骨骼映射": {
        "zh_CN": "清空全部骨骼映射",
        "zh_TW": "清空全部骨骼映射",
        "en_US": "Clear All Bone Mappings",
        "ja_JP": "すべてのボーンマッピングをクリア",
        "es_ES": "Borrar Todos los Mapeos de Huesos",
        "fr_FR": "Effacer Tous les Mappages d'Os",
        "ko_KR": "모든 뼈 매핑 지우기",
        "ru_RU": "Очистить все сопоставления костей",
        "it_IT": "Cancella Tutte le Mappature Ossa"
    },
    "开启人偶骨骼映射视口 (Puppet HUD)": {
        "zh_CN": "开启人偶骨骼映射视口 (Puppet HUD)",
        "zh_TW": "開啟人偶骨骼映射視口 (Puppet HUD)",
        "en_US": "Toggle Puppet Canvas HUD",
        "ja_JP": "人形ボーンHUD画面を開く (Puppet HUD)",
        "es_ES": "Alternar HUD de Marioneta",
        "fr_FR": "Basculer HUD Marionnette",
        "ko_KR": "퍼펫 스켈레톤 HUD 열기",
        "ru_RU": "Включить HUD марионетки",
        "it_IT": "Attiva HUD Marionetta"
    },
    "将选中的历史记录应用到当前时间轴": {
        "zh_CN": "将选中的历史记录应用到当前时间轴",
        "zh_TW": "將選中的歷史記錄應用到當前時間軸",
        "en_US": "Apply selected take to the current timeline",
        "ja_JP": "選択したテイクを現在のタイムラインに適用します",
        "es_ES": "Aplicar toma seleccionada a la línea de tiempo actual",
        "fr_FR": "Appliquer la prise sélectionnée à la chronologie actuelle",
        "ko_KR": "선택한 기록을 현재 타임라인에 적용합니다",
        "ru_RU": "Применить выбранный дубль к текущей шкале времени",
        "it_IT": "Applica la registrazione selezionata alla timeline corrente"
    },
    "删除当前选中的历史记录及其实际的动作数据": {
        "zh_CN": "删除当前选中的历史记录及其实际的动作数据",
        "zh_TW": "刪除當前選中的歷史記錄及其實際的動作數據",
        "en_US": "Delete selected take and its action animation data",
        "ja_JP": "選択したテイクと実際のアクションデータを削除します",
        "es_ES": "Eliminar toma seleccionada y sus datos de animación",
        "fr_FR": "Supprimer la prise sélectionnée et ses données d'animation",
        "ko_KR": "선택한 기록 및 실제 모션 데이터를 삭제합니다",
        "ru_RU": "Удалить выбранный дубль и связанные данные анимации",
        "it_IT": "Elimina la registrazione selezionata e i relativi dati di animazione"
    },
    "设置新的场景帧率": {
        "zh_CN": "设置新的场景帧率",
        "zh_TW": "設置新的場景幀率",
        "en_US": "Set new scene framerate (FPS)",
        "ja_JP": "新しいシーンフレームレートを設定",
        "es_ES": "Establecer nuevos FPS de escena",
        "fr_FR": "Définir la nouvelle fréquence d'images de la scène",
        "ko_KR": "새로운 씬 프레임 속도(FPS) 설정",
        "ru_RU": "Задать новый FPS сцены",
        "it_IT": "Imposta nuova frequenza fotogrammi della scena"
    },
    "分配当前在姿态模式或大纲中选中的骨骼 (Assign selected bone)": {
        "zh_CN": "分配当前在姿态模式或大纲中选中的骨骼 (Assign selected bone)",
        "zh_TW": "分配當前在姿態模式或大綱中選中的骨骼 (Assign selected bone)",
        "en_US": "Assign currently selected bone in Pose Mode or Outliner",
        "ja_JP": "ポーズモードまたはアウトライナーで選択中のボーンを割り当て",
        "es_ES": "Asignar hueso seleccionado en Modo Pose o Outliner",
        "fr_FR": "Assigner l'os actuellement sélectionné en Mode Pose ou Outliner",
        "ko_KR": "포즈 모드 또는 아웃라이너에서 선택된 뼈 할당",
        "ru_RU": "Назначить выбранную в режиме позы или аутлайнере кость",
        "it_IT": "Assegna l'osso attualmente selezionato in modalità Posa o nell'Outliner"
    },
    "导出片段json (Export JSON)": {
        "zh_CN": "导出片段json (Export JSON)",
        "zh_TW": "導出片段json (Export JSON)",
        "en_US": "Export Take JSON",
        "ja_JP": "テイクJSONを書き出し (Export JSON)",
        "es_ES": "Exportar JSON de Toma (Export JSON)",
        "fr_FR": "Exporter JSON de Prise (Export JSON)",
        "ko_KR": "테이크 JSON 내보내기",
        "ru_RU": "Экспорт JSON дубля",
        "it_IT": "Esporta JSON Registrazione (Export JSON)"
    },
    "导入片段json (Import JSON)": {
        "zh_CN": "导入片段json (Import JSON)",
        "zh_TW": "導入片段json (Import JSON)",
        "en_US": "Import Take JSON",
        "ja_JP": "テイクJSONを読み込み (Import JSON)",
        "es_ES": "Importar JSON de Toma (Import JSON)",
        "fr_FR": "Importer JSON de Prise (Import JSON)",
        "ko_KR": "테이크 JSON 가져오기",
        "ru_RU": "Импорт JSON дубля",
        "it_IT": "Importa JSON Registrazione (Import JSON)"
    },
    "挂载到时间轴 (Apply Take)": {
        "zh_CN": "挂载到时间轴 (Apply Take)",
        "zh_TW": "掛載到時間軸 (Apply Take)",
        "en_US": "Apply to Timeline (Apply Take)",
        "ja_JP": "タイムラインに適用 (Apply Take)",
        "es_ES": "Aplicar a Línea de Tiempo",
        "fr_FR": "Appliquer à la Chronologie",
        "ko_KR": "타임라인에 적용",
        "ru_RU": "Применить к шкале",
        "it_IT": "Applica alla Timeline (Apply Take)"
    },
    "删除记录 (Delete Take)": {
        "zh_CN": "删除记录 (Delete Take)",
        "zh_TW": "刪除記錄 (Delete Take)",
        "en_US": "Delete Record (Delete Take)",
        "ja_JP": "記録削除 (Delete Take)",
        "es_ES": "Eliminar Registro",
        "fr_FR": "Supprimer Enregistrement",
        "ko_KR": "기록 삭제",
        "ru_RU": "Удалить запись",
        "it_IT": "Elimina Registrazione (Delete Take)"
    },
    "使用选中的骨骼 (Use Selected Bone)": {
        "zh_CN": "使用选中的骨骼 (Use Selected Bone)",
        "zh_TW": "使用選中的骨骼 (Use Selected Bone)",
        "en_US": "Use Selected Bone",
        "ja_JP": "選択中のボーンを使用 (Use Selected Bone)",
        "es_ES": "Usar Hueso Seleccionado",
        "fr_FR": "Utiliser l'Os Sélectionné",
        "ko_KR": "선택된 뼈 사용",
        "ru_RU": "Использовать выбранную кость",
        "it_IT": "Usa Osso Selezionato"
    },
    "导出 JSON (Export Config)": {
        "zh_CN": "导出 JSON (Export Config)",
        "zh_TW": "導出 JSON (Export Config)",
        "en_US": "Export JSON (Export Config)",
        "ja_JP": "JSON エクスポート (Export Config)",
        "es_ES": "Exportar JSON (Export Config)",
        "fr_FR": "Exporter JSON (Export Config)",
        "ko_KR": "JSON 내보내기 (Export Config)",
        "ru_RU": "Экспорт JSON (Export Config)",
        "it_IT": "Esporta JSON (Export Config)"
    },
    "导入 JSON (Import Config)": {
        "zh_CN": "导入 JSON (Import Config)",
        "zh_TW": "導入 JSON (Import Config)",
        "en_US": "Import JSON (Import Config)",
        "ja_JP": "JSON インポート (Import Config)",
        "es_ES": "Importar JSON (Import Config)",
        "fr_FR": "Importer JSON (Import Config)",
        "ko_KR": "JSON 가져오기 (Import Config)",
        "ru_RU": "Импорт JSON (Import Config)",
        "it_IT": "Importa JSON (Import Config)"
    }
}

import locale

def get_os_language():
    try:
        if hasattr(locale, 'getdefaultlocale'):
            lang, _ = locale.getdefaultlocale()
        else:
            lang, _ = locale.getlocale()
            
        if lang:
            lang_l = lang.lower()
            if lang_l.startswith('zh_tw') or lang_l.startswith('zh_hk') or lang_l.startswith('zh_hant'):
                return 'zh_TW'
            elif lang_l.startswith('zh'):
                return 'zh_CN'
            elif lang_l.startswith('ja'):
                return 'ja_JP'
            elif lang_l.startswith('es'):
                return 'es_ES'
            elif lang_l.startswith('fr'):
                return 'fr_FR'
            elif lang_l.startswith('it'):
                return 'it_IT'
            elif lang_l.startswith('ko'):
                return 'ko_KR'
            elif lang_l.startswith('ru'):
                return 'ru_RU'
    except:
        pass
    return 'en_US'


import os

def get_saved_language():
    try:
        pref_path = os.path.join(os.path.dirname(__file__), '..', 'lang.txt')
        if os.path.exists(pref_path):
            with open(pref_path, 'r') as f:
                saved = f.read().strip()
                if saved in ('AUTO', 'EN', 'ZH', 'ZH_TW', 'JA', 'ES', 'FR', 'IT', 'KO', 'RU'):
                    return saved
    except:
        pass
    return 'AUTO'

def set_saved_language(lang_val):
    try:
        pref_path = os.path.join(os.path.dirname(__file__), '..', 'lang.txt')
        with open(pref_path, 'w') as f:
            f.write(lang_val)
    except:
        pass

def T_static(text):
    lang = get_saved_language()
    
    if lang == 'AUTO':
        locale_key = get_os_language()
    elif lang == 'ZH':
        locale_key = 'zh_CN'
    elif lang == 'ZH_TW':
        locale_key = 'zh_TW'
    elif lang == 'JA':
        locale_key = 'ja_JP'
    elif lang == 'ES':
        locale_key = 'es_ES'
    elif lang == 'FR':
        locale_key = 'fr_FR'
    elif lang == 'IT':
        locale_key = 'it_IT'
    elif lang == 'KO':
        locale_key = 'ko_KR'
    elif lang == 'RU':
        locale_key = 'ru_RU'
    else:
        locale_key = 'en_US'
        
    if text in TRANSLATIONS:
        if locale_key in TRANSLATIONS[text]:
            return TRANSLATIONS[text][locale_key]
        if 'en_US' in TRANSLATIONS[text]:
            return TRANSLATIONS[text]['en_US']
            
    return text

def T(text):
    scene = bpy.context.scene
    lang = getattr(scene, 'rebocap_language', 'AUTO')
    
    if lang == 'AUTO':
        locale_key = get_os_language()
    elif lang == 'ZH':
        locale_key = 'zh_CN'
    elif lang == 'ZH_TW':
        locale_key = 'zh_TW'
    elif lang == 'JA':
        locale_key = 'ja_JP'
    elif lang == 'ES':
        locale_key = 'es_ES'
    elif lang == 'FR':
        locale_key = 'fr_FR'
    elif lang == 'IT':
        locale_key = 'it_IT'
    elif lang == 'KO':
        locale_key = 'ko_KR'
    elif lang == 'RU':
        locale_key = 'ru_RU'
    else:
        locale_key = 'en_US'
        
    if text in TRANSLATIONS:
        if locale_key in TRANSLATIONS[text]:
            return TRANSLATIONS[text][locale_key]
        if 'en_US' in TRANSLATIONS[text]:
            return TRANSLATIONS[text]['en_US']
            
    return text
