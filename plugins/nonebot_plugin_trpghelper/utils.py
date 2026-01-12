
from typing import TYPE_CHECKING

from .data_manager import JsonIO

if TYPE_CHECKING:
    from pathlib import Path


def reply_generator(path: "Path") -> None:
    json_file = JsonIO(path)
    reply = {
        "already_publish": "您已经发起了一个团",
        "publish_tip": "接下来请输入开团信息，例：\n[游戏规则] 老派要典\n[跑团方式] 面团-语音团-文字团\n[平台] QQ+白板-枭熊-FVTT等\n[模组] 橡树洞\n[人数] 1=3\n[导引剧情] 很久很久以前\n[GM名称与联系方式] XX-Q号或加Q群号 \n请提前准备好录入信息粘贴，1分后超时后您需要重新发车\n规则+跑团方式+平台为必填项目，剩下的组成部分可以自行更改",  # noqa: E501
        "time_tip": "接下来请输入自动封团的时间，如\n18:00\n2025-07-21 19:19\n当您仅输入时间时，默认为当天",  # noqa: E501
        "publish_missing_sth": "您的发团信息缺少条目：",
        "please_check": "请检查后重新发团",
        "date_missing_sth": "您的结束时间有以下问题：",
        "published": "您的发车信息已经存入数据库并广播至其他群",
        "no_recruitments": "现在还没有团",
        "recruitments_now": "以下为今日停止招募的团",
        "recruitments_after": "以下为长时间招募的团",
        "close_recruitment_success": "封团完成",
        "close_recruitment_failed": "封团失败：\n团库里没有您发的团呢",
        "ask_for_uuid": "请输入想要封团的团ID",
        "delete_recruitment_success": "强制封团成功",
        "delete_recruitment_failed": "强制封团失败，车库里没有该编号的团",
        "broadcast_exists": "本群已经开启过了全群广播",
        "open_broadcast_success": "本群开启了全群广播",
        "broadcast_not_exists": "本群尚未开启全群广播，无法关闭",
        "close_broadcast_success": "本群关闭了全群广播",
        "wrong_recruitment_code": "您并非此ID的团的发车人，请确认后重新封车",
        "not_input_recruitment_code": "占位符：打了个空字符串进去",
        "no_rules": "未发现该规则"
    }
    json_file.save(reply)

