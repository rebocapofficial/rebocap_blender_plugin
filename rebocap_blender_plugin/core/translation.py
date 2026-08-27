import bpy

TRANSLATIONS = {
    # UI Panel Titles
    "Connection": {
        "zh_CN": "连接与录制",
        "ja_JP": "接続と録画",
    
        "zh_TW": "連接與錄製",
        "es_ES": "Conexión",
        "fr_FR": "Connexion",
        "ko_KR": "연결 및 녹화",
        "ru_RU": "Подключение",
},
    "Character Skeleton": {
        "zh_CN": "创建角色骨架",
        "ja_JP": "キャラクター骨格を作成",
    
        "zh_TW": "創建角色骨架",
        "es_ES": "Esqueleto del Personaje",
        "fr_FR": "Squelette du Personnage",
        "ko_KR": "캐릭터 골격 생성",
        "ru_RU": "Создание скелета персонажа",
},
    "FK Animation Mode": {
        "zh_CN": "角色骨骼直驱模式 (FK Animation)",
        "ja_JP": "キャラクターFKモード (FK Animation)",
    
        "zh_TW": "角色骨骼直驅模式 (FK Animation)",
        "es_ES": "Modo de Animación FK",
        "fr_FR": "Mode dAnimation FK",
        "ko_KR": "캐릭터 FK 모드",
        "ru_RU": "Режим FK анимации",
},
    "Tracking Point Mode": {
        "zh_CN": "追踪点模式 (Tracking Point Mode)",
        "ja_JP": "トラッキングポイントモード (Tracking Point)",
    
        "zh_TW": "追踪點模式 (Tracking Point Mode)",
        "es_ES": "Modo de Puntos de Rastreo",
        "fr_FR": "Mode Points de Suivi",
        "ko_KR": "트래킹 포인트 모드",
        "ru_RU": "Режим точек отслеживания",
},

    # Connection Panel
    "Version: Beta 11.5": {
        "zh_CN": "Version: Beta 11.5",
        "ja_JP": "Version: Beta 11.5",
        "en_US": "Version: Beta 11.5",
    },
    "Version: Beta 11.4": {
        "zh_CN": "Version: Beta 11.4",
        "ja_JP": "Version: Beta 11.4",
    },
    "Version: Beta 11.3": {
        "zh_CN": "Version: Beta 11.3",
        "ja_JP": "Version: Beta 11.3",
    },
    "Version: Beta 11.2": {
        "zh_CN": "Version: Beta 11.2",
        "ja_JP": "Version: Beta 11.2",
    },
    "Version: Beta 11.1": {
        "zh_CN": "Version: Beta 11.1",
        "ja_JP": "Version: Beta 11.1",
    },
    "Restore T-Pose": {
        "zh_CN": "恢复 T-Pose",
        "ja_JP": "Tポーズに戻す",
    
        "zh_TW": "恢復 T-Pose",
        "es_ES": "Restaurar T-Pose",
        "fr_FR": "Restaurer T-Pose",
        "ko_KR": "T-포즈 복구",
        "ru_RU": "Сброс T-Pose",
},
    "Wait": {
        "zh_CN": "等待",
        "ja_JP": "待機",
    
        "zh_TW": "等待",
        "es_ES": "Esperar",
        "fr_FR": "Attendre",
        "ko_KR": "대기",
        "ru_RU": "Ожидание",
},
    "No bone selected.": {
        "zh_CN": "未选中任何骨骼。",
        "ja_JP": "ボーンが選択されていません。",
    },
    "Please select an armature object.": {
        "zh_CN": "请选择一个骨架物体。",
        "ja_JP": "アーマチュアオブジェクトを選択してください。",
    },
    "Selected bone": {
        "zh_CN": "已选骨骼",
        "ja_JP": "選択されたボーン",
    },
    "Bone map exported successfully": {
        "zh_CN": "骨骼映射导出成功",
        "ja_JP": "ボーンマップのエクスポートに成功しました",
    },
    "Bone map imported successfully": {
        "zh_CN": "骨骼映射导入成功",
        "ja_JP": "ボーンマップのインポートに成功しました",
    },
    "Import failed": {
        "zh_CN": "导入失败",
        "ja_JP": "インポートに失敗しました",
    },
    "* Please bind Pelvis and Legs first": {
        "zh_CN": "* 请先绑定骨盆和腿部骨骼",
        "ja_JP": "* 最初に骨盤と脚のボーンをバインドしてください",
    },
    "Ankle Height": {
        "zh_CN": "脚踝高度",
        "ja_JP": "足首の高さ",
    },
    "Mode: Applied Skeleton": {
        "zh_CN": "模式: 已应用骨架",
        "ja_JP": "モード: 適用済み骨格",
    },
    "Mode: Manual Skeleton": {
        "zh_CN": "模式: 手动骨架",
        "ja_JP": "モード: 手動骨格",
    },
    "✅ Rebocap Standard": {
        "zh_CN": "✅ Rebocap 标准骨骼 (Rebocap Standard)",
        "ja_JP": "✅ Rebocap 標準ボーン (Rebocap Standard)",
    },
    "✅ Unreal Engine (UE4/UE5/MetaHuman)": {
        "zh_CN": "✅ 虚幻引擎标准 (UE4/UE5/MetaHuman)",
        "ja_JP": "✅ Unreal Engine 標準 (UE4/UE5/MetaHuman)",
    },
    "✅ VRM Humanoid": {
        "zh_CN": "✅ VRM 人形骨架 (VRM Humanoid)",
        "ja_JP": "✅ VRM ヒューマノイド (VRM Humanoid)",
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
},
    "挂载与导出帧率设置 (FPS Mode):": {
        "zh_CN": "挂载与导出帧率设置 (FPS Mode):",
        "ja_JP": "適用とエクスポートのFPS設定 (FPS Mode):",
        "en_US": "Apply / Export FPS Settings:",
    },
    "导出片段json": {
        "zh_CN": "导出片段json",
        "ja_JP": "テイクJSONを書き出し",
        "en_US": "Export Take JSON",
    },
    "导入片段json": {
        "zh_CN": "导入片段json",
        "ja_JP": "テイクJSONを読み込み",
        "en_US": "Import Take JSON",
    },
    "插件录制时按60fps记录母带保存，": {
        "zh_CN": "插件录制时按60fps记录母带保存，",
        "ja_JP": "録画は60fpsのマスターとして保存され、",
        "en_US": "Recordings are saved at 60fps master,",
    },
    "通过该选项转换帧率挂载到blender时间轴上。": {
        "zh_CN": "通过该选项转换帧率挂载到blender时间轴上。",
        "ja_JP": "この設定で変換して時間軸に適用されます。",
        "en_US": "converted to the selected FPS on apply.",
    },
    "插件录制时按60fps记录母带保存，通过该选项转换帧率挂载到blender时间轴上。": {
        "zh_CN": "插件录制时按60fps记录母带保存，通过该选项转换帧率挂载到blender时间轴上。",
        "ja_JP": "録画は60fpsのマスターとして保存され、この設定で変換してタイムラインに適用されます。",
        "en_US": "Recordings are saved at 60fps master, and converted to the target FPS on apply.",
    },
    "👤 显示人偶骨骼HUD": {
        "zh_CN": "👤 显示人偶骨骼HUD",
        "ja_JP": "👤 人形ボーンHUD画面を開く (Puppet HUD) ➔",
        "en_US": "👤 Toggle Puppet Canvas HUD ➔",
    },
    "👤 隐藏人偶骨骼HUD": {
        "zh_CN": "👤 隐藏人偶骨骼HUD",
        "ja_JP": "👤 人形ボーンHUD画面を閉じる (Hide HUD)",
        "en_US": "👤 Close Puppet Canvas HUD",
    },
    "👤 打开人偶骨骼映射画布 (Puppet View) ➔": {
        "zh_CN": "👤 打开人偶骨骼映射画布 (Puppet View) ➔",
        "ja_JP": "👤 人形ボーンマッピング画面を開く (Puppet View) ➔",
        "en_US": "👤 Open Puppet Bone Mapper ➔",
    },
    "Rebocap 人偶画布 (Skeleton View)": {
        "zh_CN": "Rebocap 人偶画布 (Skeleton View)",
        "ja_JP": "Rebocap 人形キャンバス (Skeleton View)",
        "en_US": "Rebocap Skeleton View",
    },
    "FK 骨骼映射清单 (FK Definition):": {
        "zh_CN": "FK 骨骼映射清单 (FK Definition):",
        "ja_JP": "FKボーン定義リスト (FK Definition):",
        "en_US": "FK Bone Definition:",
    },
    "四肢对称映射:": {
        "zh_CN": "四肢对称映射:",
        "ja_JP": "四肢対称マッピング:",
        "en_US": "Limbs Mapping:",
    },
    "Left (左)": {
        "zh_CN": "Left (左)",
        "ja_JP": "Left (左)",
        "en_US": "Left",
    },
    "Right (右)": {
        "zh_CN": "Right (右)",
        "ja_JP": "Right (右)",
        "en_US": "Right",
    },
    "清空全部": {
        "zh_CN": "清空全部",
        "ja_JP": "すべてクリア",
        "en_US": "Clear All",
    },
    "片段名称": {
        "zh_CN": "片段名称",
        "ja_JP": "テイク名",
        "en_US": "Take Name",
    },
    "类型": {
        "zh_CN": "类型",
        "ja_JP": "タイプ",
        "en_US": "Type",
    },
    "总帧数": {
        "zh_CN": "总帧数",
        "ja_JP": "総フレーム数",
        "en_US": "Total Frames",
    },
    "自动匹配场景 (Auto Scene)": {
        "zh_CN": "自动匹配场景 (Auto Scene)",
        "ja_JP": "シーンFPSに自動一致 (Auto Scene)",
        "en_US": "Auto Scene FPS",
    },
    "24 FPS (电影/标准动画 Film)": {
        "zh_CN": "24 FPS (电影/标准动画 Film)",
        "ja_JP": "24 FPS (映画/標準アニメ Film)",
        "en_US": "24 FPS (Film/Animation)",
    },
    "30 FPS (电视/短视频 TV/Video)": {
        "zh_CN": "30 FPS (电视/短视频 TV/Video)",
        "ja_JP": "30 FPS (テレビ/動画 TV/Video)",
        "en_US": "30 FPS (TV/Video)",
    },
    "60 FPS (原生动捕/流畅游戏 60Hz)": {
        "zh_CN": "60 FPS (原生动捕/流畅游戏 60Hz)",
        "ja_JP": "60 FPS (ネイティブ 60Hz)",
        "en_US": "60 FPS (Native 60Hz)",
    },
    "自定义帧率 (Custom...)": {
        "zh_CN": "自定义帧率 (Custom...)",
        "ja_JP": "カスタムFPS (Custom...)",
        "en_US": "Custom FPS...",
    },
    "自定义帧率 (Target FPS)": {
        "zh_CN": "自定义帧率 (Target FPS)",
        "ja_JP": "カスタムFPS (Target FPS)",
        "en_US": "Target FPS",
    },
    "场景帧率:": {
        "zh_CN": "场景帧率:",
        "ja_JP": "シーンFPS:",
        "en_US": "Scene FPS:",
    },
    "尺寸单位:": {
        "zh_CN": "尺寸单位:",
        "ja_JP": "単位スケール:",
        "en_US": "Unit Scale:",
    },
    "确定要删除此动捕记录吗？": {
        "zh_CN": "确定要删除此动捕记录吗？",
        "ja_JP": "このキャプチャ記録を削除しますか？",
        "en_US": "Are you sure you want to delete this take?",
    },
    "此操作将永久删除相关动作数据。": {
        "zh_CN": "此操作将永久删除相关动作数据。",
        "ja_JP": "関連するアクションデータは完全に削除されます。",
        "en_US": "This will permanently remove the associated action data.",
    },
    "动捕记录已删除": {
        "zh_CN": "动捕记录已删除",
        "ja_JP": "キャプチャ記録が削除されました",
        "en_US": "Take deleted",
    },
    "Port": {
        "zh_CN": "端口",
        "ja_JP": "ポート",
    },
    "Connect": {
        "zh_CN": "连接",
        "ja_JP": "接続",
    
        "zh_TW": "連接 (Connect)",
        "es_ES": "Conectar",
        "fr_FR": "Connecter",
        "ko_KR": "연결 (Connect)",
        "ru_RU": "Подключить",
},
    "Disconnect": {
        "zh_CN": "断开连接",
        "ja_JP": "切断",
    
        "zh_TW": "斷開連接",
        "es_ES": "Desconectar",
        "fr_FR": "Déconnecter",
        "ko_KR": "연결 끊기",
        "ru_RU": "Отключить",
},
    "Connected": {
        "zh_CN": "已连接",
        "ja_JP": "接続済み",
    },
    "Pause Control": {
        "zh_CN": "暂停控制 (手动调整动作)",
        "ja_JP": "一時停止 (手動調整)",
    },
    "Restore Pose": {
        "zh_CN": "恢复原始姿态 (T-Pose)",
        "ja_JP": "元のポーズを復元 (T-Pose)",
    },
    "Start Record": {
        "zh_CN": "开始录制",
        "ja_JP": "録画開始",
    
        "zh_TW": "開始錄製",
        "es_ES": "Iniciar Grabación",
        "fr_FR": "Démarrer lEnregistrement",
        "ko_KR": "녹화 시작",
        "ru_RU": "Начать запись",
},
    "Stop Record": {
        "zh_CN": "停止录制",
        "ja_JP": "録画停止",
    
        "zh_TW": "停止錄製",
        "es_ES": "Detener Grabación",
        "fr_FR": "Arrêter lEnregistrement",
        "ko_KR": "녹화 중지",
        "ru_RU": "Остановить запись",
},
    "Enable Debug Logs": {
        "zh_CN": "开启系统调试日志",
        "ja_JP": "システムデバッグログを有効化",
    },

    # Create Skeleton Panel
    "Save Bone": {
        "zh_CN": "导出骨架文件",
        "ja_JP": "スケルトンファイルをエクスポート",
    },
    "Export Skeleton File": {
        "zh_CN": "导出骨架文件",
        "ja_JP": "スケルトンファイルをエクスポート",
    },
    "Please bind Pelvis and Legs first": {
        "zh_CN": "* 请先绑定 Pelvis(骨盆) 和双腿骨骼",
        "ja_JP": "* 最初に Pelvis (骨盤) と脚をバインドしてください",
    },
    "Foot Contact Positions": {
        "zh_CN": "足底接触点配置",
        "ja_JP": "足の接地ポイント設定",
    },
    "Place All 6 Contact Points": {
        "zh_CN": "放置全部 6 个接触点",
        "ja_JP": "6つの接触点をすべて配置",
    },
    "Left": {
        "zh_CN": "左脚",
        "ja_JP": "左足",
    },
    "Right": {
        "zh_CN": "右脚",
        "ja_JP": "右足",
    },
    "Right (Control)": {
        "zh_CN": "右脚 (主控)",
        "ja_JP": "右足 (コントロール)",
    },
    "Left (Mirrored)": {
        "zh_CN": "左脚 (自动镜像)",
        "ja_JP": "左足 (ミラー)",
    },
    "Set Point": {
        "zh_CN": "放置节点",
        "ja_JP": "ポイントを配置",
    },
    "Auto Mirrored": {
        "zh_CN": "已自动镜像",
        "ja_JP": "自動ミラー済み",
    },

    # FK Panel
    "Drive Type": {
        "zh_CN": "驱动模式",
        "ja_JP": "駆動モード",
    },
    "Source": {
        "zh_CN": "源骨架",
        "ja_JP": "ソース骨格",
    },
    "Auto Detect Config Path": {
        "zh_CN": "自动检测配置文件路径",
        "ja_JP": "設定ファイルパスを自動検出",
    },
    "Auto Detect": {
        "zh_CN": "自动检测骨骼名称",
        "ja_JP": "ボーン名を自動検出",
    },
    "Supports Mixamo & VRM naming rules": {
        "zh_CN": "支持 Mixamo 和 VRM 命名规则",
        "ja_JP": "Mixamo および VRM の命名規則をサポート",
    },
    "Setup Character Bones": {
        "zh_CN": "一键配置角色骨骼绑定",
        "ja_JP": "キャラクターボーンを自動設定",
    },
    "Import JSON": {
        "zh_CN": "导入 JSON 配置",
        "ja_JP": "JSON 設定をインポート",
    },
    "Export JSON": {
        "zh_CN": "导出 JSON 配置",
        "ja_JP": "JSON 設定をエクスポート",
    },
    "View Supported Formats": {
        "zh_CN": "查看支持的预设格式",
        "ja_JP": "サポートされているフォーマットを表示",
    },
    "Hide Supported Formats": {
        "zh_CN": "收起支持的预设格式",
        "ja_JP": "サポートされているフォーマットを隠す",
    },
    "✅ Mixamo (with/without prefix)": {
        "zh_CN": "✅ Mixamo (带/不带前缀)",
        "ja_JP": "✅ Mixamo (プレフィックスあり/なし)",
    },

    # IK Panel
    "Generate Nodes": {
        "zh_CN": "生成骨架追踪点",
        "ja_JP": "トラッキングポイントを生成",
    },
    "Node Size (mm)": {
        "zh_CN": "追踪点大小 (mm)",
        "ja_JP": "トラッキングポイントサイズ (mm)",
    },
    "Cancel Usage": {
        "zh_CN": "取消使用角色",
        "ja_JP": "キャラクターの使用をキャンセル",
    },
    "Use Rebocap Character": {
        "zh_CN": "使用 Rebocap 角色",
        "ja_JP": "Rebocap キャラクターを使用",
    },
    "Config Path": {
        "zh_CN": "上位软件配置路径 (Config Path)",
        "ja_JP": "ホストソフトウェア設定パス (Config Path)",
    },
    "Read Data": {
        "zh_CN": "读取骨骼长度",
        "ja_JP": "ボーンの長さを読み込む",
    },
    "Auto Refresh": {
        "zh_CN": "自动刷新",
        "ja_JP": "自動更新",
    },
    "Current Bone Lengths": {
        "zh_CN": "当前骨骼长度",
        "ja_JP": "現在のボーンの長さ",
    },

    # Bone Names
    "Neck & Head": {
        "zh_CN": "头颈 (Neck & Head)",
        "ja_JP": "頭と首 (Neck & Head)",
    },
    "Chest": {
        "zh_CN": "胸腔 (Chest)",
        "ja_JP": "胸 (Chest)",
    },
    "Spine": {
        "zh_CN": "脊椎 (Spine)",
        "ja_JP": "脊椎 (Spine)",
    },
    "Shoulder Width": {
        "zh_CN": "肩宽 (Shoulder Width)",
        "ja_JP": "肩幅 (Shoulder Width)",
    },
    "Upper Arm": {
        "zh_CN": "大臂 (Upper Arm)",
        "ja_JP": "上腕 (Upper Arm)",
    },
    "Lower Arm": {
        "zh_CN": "小臂 (Lower Arm)",
        "ja_JP": "前腕 (Lower Arm)",
    },
    "Hip Width": {
        "zh_CN": "胯宽 (Hip Width)",
        "ja_JP": "股幅 (Hip Width)",
    },
    "Hip Height": {
        "zh_CN": "跨高 (Hip Height)",
        "ja_JP": "股の高さ (Hip Height)",
    },
    "Upper Leg": {
        "zh_CN": "大腿 (Upper Leg)",
        "ja_JP": "大腿 (Upper Leg)",
    },
    "Lower Leg": {
        "zh_CN": "小腿 (Lower Leg)",
        "ja_JP": "下腿 (Lower Leg)",
    },
    "Foot": {
        "zh_CN": "脚掌 (Foot)",
        "ja_JP": "足 (Foot)",
    },
    "History & Takes": {
        "zh_CN": "录制历史与回放 (History & Takes)",
        "ja_JP": "録画履歴と再生 (History & Takes)",
    },
    "Connection": {
        "zh_CN": "连接与录制 (Connection)",
        "ja_JP": "接続と録画 (Connection)",
    
        "zh_TW": "連接與錄製",
        "es_ES": "Conexión",
        "fr_FR": "Connexion",
        "ko_KR": "연결 및 녹화",
        "ru_RU": "Подключение",
},
    "Character Skeleton": {
        "zh_CN": "创建角色骨架",
        "ja_JP": "キャラクタースケルトンを作成",
    
        "zh_TW": "創建角色骨架",
        "es_ES": "Esqueleto del Personaje",
        "fr_FR": "Squelette du Personnage",
        "ko_KR": "캐릭터 골격 생성",
        "ru_RU": "Создание скелета персонажа",
},
    "Apply Take": {
        "zh_CN": "挂载到时间轴 (Apply Take)",
        "ja_JP": "タイムラインに適用 (Apply Take)",
    },
    "Delete Take": {
        "zh_CN": "删除记录 (Delete Take)",
        "ja_JP": "記録削除 (Delete Take)",
    },
    "Scene FPS:": {
        "zh_CN": "场景帧率 (Scene FPS):",
    },
    "Apply / Export FPS Settings:": {
        "zh_CN": "挂载 / 导出帧率设置:",
    },
    "Apply FPS Mode": {
        "zh_CN": "应用帧率模式",
    },
    "Auto (Scene)": {
        "zh_CN": "自动 (场景帧率)",
    },
    "Custom": {
        "zh_CN": "自定义",
    },
    "Target FPS": {
        "zh_CN": "目标帧率",
    },

    # A2T Translations
    "A2T Pose Calibration (A-Pose to T-Pose)": {
        "zh_CN": "A2T 姿态校准 (A-Pose 转 T-Pose)",
        "ja_JP": "A2T ポーズキャリブレーション",
    },
    "Enable A2T Calibration": {
        "zh_CN": "启用 A2T 姿态校准",
        "ja_JP": "A2T キャリブレーションを有効化",
    },
    "* A2T Disabled (Direct Mocap Mapping)": {
        "zh_CN": "* A2T 已停用 (直连动捕映射)",
        "ja_JP": "* A2T 無効 (直接マッピング)",
    },
    "Preset Template:": {
        "zh_CN": "预设模板:",
        "ja_JP": "プリセットテンプレート:",
    },
    "Export JSON": {
        "zh_CN": "📤 导出配置 JSON",
        "ja_JP": "📤 JSON エクスポート",
    },
    "Import JSON": {
        "zh_CN": "📥 导入配置 JSON",
        "ja_JP": "📥 JSON インポート",
    },
    "Preview in Viewport": {
        "zh_CN": "👁️ 实时视口预览",
        "ja_JP": "👁️ ビューポートプレビュー",
    },
    "Reset Offsets": {
        "zh_CN": "重置所有偏移",
        "ja_JP": "オフセットをリセット",
    },
    "Symmetrical Edit (Mirror Left -> Right)": {
        "zh_CN": "对称镜像编辑 (左侧同步右侧)",
        "ja_JP": "対称ミラー編集 (左から右へ)",
    },
    "1. Left Arm": {
        "zh_CN": "1. 左上肢 (Left Arm)",
        "ja_JP": "1. 左腕 (Left Arm)",
    },
    "2. Right Arm": {
        "zh_CN": "2. 右上肢 (Right Arm)",
        "ja_JP": "2. 右腕 (Right Arm)",
    },
    "(Mirrored)": {
        "zh_CN": "(镜像联动中)",
        "ja_JP": "(ミラー連動中)",
    },
    "3. Left Leg": {
        "zh_CN": "3. 左下肢 (Left Leg)",
        "ja_JP": "3. 左脚 (Left Leg)",
    },
    "4. Right Leg": {
        "zh_CN": "4. 右下肢 (Right Leg)",
        "ja_JP": "4. 右脚 (Right Leg)",
    },
    "5. Root & Spine & Head": {
        "zh_CN": "5. 躯干与头部 (Root & Spine & Head)",
        "ja_JP": "5. 体幹と頭部 (Root & Spine & Head)",
    },
    "Left Clavicle (Collar)": {
        "zh_CN": "左锁骨 (Clavicle / Collar)",
        "ja_JP": "左鎖骨 (Clavicle / Collar)",
    },
    "Left UpperArm (Shoulder)": {
        "zh_CN": "左大臂 (UpperArm / Shoulder)",
        "ja_JP": "左上腕 (UpperArm / Shoulder)",
    },
    "Left LowerArm (Elbow)": {
        "zh_CN": "左小臂 (LowerArm / Elbow)",
        "ja_JP": "左前腕 (LowerArm / Elbow)",
    },
    "Left Hand (Wrist)": {
        "zh_CN": "左手/手腕 (Hand / Wrist)",
        "ja_JP": "左手/手首 (Hand / Wrist)",
    },
    "Right Clavicle (Collar)": {
        "zh_CN": "右锁骨 (Clavicle / Collar)",
        "ja_JP": "右鎖骨 (Clavicle / Collar)",
    },
    "Right UpperArm (Shoulder)": {
        "zh_CN": "右大臂 (UpperArm / Shoulder)",
        "ja_JP": "右上腕 (UpperArm / Shoulder)",
    },
    "Right LowerArm (Elbow)": {
        "zh_CN": "右小臂 (LowerArm / Elbow)",
        "ja_JP": "右前腕 (LowerArm / Elbow)",
    },
    "Right Hand (Wrist)": {
        "zh_CN": "右手/手腕 (Hand / Wrist)",
        "ja_JP": "右手/手首 (Hand / Wrist)",
    },
    "Left Thigh (Hip)": {
        "zh_CN": "左大腿 (Thigh / Hip)",
        "ja_JP": "左太もも (Thigh / Hip)",
    },
    "Left Calf (Knee)": {
        "zh_CN": "左小腿 (Calf / Knee)",
        "ja_JP": "左すね (Calf / Knee)",
    },
    "Left Foot (Ankle)": {
        "zh_CN": "左脚踝 (Foot / Ankle)",
        "ja_JP": "左足首 (Foot / Ankle)",
    },
    "Right Thigh (Hip)": {
        "zh_CN": "右大腿 (Thigh / Hip)",
        "ja_JP": "右太もも (Thigh / Hip)",
    },
    "Right Calf (Knee)": {
        "zh_CN": "右小腿 (Calf / Knee)",
        "ja_JP": "右すね (Calf / Knee)",
    },
    "Right Foot (Ankle)": {
        "zh_CN": "右脚踝 (Foot / Ankle)",
        "ja_JP": "右足首 (Foot / Ankle)",
    },
    "Pelvis (Hips)": {
        "zh_CN": "骨盆 (Pelvis / Hips)",
        "ja_JP": "骨盤 (Pelvis / Hips)",
    },
    "Spine1 (Waist)": {
        "zh_CN": "腰椎 (Spine1 / Waist)",
        "ja_JP": "腰 (Spine1 / Waist)",
    },
    "Spine2 (Chest)": {
        "zh_CN": "胸部 (Spine2 / Chest)",
        "ja_JP": "胸 (Spine2 / Chest)",
    },
    "Spine3 (Up Chest)": {
        "zh_CN": "上胸部 (Spine3 / Up Chest)",
        "ja_JP": "上胸 (Spine3 / Up Chest)",
    },
    "Neck": {
        "zh_CN": "颈部 (Neck)",
        "ja_JP": "首 (Neck)",
    },
    "Head": {
        "zh_CN": "头部 (Head)",
        "ja_JP": "頭 (Head)",
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
},
    "请先选择一个骨架和骨骼 (Select an armature)": {
        "en_US": "Please select an armature first",
        "zh_CN": "请先选择一个骨架和骨骼",
        "ja_JP": "先にアーマチュアを選択してください",
    },
    "未选中任何骨骼 (No bone selected)": {
        "en_US": "No bone selected",
        "zh_CN": "未选中任何骨骼",
        "ja_JP": "ボーンが選択されていません",
    },
    "(点击绑定)": {
        "en_US": "(Click to Bind)",
        "zh_CN": "(点击绑定)",
        "ja_JP": "(クリックでバインド)",
    },
    "💡 点击插槽绑定当前选中骨骼": {
        "en_US": "💡 Click a slot to bind the selected bone",
        "zh_CN": "💡 点击插槽绑定当前选中骨骼",
        "ja_JP": "💡 スロットをクリックして選択中のボーンをバインド",
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
},
    "勾选后以角色当前物体位置为参考系动捕，不会强制吸回世界原点": {
        "en_US": "Capture relative to the character's current position instead of snapping to world origin.",
        "zh_CN": "勾选后以角色当前物体位置为参考系动捕，不会强制吸回世界原点",
        "ja_JP": "現在のオブジェクト位置を基準にしてキャプチャし、ワールド原点に強制的に戻りません。"
    ,
        "zh_TW": "勾選後以角色當前物體位置為參考系動捕，不會強制吸回世界原點",
        "es_ES": "Captura relativa a la posición actual del personaje en lugar de ajustarse al origen del mundo.",
        "fr_FR": "Capture relative à la position actuelle du personnage au lieu de s'aligner sur l'origine du monde.",
        "ko_KR": "캐릭터의 현재 위치를 기준으로 캡처하며, 월드 원점으로 강제 이동하지 않습니다.",
        "ru_RU": "Захват относительно текущей позиции персонажа вместо привязки к началу координат мира.",
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
},
    "💡 悬停查看对应骨骼，点击绿点快速选中": {
        "en_US": "💡 Hover to view bone name, click green dot to select",
        "zh_CN": "💡 悬停查看对应骨骼，点击绿点快速选中",
        "ja_JP": "💡 ホバーでボーン名を確認、緑の点をクリックで選択"
    ,
        "zh_TW": "💡 懸停查看對應骨骼，點擊綠點快速選中",
        "es_ES": "💡 Pasa el ratón para ver el nombre del hueso, haz clic en el punto verde para seleccionar",
        "fr_FR": "💡 Survolez pour voir le nom de l'os, cliquez sur le point vert pour sélectionner",
        "ko_KR": "💡 마우스를 올려 뼈 이름을 확인하고, 녹색 점을 클릭하여 선택합니다",
        "ru_RU": "💡 Наведите курсор, чтобы увидеть имя кости, нажмите зеленую точку для выбора",
},
    "💡 语言设置已保存！": {
        "en_US": "💡 Language saved!",
        "zh_CN": "💡 语言设置已保存！",
        "ja_JP": "💡 言語設定を保存しました！"
    ,
        "zh_TW": "💡 語言設置已保存！",
        "es_ES": "💡 ¡Idioma guardado!",
        "fr_FR": "💡 Langue sauvegardée !",
        "ko_KR": "💡 언어 설정이 저장되었습니다!",
        "ru_RU": "💡 Язык сохранен!",
},
    "部分悬停提示需要重启 Blender 才能生效。": {
        "en_US": "Please restart Blender to apply tooltips.",
        "zh_CN": "部分悬停提示需要重启 Blender 才能生效。",
        "ja_JP": "ツールチップを適用するにはBlenderを再起動してください。"
    ,
        "zh_TW": "部分懸停提示需要重啟 Blender 才能生效。",
        "es_ES": "Reinicie Blender para aplicar los mensajes de información (tooltips).",
        "fr_FR": "Veuillez redémarrer Blender pour appliquer les info-bulles.",
        "ko_KR": "일부 툴팁은 Blender를 다시 시작해야 적용됩니다.",
        "ru_RU": "Перезапустите Blender, чтобы применить всплывающие подсказки.",
},
    "自动匹配场景 (Auto Scene)": {
        "en_US": "Auto Match Scene (Auto Scene)",
        "zh_CN": "自动匹配场景 (Auto Scene)",
        "ja_JP": "シーン自動マッチ (Auto Scene)"
    },
    "自动根据当前 Blender 场景帧率重采样动作关键帧": {
        "en_US": "Automatically resample keyframes to match the current Blender scene FPS.",
        "zh_CN": "自动根据当前 Blender 场景帧率重采样动作关键帧",
        "ja_JP": "現在のBlenderシーンのFPSに合わせてキーフレームを自動的にリサンプリングします。"
    },
    "24 FPS (电影/标准动画 Film)": {
        "en_US": "24 FPS (Film/Animation)",
        "zh_CN": "24 FPS (电影/标准动画 Film)",
        "ja_JP": "24 FPS (映画/アニメ Film)"
    },
    "匹配 24 FPS 标准电影与影视动画帧率": {
        "en_US": "Match 24 FPS standard film and animation framerate.",
        "zh_CN": "匹配 24 FPS 标准电影与影视动画帧率",
        "ja_JP": "24 FPS の標準的な映画・アニメーションのフレームレートに合わせます。"
    },
    "30 FPS (电视/短视频 TV/Video)": {
        "en_US": "30 FPS (TV/Video)",
        "zh_CN": "30 FPS (电视/短视频 TV/Video)",
        "ja_JP": "30 FPS (テレビ/動画 TV/Video)"
    },
    "匹配 30 FPS 电视与视频帧率": {
        "en_US": "Match 30 FPS TV and video framerate.",
        "zh_CN": "匹配 30 FPS 电视与视频帧率",
        "ja_JP": "30 FPS のテレビ・動画のフレームレートに合わせます。"
    },
    "60 FPS (原生动捕/流畅游戏 60Hz)": {
        "en_US": "60 FPS (Native/Game 60Hz)",
        "zh_CN": "60 FPS (原生动捕/流畅游戏 60Hz)",
        "ja_JP": "60 FPS (ネイティブ/ゲーム 60Hz)"
    },
    "匹配 60 FPS 原生动捕高帧率": {
        "en_US": "Match 60 FPS native high framerate mocap.",
        "zh_CN": "匹配 60 FPS 原生动捕高帧率",
        "ja_JP": "60 FPS のネイティブ高フレームレートキャプチャに合わせます。"
    },
    "自定义帧率 (Custom...)": {
        "en_US": "Custom FPS (Custom...)",
        "zh_CN": "自定义帧率 (Custom...)",
        "ja_JP": "カスタムFPS (Custom...)"
    },
    "手动指定任意目标帧率数值": {
        "en_US": "Manually specify any target framerate value.",
        "zh_CN": "手动指定任意目标帧率数值",
        "ja_JP": "任意のターゲットフレームレート数値を手動で指定します。"
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
                if saved in ('AUTO', 'EN', 'ZH', 'ZH_TW', 'JA', 'ES', 'FR', 'KO', 'RU'):
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
