# 解剖板绘图指南

## ⚠️ 核心原则：科学准确性优先

> **所有解剖结构必须严格准确，符合科学性标准。**

在创建任何解剖板之前，必须确保：

1. **解剖学准确性** - 所有结构、位置、大小、比例必须符合解剖学标准
2. **科学合理性** - 生理机制、信号通路、因果关系必须符合当前科学共识
3. **术语规范性** - 使用标准医学/解剖学术语，避免模糊或不准确的表达
4. **参考文献校验** - 涉及复杂结构时，优先参考权威解剖学教材或文献：
   - Gray's Anatomy
   - Netter's Atlas of Human Anatomy
   - Sobotta Atlas of Human Anatomy
   - 临床解剖学标准

5. **临床相关性** - 如果涉及临床场景，确保符合临床实际

**当存在任何科学疑问时，必须主动确认或说明，不能臆造不存在的解剖关系。**

---

## 概述

本指南专门用于创建专业的医学解剖学插图，涵盖单器官、系统解剖和局部解剖三种类型，支持多种信息层次和艺术风格。

## 解剖板类型

### 单器官解剖 (Organ Anatomy)

**适用场景**：心脏、肝脏、肾脏、肺、胃、脑等单个器官的详细解剖展示

**推荐风格**：
- 现代3D风格 + 局部放大视图
- 适合展示器官内部复杂结构

**关键元素**：
- 器官整体形态
- 内部腔室、管道系统
- 主要血管进出点
- 神经分布
- 邻近器官关系

**示例提示词**：
```bash
python scripts/prompts_helper.py "心脏解剖结构" --anatomy organ deep 3d
```

---

### 系统解剖 (System Anatomy)

**适用场景**：循环系统、神经系统、消化系统、呼吸系统、泌尿系统、生殖系统、骨骼系统、肌肉系统等

**推荐风格**：
- Netter 风格 + 系统示意图
- 经典教科书风格，清晰易懂

**关键元素**：
- 系统整体分布
- 各组成部分间的关系
- 功能流向（如血液循环方向）
- 系统边界与毗邻结构

**示例提示词**：
```bash
python scripts/prompts_helper.py "循环系统" --anatomy system all netter
python scripts/prompts_helper.py "神经系统" --anatomy system full hybrid
```

---

### 局部解剖 (Regional Anatomy)

**适用场景**：头颈部、胸部、腹部、盆部、上肢、下肢等特定区域的解剖层次展示

**推荐风格**：
- 素描+3D混合风格
- 强调层次和空间关系

**关键元素**：
- 区域完整边界
- 浅层到深层的层次递进
- 关键解剖标志
- 手术入路参考

**示例提示词**：
```bash
python scripts/prompts_helper.py "头颈部解剖" --anatomy regional full hybrid
python scripts/prompts_helper.py "腹部解剖" --anatomy regional deep sketch
```

## 信息层次

### 浅层解剖 (Superficial Layer)

**展示内容**：
- 皮肤轮廓
- 皮下脂肪
- 浅筋膜
- 体表标志（landmarks）
- 可见的浅表血管、神经

**提示关键词**：
```
surface anatomy, fascia, superficial landmarks, subcutaneous structures
```

**适用场景**：体格检查、注射部位、手术切口定位

---

### 深层解剖 (Deep Layer)

**展示内容**：
- 深层器官
- 主要血管干
- 深层神经干
- 重要解剖间隙
- 关键的深层标志

**提示关键词**：
```
deep structures, deep anatomy, internal organs, deep vascular anatomy
```

**适用场景**：手术解剖、病理机制展示、治疗靶点

---

### 全层解剖 (Full Layer)

**展示内容**：
- 从浅到深的完整分层
- 各层之间的相互关系
- 横断面或纵断面展示
- 穿经各层的重要结构

**提示关键词**：
```
layered anatomy, transverse section, cross-sectional view, depth stratification
```

**适用场景**：全面教学、外科训练、断层解剖对照

## 风格说明

### Netter 风格 (netter)

**特点**：
- 经典手绘水彩质感
- 温暖柔和的配色
- 教科书式的清晰度
- 解剖精准性与艺术灵魂并存

**最适合**：医学教育、经典教科书插图

---

### 现代3D风格 (3d)

**特点**：
- 高精度3D渲染
- 光影效果逼真
- 组织的次表面散射效果
- 湿润表面的高光反射
- 临床级质量

**最适合**：临床展示、复杂结构、学术报告

---

### 素描线稿风格 (sketch)

**特点**：
- 精致的碳粉/石墨渲染
- 结构定义的交叉排线
- 羊皮纸灰色背景
- 手术场般的精确感
- 干净简洁

**最适合**：教学参考、结构强调、快速草图

---

### 混合风格 (hybrid)

**特点**：
- 结合 Netter 的温暖与现代3D的精准
- 艺术手绘轮廓叠加在照片级3D结构上
- 教育清晰度与视觉冲击力的平衡

**最适合**：综合性展示、复杂概念、出版级插图

## 标注规范

### 标注线类型
- **直线**：直接、简洁的标注
- **优雅曲线**：避免交叉时的美观标注

### 标注位置原则
- 避免遮挡关键结构
- 保持标签分布均匀
- 使用清晰的层级关系
- 标注文字大小适中，易于阅读

### 标准医学标注用词
- 动脉、静脉、神经使用规范术语
- 器官使用标准解剖学术语
- 必要时添加拉丁学名

## 常见解剖板配置示例

### 心脏解剖板
```bash
python scripts/prompts_helper.py "心脏解剖结构" --anatomy organ deep 3d
```
**特点**：展示心脏内部腔室、瓣膜、冠状动脉分支，3D渲染突出立体结构

### 腹部解剖板
```bash
python scripts/prompts_helper.py "腹部解剖" --anatomy regional full hybrid
```
**特点**：从腹壁到腹膜后的完整分层，展示各器官位置关系

### 循环系统解剖板
```bash
python scripts/prompts_helper.py "循环系统" --anatomy system all netter
```
**特点**：全身动脉、静脉分布，Netter风格清晰展示血流方向

### 头颈部解剖板
```bash
python scripts/prompts_helper.py "头颈部解剖" --anatomy regional full sketch
```
**特点**：强调各层关系和手术入路，素描风格突出结构层次