def faq_generator(path: "Path") -> None:
    json_file = JsonIO(path)
    faq = {
        "qa1": {
            "title": "OSR是什么",
            "aliases": [
            "什么是OSR",
            "OSR含义",
            "OSR是什么意思",
            "Old School Renaissance是什么",
            "Old School Revival是什么",
            "老派复兴是什么"
            ],
            "keywords": [
            "OSR",
            "Old School Renaissance",
            "Old School Revival",
            "老派复兴",
            "TSR",
            "D&D",
            "老派游戏",
            "复古"
            ],
            "content": "OSR 是「老派复兴」（Old School Renaissance / Old School Revival）的缩写，是面向 TSR 时期 D&D 的风格和运动。\n据说 OSR 运动早在 2000s 就已萌发¹，而发展至今已经完成了「复刻经典 D&D」的夙愿。现在 OSR 可以指代一种游戏精神，也能指代一类游戏作品（充当商店分类）。\nOSR 的历史脉络可见《历史学家回顾 OSR》，标签分类体系可见第五期。OSR 的游戏精神可参考《老派游戏快速入门 (2024)》《伪经准则》 。"
        },

        "qa2": {
            "title": "NSR是什么",
            "aliases": [
            "什么是NSR",
            "NSR含义",
            "NSR是什么意思",
            "New School Revolution是什么",
            "Nu-OSR是什么"
            ],
            "keywords": [
            "NSR",
            "New School Revolution",
            "Nu-OSR",
            "新派革命",
            "OSR",
            "Into the Odd",
            "Cairn",
            "Mörk Borg",
            "Troika"
            ],
            "content": ">本条答案需要改进\nNSR 是「新派革命」（New School Revolution / Nu-OSR）的缩写，是面向 OSR 的修正主义风格，早在 2013 年就已兴起。具体来说，NSR 往往不拘泥于 D&D 规则框架，但认可现代 OSR 的精神（玩家能动性、DIY、泛用资源兼容、地城/荒野探索等等）。\n有些人会认为 NSR 完全属于 OSR，有些人则反之。总之，NSR 是 OSR 社群中最难定义的游戏风格。很容易注意到 NSR 作品通常还会倡导轻量规则、独立或强烈的美术风格等，但也不尽然。\n最著名的 NSR 作品包括 Into the Odd、Cairn、Mörk Borg、Troika 等等。"
        },

        "qa3": {
            "title": "OSR涵盖哪些D&D原典版本",
            "aliases": [
            "OSR包括哪些D&D版本",
            "OSR包含哪些原典",
            "OSR适用哪些D&D版本"
            ],
            "keywords": [
            "OSR",
            "D&D",
            "原典",
            "0E",
            "1E",
            "2E",
            "BD&D",
            "版本"
            ],
            "content": "经典 OSR 最初主要面向 0E、1E、BD&D，后来才涵盖了 2E。这些游戏版本的资源在很大程度上可以互相兼容。"
        },

        "qa4": {
            "title": "OD&D是什么",
            "aliases": [
            "什么是OD&D",
            "0E是什么",
            "什么是0E",
            "OD&D含义",
            "0E含义",
            "原始D&D是什么"
            ],
            "keywords": [
            "OD&D",
            "0E",
            "原始D&D",
            "原典",
            "TSR"
            ],
            "content": "经典 OSR 最初主要面向 0E、1E、BD&D，后来才涵盖了 2E。这些游戏版本的资源在很大程度上可以互相兼容。"
        },

        "qa5": {
            "title": "AD&D是什么/1E是什么/2E是什么",
            "aliases": [
            "什么是AD&D",
            "1E是什么",
            "2E是什么",
            "什么是1E",
            "什么是2E",
            "高级龙与地下城是什么",
            "AD&D1E是什么",
            "AD&D2E是什么"
            ],
            "keywords": [
            "AD&D",
            "1E",
            "2E",
            "高级龙与地下城",
            "TSR",
            "原典"
            ],
            "content": "AD&D 是《高级龙与地下城》的缩写，它有 1E 和 2E 先后两个主要版本。\nAD&D 1E 指代 1977–1979 年间陆续发布的一套三卷 D&D 产品，由于是 AD&D 的第一个版本而简称 1E，但在 2E 问世之前并没有特意标注上「1E」。后来，AD&D 2E 在 1989 年正式发布，简称 2E。\n所以现代称呼的「AD&D」可能同时涵盖 1E 和 2E 两个版本及其相关资源。实际上，由于底层机制相近，1E 和 2E 的资源确实也在很大程度上可以通用。"
        },

        "qa6": {
            "title": "BD&D是什么",
            "aliases": [
            "什么是BD&D",
            "BD&D含义",
            "基础D&D是什么",
            "Basic D&D是什么"
            ],
            "keywords": [
            "BD&D",
            "Basic D&D",
            "基础D&D",
            "Holmes",
            "B/X",
            "BECMI",
            "Rules Cyclopedia",
            "Classic D&D"
            ],
            "content": "BD&D 是指一条独立产品线，主要版本包括 Basic Set (Holmes)、B/X、BECMI、Rules Cyclopedia、Classic D&D。这条产品线从 1977 年开始，到 1994 年发布了最后一个版本。这条产品线的推进也是反复修订的过程。"
        },

        "qa7": {
            "title": "B/X是什么",
            "aliases": [
            "什么是B/X",
            "《基础级/专家级》是什么",
            "基础级专家级是什么",
            "B/X D&D是什么",
            "Basic/eXpert是什么"
            ],
            "keywords": [
            "B/X",
            "基础级/专家级",
            "Basic/eXpert",
            "BD&D",
            "D&D"
            ],
            "content": "B/X 是《基础级/专家级 D&D》（Basic/eXpert）的缩写，是一款 1981 年正式修订发布的 D&D 官方版本。这个版本属于 BD&D 产品线的第二个主要版本。B/X 也是 BD&D 产品线中最常复刻和讨论的版本。"
        },

        "qa8": {
            "title": "BECMI是什么",
            "aliases": [
            "什么是BECMI",
            "RC是什么",
            "RulesCyclopedia是什么",
            "什么是RC",
            "什么是Rules Cyclopedia",
            "规则大典是什么"
            ],
            "keywords": [
            "BECMI",
            "RC",
            "Rules Cyclopedia",
            "规则大典",
            "基础",
            "专家",
            "搭档",
            "大师",
            "不朽"
            ],
            "content": "BECMI 是五件连续套组的统称，分别对应「B 基础」「E 专家」「C 搭档」「M 大师」「I 不朽」。其中 B 和 E 在内容上和之前的 B/X 相差无几。\nRC 是《规则大典》（Rules Cyclopedia）的缩写，是 BECM 的修订复刻品，与其在机制上相差无几。"
        },

        "qa9": {
            "title": "TSR是什么",
            "aliases": [
            "什么是TSR",
            "TSR公司是什么",
            "D&D创始公司是什么"
            ],
            "keywords": [
            "TSR",
            "公司",
            "D&D",
            "创始人",
            "1973",
            "1997"
            ],
            "content": "TSR 是 D&D 的创始公司（1973–1997），发布了 0E 到 2E 的 D&D 产品。"
        },

        "qa10": {
            "title": "威世智是什么？",
            "aliases": [
            "什么是威世智",
            "WSZ是什么",
            "什么是WSZ",
            "Wizards of the Coast是什么",
            "海岸巫师是什么",
            "卫生纸是什么"
            ],
            "keywords": [
            "威世智",
            "WSZ",
            "Wizards of the Coast",
            "海岸巫师",
            "卫生纸",
            "孩之宝",
            "万智牌",
            "D&D"
            ],
            "content": "威世智是继承 TSR 接手 D&D 品牌的公司，发行了 3E 及之后的 D&D 产品，也重印、重编了一些 TSR 时期的历史资源。威世智是孩之宝公司的子公司，还发行了著名集换式卡牌游戏「万智牌」。\n「海岸巫师」是威世智原文（Wizards of the Coast）的直译，「WSZ」是威世智的拼音缩写，「卫生纸」恰好符合这份缩写。这就形成了三种俗称。"
        },

        "qa11": {
            "title": "5E是OSR游戏吗",
            "aliases": [
            "D&D5E是OSR吗",
            "第五版符合OSR吗",
            "5E算老派吗",
            "5E和OSR兼容吗",
            "5E符合OSR精神吗"
            ],
            "keywords": [
            "5E",
            "第五版",
            "OSR",
            "老派",
            "威世智",
            "Basic Rules",
            "Shadowdark"
            ],
            "content": "5E 不是 OSR 游戏，也不充分符合 OSR 精神。\n虽然 5E 确实有一些比 3E、4E 更符合 OSR 精神的特征，但整体而言不符合 OSR 风格的取向。\n威世智曾在 2018 年发布了一份高度借鉴 B/X 内容主题、甚至名字也叫《Basic Rules (2018)[https://media.wizards.com/2018/dnd/downloads/DnD_BasicRules_2018.pdf]》的测试资源（实际可玩）。在测试阶段，威世智还计划涵盖地城探索规则、推出荒野六角格探索产品套组。但这些内容到了实际发布阶段未能面世。在入门帷幕和勘误前的 PHB 中能找到一些废案残留。\n5E 不契合 OSR 风格的特征包括：等级/数值膨胀、重视构筑、检定机制优先、资源倾向、忽视地城探索规则（仍广泛使用地城场景）、抹消死亡风险、基于四人小组、强调局部遭遇战力平衡、轨训官方冒险。\n不过，也有玩家热衷于面向 5E 使用/创作 OSR 资源。譬如，于 2023 年问世的《Shadowdark》就算是尝试引入近 OSR 风格的 D&D 5E 魔改作品。"
        },

        "qa12": {
            "title": "「漏斗冒险」是什么",
            "aliases": [
            "什么是漏斗冒险",
            "漏斗玩法是什么",
            "0级冒险是什么",
            "DCC漏斗是什么"
            ],
            "keywords": [
            "漏斗冒险",
            "漏斗",
            "0级",
            "DCC",
            "地城探险经典",
            "OSE"
            ],
            "content": "「漏斗冒险」是一种玩法，让每名玩家操控一组平凡角色（通常为 2–5 名、0 级、随机生成），去挑战致命危险。幸存的角色可升到 1 级，晋升为正式的冒险者。\n这种玩法是《DCC 地城探险经典》发明的，但《OSE》等其他游戏也能适用。\n漏斗玩法既可以搭配专门的漏斗冒险剧本，也可以搭配寻常的低等级冒险——只需要调整好角色数量就行。\n相关阅读：《DCC 地城探险经典》《OSE·虫杂#5》"
        },

        "qa13": {
            "title": "如何入门D&D各版本原典",
            "aliases": [
            "怎么开始玩D&D原典",
            "各版本D&D入门",
            "TSR D&D怎么入门"
            ],
            "keywords": [
            "入门",
            "原典",
            "0E",
            "1E",
            "2E",
            "B/X",
            "BECMI",
            "S&W",
            "OSE",
            "DCC",
            "Shadowdark"
            ],
            "content": "当然，原典本身也是能玩的，只是有种种缘故导致不太方便。这里只介绍经典 OSR 概念中的 TSR 时期 D&D 版本。本答案假定读者真的很在乎原典，所以不提及魔改程度更高的兼容作品。\n0E：建议改玩《剑与巫法》（S&W）。OD&D 原典三卷核心书缺乏战斗系统，需要搭配《链甲》或「白盒子」的《增补I：灰鹰》才能玩。OSR 复刻品 S&W 有不同复刻思路的多种版本，可按心意选用，详见其官网说明。\n1E：建议先尝试玩原典，入门时可阅读蓝诗人写作的(入门指南)[https://porpoise-quillfish-ygj6.squarespace.com/blog/running-your-first-ad-d-campaign]。原典的编排确实非常晦涩（尤其是大量核心规则拆到了 DMG 里去，导致只读 PHB 是不够学会的），但其精髓从未有过完美复刻。即便要玩复刻品，也建议至少阅读一遍 PHB 和 DMG 而了解相关游戏理念。OSR 复刻品推荐 OSRIC 3.0（简化修改）和 OSE（资源移植）。\nB/X：建议改玩《老派要典》（OSE）。不过 B/X 原版其实已经非常易学易用了，推荐社群自制的原典合订本《Omnibus BX》，非常适合考据学习。\nBECMI：建议改玩《Rules Cyclopedia》，可外加《Wrath of the Immortals》。前者在机制上等效 BECM，后者对标 I。前述的这一套产品也是原典，但更容易学习和使用。\n2E：建议玩原典。OSR 复刻品有个简化魔改作品《For Gold and Glory》，但 2E 原典已经足够易学易用。\n更多有趣内容：推荐看看 DCC 和 Shadowdark 吧！"
        },

        "qa14": {
            "title": "B/X的战士为何没有职业能力",
            "aliases": [
            "不喜欢白板战士怎么办",
            "B/X战士为什么白板",
            "战士没有技能怎么办",
            "白板战士怎么玩",
            "战士职业能力"
            ],
            "keywords": [
            "B/X",
            "战士",
            "白板",
            "职业能力",
            "战技",
            "OSE",
            "虫杂",
            "石墓密林"
            ],
            "content": "B/X 的战士特意没有职业能力，但在各方面数值（生命值、命中率、豁免目标、武器熟练、经验需求）上略有优势。\n历史渊源：B/X 继承了 0E 的简约方案，所以没有继承 1E 的多重攻击能力。0E 讲究快速作战，B/X 讲究简化易用，所以这两个版本的战士都是白板。而 1E 则认为核心规则的战斗机制已经构成非常丰富的体验，所以也没有给战士添加更多职业能力。\nOSR 的简约自由取向：许多玩家认为，战士就是战士，白板战士是很好的基础职业，其简单纯粹反而蕴含着无数可能性。若增加纸面战技（譬如顺势斩等等），实质上会封锁战士或其他职业的即兴创意战斗。另外，战士的白板特性也能鼓励叙事成长和自创资源，譬如魔法宝物、基因突变、恶魔契约、乱吃东西、训养宠物、传奇经历等等都能带来意想不到的专属能力。\n白板，是为了不白板：玩家团体可以自行选用或创作战士的职业能力，譬如《OSE·虫杂#1》或《石墓密林》或 BECMI 演示的战技，或者《DCC》的武勇壮举，甚至《RuneQuest》的格挡机制等等。\n若不喜欢：建议禁用白板战士职业，鼓励玩家选用其他战系职业。"
        },

        "qa15": {
            "title": "有哪些常用的地图绘制网站",
            "aliases": [
            "OSR地图工具",
            "免费地图绘制软件",
            "地城地图制作",
            "六角格地图工具"
            ],
            "keywords": [
            "地图",
            "绘制",
            "软件",
            "Worldographer",
            "Dungeon Scrawl",
            "免费"
            ],
            "content": "为了避免导购倾向，只推荐这两个免费软件：\n\nWorldographer 试用版：适合绘制六角格、城镇地图等等。是很好的一站式方案。\nDungeon Scrawl 网站：适合绘制老派画风的简易地图。\n更多推荐：绝大部分制图软件都可以使用，完全没必要专为 OSR 而生。"
        },

        "qa16": {
            "title": "OSE是什么",
            "aliases": [
            "什么是OSE",
            "老派要典是什么",
            "OSE规则",
            "Old-School Essentials是什么"
            ],
            "keywords": [
            "OSE",
            "老派要典",
            "Old-School Essentials",
            "B/X",
            "复刻",
            "死灵侏儒"
            ],
            "content": "OSE 是《老派要典》（Old-School Essentials）的缩写，是一款 2019 年正式发布的 B/X D&D 复古克隆品。\nOSE 是《B/X D&D》的忠实复刻版，主要提升了可读性、提纯了规则文本；此外还补充扩展了《AD&D 1E》的游戏资源（1E 移植到 B/X 环境）。\n官方产品目录详见：(死灵侏儒 产品目录)[https://b02.zulipchat.com/#narrow/with/527153746]"
        },

        "qa17": {
            "title": "《OSE》和「OSR」的关系是什么",
            "aliases": [
            "OSE属于OSR吗",
            "OSE和OSR有什么区别",
            "OSE是OSR游戏吗"
            ],
            "keywords": [
            "OSE",
            "OSR",
            "关系",
            "经典OSR",
            "游戏风格",
            "产品"
            ],
            "content": "《OSE》是具体游戏产品，「OSR」是游戏风格。\nOSE 是一个典型的 OSR 风格的游戏产品。它忠实复刻了 B/X D&D、补充扩展了 AD&D，非常符合「经典 OSR」定义。"
        },

        "qa18": {
            "title": "OSE和2E的关系",
            "aliases": [
            "OSE能用2E资源吗",
            "OSE和AD&D2E兼容吗",
            "OSE与2E的联系"
            ],
            "keywords": [
            "OSE",
            "2E",
            "AD&D",
            "兼容",
            "资源"
            ],
            "content": "没有直接关系。\n不过，OSE 补充移植了 1E 内容，2E 和 1E 都属于 AD&D，所以可以说有间接关系。另外，OSE 确实可以很轻松地取用 2E 的资源。"
        },

        "qa19": {
            "title": "OSE和5E的关系",
            "aliases": [
            "OSE和D&D5E有关吗",
            "OSE能兼容5E吗",
            "OSE与第五版区别"
            ],
            "keywords": [
            "OSE",
            "5E",
            "D&D",
            "关系",
            "兼容"
            ],
            "content": "几乎没有关系。\nD&D 5E 的早期测试版中确实在很大程度上借鉴了 B/X 的内容主题，但那也本来就是 D&D 历代版本的文化内核。而 OSE 从内容和风格上，也都没有借鉴 5E 的内容。"
        },

        "qa20": {
            "title": "OSE适合什么世界观",
            "aliases": [
            "OSE用什么设定",
            "OSE世界观推荐",
            "OSE世设",
            "OSE官方设定"
            ],
            "keywords": [
            "OSE",
            "世界观",
            "世设",
            "密斯塔拉",
            "灰鹰",
            "费伦",
            "浩劫残阳",
            "月下地城",
            "石墓密林"
            ],
            "content": "OSE 作为提纯的规则书，特意不绑定官方世设。玩家可以自由选择任何适合 D&D 风格的世设。\n不过，确实推荐参考 OSE 官方推出的《月下地城》和《石墓密林》。\n另外，《B/X D&D》内置的官方世设是「密斯塔拉」，《AD&D》内置的官方世设是「灰鹰」。\n采用其他 D&D 世设也非常合适，譬如：费伦、浩劫残阳等等。"
        },

        "qa21": {
            "title": "既然OSE是B/X D&D的忠实复刻品，那为什么不直接玩B/X D&D",
            "aliases": [
            "OSE和B/X哪个好",
            "为什么要用OSE",
            "OSE相比B/X优势",
            "复刻版和原版区别"
            ],
            "keywords": [
            "OSE",
            "B/X",
            "复刻",
            "原典",
            "易用性",
            "排版",
            "查阅"
            ],
            "content": "B/X 原典分成两本书，而且内容相对零散，前后、来回查阅起来不太方便。而且书中含有一些解释文本和隐含世设内容，导致不利于快速定位规则文本。\nOSE 比 B/X 更加精致、清楚、易用，在行文、排版、装订上都有体现。模块化设计也有利于规定选开资源和自行魔改。在实际游戏中，使用 OSE 也会更容易快速查阅。\n不过，确实也有许多 OSE 玩家会在幕后学习或考据 B/X 原典。"
        },

        "qa22": {
            "title": "OSE是纯地城爬吗",
            "aliases": [
            "OSR只玩地城吗",
            "OSR主张纯地城爬吗",
            "OSE有没有野外冒险",
            "老派游戏是不是只有地城"
            ],
            "keywords": [
            "OSE",
            "OSR",
            "地城",
            "荒野",
            "聚落",
            "沙盒",
            "探险"
            ],
            "content": "不是。\n首先，要定义一下地城：地城泛指任何封闭式（地下/室内）冒险场景，不限于洞窟隧道、坟冢墓穴、城堡庄园、酒馆澡堂等等。\n那么地城确实是 OSE、OSR 乃至新派 D&D 的重要场景题材，但它不是唯一题材。OSR 还会涵盖「聚落探险」「荒野探险」「沙盒探险（混合）」题材。"
        },

        "qa23": {
            "title": "OSE为什么着重强调地城冒险规则",
            "aliases": [
            "OSE地城规则多吗",
            "OSE偏向地城吗",
            "地城规则篇幅"
            ],
            "keywords": [
            "OSE",
            "地城",
            "规则",
            "篇幅",
            "简洁"
            ],
            "content": "不，这是一种偏颇印象。\nOSE 的「地城冒险规则」篇幅只有两页，紧接着就是「荒野冒险规则」。其中「地城冒险规则」主要讲了近距离移动、门的交互、定时休息、处理陷阱，本质上也是泛用的。OSE（和 B/X）处处都很简洁，并且主张许多游戏内容是自然发生的。"
        },

        "qa24": {
            "title": "英文「冒险模组」从哪里找",
            "aliases": [
            "哪里下载英文冒险",
            "OSR模组资源",
            "D&D官方模组",
            "英文模组网站"
            ],
            "keywords": [
            "冒险模组",
            "英文",
            "资源",
            "BFRPG",
            "龙足论坛",
            "itch.io",
            "DTRPG",
            "OSR模组"
            ],
            "content": "D&D 官模目录—b02：<https://b02.zulipchat.com/#narrow/with/528609703>\nBFRPG (B/X) 冒险：<https://www.basicfantasy.org/downloads.html#sn_modules>\n龙足论坛冒险区：<https://www.dragonsfoot.org/fe/#FEAD13>\n在线商店 itch.io：<https://itch.io/physical-games/tag-osr>\n在线商店 DTRPG：<https://www.drivethrurpg.com/browse.php?filters=45582>\nOSR 模组讨论度榜单：<https://figcat.com/lists/osr-and-old-school-dnd-adventure-modules>"
        },

        "qa25": {
            "title": "汉化「冒险模组」从哪里找",
            "aliases": [
            "中文冒险模组",
            "汉化模组资源",
            "哪里找中文OSR模组"
            ],
            "keywords": [
            "汉化",
            "冒险模组",
            "中文",
            "B02",
            "纯美苹果园",
            "TSR",
            "OSR"
            ],
            "content": "目前主要集中在B02<https://b02.zulipchat.com/>\n\n以及纯美苹果园论坛：\nTSR 冒险模组专区：<https://www.goddessfantasy.net/bbs/index.php?board=1757.0>\nOSR 冒险剧本专区：<https://www.goddessfantasy.net/bbs/index.php?board=2081.0>"
        },
        "qa26": {
            "title": "OSR规则能玩哪些冒险",
            "aliases": [
            "OSR兼容哪些模组",
            "OSR怎么跨版本玩冒险",
            "跨版本玩冒险",
            "OSE能玩哪些冒险"
            ],
            "keywords": [
            "OSR",
            "冒险",
            "兼容",
            "跨版本",
            "OSE",
            "B/X",
            "1E",
            "2E"
            ],
            "content": "绝大部分 OSR 规则的冒险材料是互相兼容的。\n拿《OSE》举例，B/X、0E、1E、2E 的冒险统统能玩。\nD&D·官方冒险目录：<https://b02.zulipchat.com/#narrow/with/528609703>\n死灵侏儒·官方产品目录：<https://b02.zulipchat.com/#narrow/with/527153746>\n一般冒险剧本会自带相关的怪物/法术/物品数据，但如果不带（或者强度不合适），只需在你玩的规则书里找同名条目就好。如果没有原生的同名条目，就去找冒险剧本绑定的规则书里找，也能兼容。若有轻微不平滑之处，也很容易调整。\n通常而言，1E 的资源强度略高于 B/X，尤其是职业和法术。\n对于 NSR 规则，通常规则书会自带兼容指南。"
        },

        "qa27": {
            "title": "OSR的论坛推荐",
            "aliases": [
            "OSR讨论区",
            "老派游戏论坛",
            "OSR的博客推荐",
            "OSR资源网站"
            ],
            "keywords": [
            "论坛",
            "博客",
            "OSR",
            "B02",
            "Reddit",
            "Dragonsfoot",
            "Canonfire",
            "The Alexandrian",
            "Questing Beast"
            ],
            "content": "B02: https://b02.zulipchat.com/\n汇总站点：Old School RPG Planet(https://campaignwiki.org/osr/)\n论坛：Reddit r/osr(https://www.reddit.com/r/osr/)\n论坛：Dragonsfoot(https://www.dragonsfoot.org/forums/)\n论坛：Canonfire(http://www.canonfire.com/)\nD&D 产品知识库：The Acaeum(https://www.acaeum.com/index.html)\n博客：The Alexandrian(https://thealexandrian.net/)\n博客：Simulacrum(https://osrsimulacrum.blogspot.com/)\n博客：The Blue Bard - by Anthony Huso(https://porpoise-quillfish-ygj6.squarespace.com/playables)\n评测博客：Age of Dusk - by PrinceOfNothing(https://princeofnothingblogs.wordpress.com/)\n评测博客：Questing Beast - by Ben Milton(https://questingblog.com/)\n评测博客：TenFootPole - by Bryce Lynch(https://tenfootpole.org/)\n在线商店：itch.io(https://itch.io/physical-games/tag-osr)\n在线商店：DriveThruRPG(https://www.drivethrurpg.com/browse.php?filters=45582)"
        },

        "qa28": {
            "title": "上行AC或AAC是什么",
            "aliases": [
            "什么是上行AC",
            "下行AC或DAC是什么",
            "什么是下行AC",
            "AAC和DAC区别",
            "护甲等级计算"
            ],
            "keywords": [
            "AC",
            "AAC",
            "DAC",
            "上行AC",
            "下行AC",
            "护甲等级",
            "TSR",
            "3E"
            ],
            "content": "AC 是指护甲等级，详见规则书。\nAAC 是上行 AC 的缩写，是一种 AC 越高越强的 AC 计算规则；DAC 是下行 AC 的缩写，是一种 AC 越低越强的 AC 计算规则。\n在 TSR 时代的历史材料中，通常使用 DAC。在 3E 及之后的 D&D 版本中，通常使用 AAC。\n而现代 OSR 规则通常兼具两种规则，并由玩家进行二选一（要么选用 AAC，要么选用 DAC）。这种设计是为了同时兼容两种写法。\n推荐使用上行 AC。"
        },

        "qa29": {
            "title": "THAC0是什么",
            "aliases": [
            "什么是THAC0",
            "攻击奖励或BAB是什么",
            "什么是BAB",
            "零级命中值",
            "基础攻击奖励"
            ],
            "keywords": [
            "THAC0",
            "BAB",
            "零级命中值",
            "基础攻击奖励",
            "命中率",
            "DAC",
            "AAC"
            ],
            "content": "THAC0 是「零级命中值」的缩写，它是搭配 DAC 使用的「命中率」数值，越低越强。\nBAB 是「基础攻击奖励」的缩写，它是搭配 AAC 使用的「命中率」数值，越高越强。\n代 OSR 规则通常会把 BAB 写在 THAC0 后面的方括号里 THAC0 [+BAB]。"
        },

        "qa30": {
            "title": "怎么转换出AAC和BAB",
            "aliases": [
            "AAC转换公式",
            "BAB怎么算",
            "上行AC怎么算",
            "AC转换方法"
            ],
            "keywords": [
            "转换",
            "AAC",
            "BAB",
            "DAC",
            "THAC0",
            "公式",
            "BD&D",
            "1E",
            "2E"
            ],
            "content": "现代 OSR 规则通常会把所有的 AAC 和 BAB 标注好。但如果你读的材料里没有标注，也可以自行转换。\n在 BD&D、0E 中，AAC = 19 - DAC，BAB = 19 - THAC0。也就是说，用 19 减去 DAC 机制的数值，就能得到 AAC 机制的数值。\n在 1E、2E 中，AAC = 20 - DAC，BAB = 20 - THAC0。也就是说，用 20 减去 DAC 机制的数值，就能得到 AAC 机制的数值。\n在 1E 中可能找不到 THAC0。但没关系，先找到 dmg p74 的「攻击矩阵表」，再找到 AC 的 0 的那一行，那些数值就是对应等级的 THAC0。"
        },

        "qa31": {
            "title": "OSE的盗贼技能是独属于盗贼的吗",
            "aliases": [
            "盗贼技能其他职业能用吗",
            "非盗贼怎么用盗贼技能",
            "盗贼技能通用性"
            ],
            "keywords": [
            "盗贼",
            "技能",
            "职业",
            "OSE",
            "攀爬",
            "拆除陷阱",
            "潜行",
            "开锁"
            ],
            "content": "不完全是，盗贼（及类似职业）只是更擅长盗贼技能而已。\n不同裁判可能会给出不同答案。但此处我们采用《虫杂#1》的思路，解答业余职业如何使用盗贼技能。\n攀爬：在紧要关头，需要借助工具并且通过敏捷检定。\n拆除陷阱：只能通过叙事做到。\n聆听（发觉响动）：参考「聆听门后」（通常 1/6）。\n躲藏（遁入阴影）：难以遁入阴影，而躲进掩体可能需要投骰（譬如：敏捷检定或者 2/6）。\n潜行（无声行动）：在安静环境下难以潜行。在噪音环境下，标准的突袭投骰已足以涵盖潜行行为。\n开锁：难以撬锁。\n盗窃：难以扒窃。"
        }
    }
    json_file.save(faq)

