import os
import shutil
import re

# 配置路径
INPUT_DIR = './pic'
OUTPUT_DIR = './output'

# 定义筛选规则与重命名映射 (正则表达式)
RULES = [
    # 1. 评级图标: UI_TTR_Rank_SSS.png -> rank_sss.png
    (r'UI_TTR_Rank_(.+)\.png', 'rank_{}'),
    
    # 2. Combo 徽章: UI_MSS_MBase_Icon_APp.png -> icon_{}.png
    (r'UI_MSS_MBase_Icon_(.+)\.png', 'icon_{}'),
    
    # 3. DX 星级: UI_GAM_Gauge_DXScoreIcon_01.png -> dx_star_{}.png
    (r'UI_GAM_Gauge_DXScoreIcon_0(\d)\.png', 'dx_star_{}'),
    
    # 4. Rating 数字: UI_NUM_Drating_5.png -> num_{}.png
    (r'UI_NUM_Drating_(\d)\.png', 'num_{}'),
    
    # 5. 类型标识: DX.png -> type_dx.png
    (r'^(DX|SD)\.png$', 'type_{}')
]

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"创建输出目录: {OUTPUT_DIR}")

    if not os.path.exists(INPUT_DIR):
        print(f"错误: 找不到输入目录 {INPUT_DIR}")
        return

    count = 0
    print("开始筛选并重命名素材...")

    for filename in os.listdir(INPUT_DIR):
        src_path = os.path.join(INPUT_DIR, filename)
        
        # 跳过文件夹
        if not os.path.isfile(src_path):
            continue

        for pattern, rename_fmt in RULES:
            match = re.match(pattern, filename, re.IGNORECASE)
            if match:
                # 获取匹配到的关键部分 (如 'SSS' 或 'APp')
                key_part = match.group(1).lower()
                # 构造符合 Android 规范的目标文件名
                new_name = rename_fmt.format(key_part) + ".png"
                dest_path = os.path.join(OUTPUT_DIR, new_name)
                
                # 执行拷贝
                shutil.copy2(src_path, dest_path)
                print(f"已处理: {filename} -> {new_name}")
                count += 1
                break

    print(f"\n处理完成！共导出 {count} 个有效素材到 {OUTPUT_DIR}")
    print("提示: 请直接将 output 文件夹内的所有文件拷贝到 Android 项目的 res/drawable 目录下。")

if __name__ == "__main__":
    main()