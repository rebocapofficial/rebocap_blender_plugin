import bpy

TRANSLATIONS = {
    # UI Panel Titles
    "Connection": {
        "zh_CN": "连接与录制",
        "ja_JP": "接続と録画",
    },
    "Character Skeleton": {
        "zh_CN": "创建角色骨架",
        "ja_JP": "キャラクター骨格を作成",
    },
    "FK Animation Mode": {
        "zh_CN": "角色骨骼直驱模式 (FK Animation)",
        "ja_JP": "キャラクターFKモード (FK Animation)",
    },
    "Tracking Point Mode": {
        "zh_CN": "追踪点模式 (Tracking Point Mode)",
        "ja_JP": "トラッキングポイントモード (Tracking Point)",
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
    },
    "Wait": {
        "zh_CN": "等待",
        "ja_JP": "待機",
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
    "保持角色当前位置 (Keep Character Position)": {
        "zh_CN": "保持角色当前位置 (Keep Character Position)",
        "ja_JP": "キャラクターの現在位置を保持 (Keep Position)",
        "en_US": "Keep Character Position",
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
    },
    "Disconnect": {
        "zh_CN": "断开连接",
        "ja_JP": "切断",
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
    },
    "Stop Record": {
        "zh_CN": "停止录制",
        "ja_JP": "録画停止",
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
    },
    "Character Skeleton": {
        "zh_CN": "创建角色骨架",
        "ja_JP": "キャラクタースケルトンを作成",
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
}

import locale

def get_os_language():
    try:
        if hasattr(locale, 'getdefaultlocale'):
            lang, _ = locale.getdefaultlocale()
        else:
            lang, _ = locale.getlocale()
            
        if lang:
            if lang.startswith('zh'):
                return 'zh_CN'
            elif lang.startswith('ja'):
                return 'ja_JP'
    except:
        pass
    return 'en_US'

def T(text):
    scene = bpy.context.scene
    lang = getattr(scene, 'rebocap_language', 'AUTO')
    
    if lang == 'AUTO':
        locale_key = get_os_language()
    elif lang == 'ZH':
        locale_key = 'zh_CN'
    elif lang == 'JA':
        locale_key = 'ja_JP'
    else:
        locale_key = 'en_US'
        
    if text in TRANSLATIONS:
        if locale_key in TRANSLATIONS[text]:
            return TRANSLATIONS[text][locale_key]
        if locale_key == 'en_US' and 'en_US' in TRANSLATIONS[text]:
            return TRANSLATIONS[text]['en_US']
            
    return text