def rules_aliases_generator(path: "Path") -> None:
    json_file = JsonIO(path)
    aliases = {
        "最终物语": "最终物语",
        "fu":"最终物语",
        "老派要典": "老派要典",
        "ose": "老派要典",
        "三角机构": "三角机构",
        "三角": "三角机构",
        "地城探险经典": "地城探险经典",
        "dcc": "地城探险经典",
        "恐怖录像带": "恐怖录像带",
        "vhs": "恐怖录像带",
        "恶棍": "恶棍",
        "knave": "恶棍",
        "狂野世界": "狂野世界",
        "母舰": "母舰",
        "mothership": "母舰",
        "妈妈船": "母舰",
        "龙与地下城": "龙与地下城",
        "dnd": "龙与地下城",
        "1e": "龙与地下城",
        "2e": "龙与地下城",
        "3r": "龙与地下城",
        "4e": "龙与地下城",
        "5e": "龙与地下城",
        "5r": "龙与地下城",
        "dnd2014": "龙与地下城",
        "dnd2024": "龙与地下城",
        "adnd": "龙与地下城",
        "0e": "龙与地下城",
        "3e": "龙与地下城",
        "bdnd": "龙与地下城",
        "b/x": "龙与地下城",
        "克苏鲁的呼唤": "克苏鲁的呼唤",
        "石冢": "石冢",
        "carin": "石冢",
        "阈限恐怖": "阈限恐怖",
        "lh": "阈限恐怖"
    }
    json_file.save(aliases)